
create or replace view VW_COMMUNITY_ENGAGEMENT as

with community_group_genre as (
  select group_id, group_preponderant_genre
  from (
    select gc.group_id, genre.genre as group_preponderant_genre, sum(genre.weight * e.engagement) as total_weight
    , row_number() over (partition by gc.group_id order by total_weight desc) as genre_rank
    from engagement_ondemand.content c
    inner join genres.program_genres genre
    on c.programtypesummary = genre.programtypesummary
    and c.programname = genre.program
    inner join communities_ondemand.group_content gc
    on c.contentsk = gc.contentsk
    inner join communities_ondemand.group_viewers gv
    on gc.group_id = gv.group_id
    inner join engagement_ondemand.engagement e
    on gc.contentsk = e.contentsk
    and gv.personkey = e.personkey       
    group by gc.group_id, genre.genre 
  ) g
  where genre_rank = 1
)

, group_relations as (
    select distinct 
    g1.group_id
    , case when g1.parent_group_id = '' then 1 else 0 end as is_top_level
    , case when g2.parent_group_id is null then 1 else 0 end as is_bottom_level
    from communities_ondemand.community_group g1
    left outer join communities_ondemand.community_group g2
    on g1.group_id = g2.parent_group_id
)

select 
gc.group_id as community_group_id
, g.parent_group_id as parent_community_group_id
, gr.is_top_level
, gr.is_bottom_level
, gg.group_preponderant_genre
, g.top_programs
, c.*
, ifnull(genre.genre, 'Unknown') as program_genre
, v.*
, e.engagement

from engagement_ondemand.content c
  
left outer join genres.program_genres genre
on c.programtypesummary = genre.programtypesummary
and c.programname = genre.program
and genre.weight = 1
  
inner join communities_ondemand.group_content gc
on c.contentsk = gc.contentsk

inner join group_relations gr
on gc.group_id = gr.group_id

left outer join community_group_genre gg
on gc.group_id = gg.group_id

inner join communities_ondemand.community_group g
on gc.group_id = g.group_id
inner join communities_ondemand.group_viewers gv
on gc.group_id = gv.group_id
inner join engagement_ondemand.engagement e
on gc.contentsk = e.contentsk
and gv.personkey = e.personkey
inner join engagement_ondemand.viewers v
on gv.personkey = v.personkey
;