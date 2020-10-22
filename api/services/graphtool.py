import graph_tool.all as gt
import numpy as np

# from services.mysql import (
#     get_viewers, get_content, get_engagement
# )

from services.snowflake import (
    get_viewers, get_content, get_engagement
)

def case(key):
    return key.upper()

v_is_content = None
v_person_key = None
v_education = None
v_income = None
v_county_size = None
v_gender = None
v_age = None
v_content_sk = None
v_program_name = None
v_program_type = None
v_program_summary = None
e_engagement = None

def build_tree(viewer_condition, content_condition, size):
    global v_is_content
    global v_person_key
    global v_content_sk
    global v_program_name
    global v_program_type
    global v_program_summary
    global e_engagement
    global v_education
    global v_income
    global v_county_size
    global v_gender
    global v_age

    viewers = get_viewers(size, viewer_condition, content_condition)
    print(f"Viewers: {len(viewers)}")
    if (len(viewers) < int(size)):
        raise Exception("Too few viewers were found using the given condtions")
    engagement = get_engagement(viewers)
    print(f"Engagement: {len(engagement)}")
    content = get_content(viewers)
    print(f"Content: {len(content)}")
    viewers_map = {}
    content_map = {}
    g = gt.Graph()
    v_is_content = g.new_vertex_property("bool")
    v_person_key = g.new_vertex_property("string")
    v_education = g.new_vertex_property("string")
    v_county_size = g.new_vertex_property("string")
    v_income= g.new_vertex_property("int")
    v_gender = g.new_vertex_property("string")
    v_age = g.new_vertex_property("string")
    v_content_sk = g.new_vertex_property("int")
    v_program_name = g.new_vertex_property("string")
    v_program_type = g.new_vertex_property("string")
    v_program_summary = g.new_vertex_property("string")
    e_engagement = g.new_edge_property("int")
    g.vertex_properties["is_content"] = v_is_content
    g.vertex_properties['person_key'] = v_person_key
    g.vertex_properties['education'] = v_education
    g.vertex_properties['county_size'] = v_county_size
    g.vertex_properties['income'] = v_income
    g.vertex_properties['gender'] = v_gender
    g.vertex_properties['age'] = v_age
    g.vertex_properties['content_sk'] = v_content_sk
    g.vertex_properties['program_name'] = v_program_name
    g.vertex_properties['program_type'] = v_program_name
    g.vertex_properties['program_summary'] = v_program_summary
    g.edge_properties['engagement'] = e_engagement
    for v in viewers:
        vertex = g.add_vertex()
        v_is_content[vertex] = False
        v_person_key[vertex] = v.get(case('personkey'))
        v_gender[vertex] = v.get(case('gender'))
        v_age[vertex] = v.get(case('age'))
        v_education[vertex] = v.get(case('person_education'))
        v_income[vertex] = v.get(case('householdincome'))
        v_county_size[vertex] = v.get(case('countysize'))
        viewers_map[v.get(case('personkey'))] = vertex
    for c in content:
        vertex = g.add_vertex()
        v_is_content[vertex] = True
        v_content_sk[vertex] = c.get(case('contentsk'))
        v_program_name[vertex] = c.get(case('programname'))
        v_program_type[vertex] = c.get(case('nhiprogramtype'))
        v_program_summary[vertex] = c.get(case('programtypesummary'))
        content_map[c.get(case('contentsk'))] = vertex
    for e in engagement:
        v = viewers_map[e.get(case('personkey'))]
        c = content_map[e.get(case('contentsk'))]
        edge = g.add_edge(v, c)
        eng = e.get(case('engagement'))
        e_engagement[edge] = eng if eng <= 100 else 100
    return g

def get_result_item(v):
    if v_is_content[v]:
        return {
            "type": "content",
            "content_key": v_content_sk[v],
            "program_name": v_program_name[v],
            "program_type": v_program_type[v],
            "program_summary": v_program_summary[v] 
        }
    else:
        return {
            "type": "viewer",
            "person_key": v_person_key[v],
            "age": v_age[v],
            "gender": v_gender[v],
            "county_size": v_county_size[v],
            "income": v_income[v],
            "education": v_education[v]
        }

def build_block_model(viewer_condition, content_condition, size, use_deg_corr, use_edge_weights):
    g = build_tree(viewer_condition, content_condition, size)
    state_args = dict(recs=[g.ep.engagement],rec_types=["real-exponential"]) if use_edge_weights else dict()
    state = gt.minimize_blockmodel_dl(g
        , state_args=state_args
        , deg_corr=use_deg_corr
    )
    print(state.entropy())
    b = state.get_blocks()
    verticies = g.get_vertices()
    results = {}
    for i, v in enumerate(verticies):
        if b[i] not in results:
            results[b[i]] = []
        results[b[i]].append(get_result_item(v))
    return results

def recurseDown(item, results, counter):
    matching = [x for x in results if x.get('name') == item[0]]
    children = []
    if len(matching) == 0:
        counter['count'] += 1
        results.append({
            "id": counter.get('count'),
            "name": item[0],
            "children": children
        })
    else:
        children = results[0].get("children")

    if type(item[1]) is tuple:
        recurseDown(item[1], children, counter)
    else:
        if v_is_content[item[1]]:
            match = [x for x in children if x.get('name') == 'Content']
            content = {"content": []}
            if match:
                content = match[0]['children'][0]
            else:
                counter['count'] += 1
                children.append({ "id": counter.get('count'), 'name': 'Content', 'children': [content]})
            content['content'].append(get_result_item(item[1]))
        else:
            match = [x for x in children if x.get('name') == 'Viewers']
            viewers = {"viewers": []}
            if match:
                viewers = match[0]['children'][0]
            else:
                counter['count'] += 1
                children.append({ "id": counter.get('count'), 'name': 'Viewers', 'children': [viewers]})
            viewers["viewers"].append(get_result_item(item[1]))

def recurseUp(max_level, blocks, level, i, item, results, counter):
    if level == max_level:
        recurseDown(item, results, counter)
    else:
        b = blocks[level]
        recurseUp(max_level, blocks, level + 1, b[i], (b[i], item), results, counter)

def build_nest_block_model(viewer_condition, content_condition, size, use_deg_corr, use_edge_weights):
    g = build_tree(viewer_condition, content_condition, size)
    print("building model")
    state_args = dict(recs=[g.ep.engagement],rec_types=["real-exponential"]) if use_edge_weights else dict()
    state = gt.minimize_nested_blockmodel_dl(g
        , state_args=state_args
        , deg_corr=use_deg_corr
    )

        # expand and improve the model
        # S1 = state.entropy()
        # state = state.copy(bs=state.get_bs() + [np.zeros(1)] * 4, sampling=True)
        # for i in range(100):
        #     ret = state.multiflip_mcmc_sweep(niter=10, beta=np.inf)
        # S2 = state.entropy()
        # print("Improvement:", S2 - S1)
    print("preparing results")
    levels = state.get_levels()
    blocks = []
    for level in levels:
        blocks.append(level.get_blocks())
    verticies = g.get_vertices()
    results = []
    counter = { "count": 0 }
    for i, v in enumerate(verticies):
        recurseUp(len(blocks), blocks, 0, i, v, results, counter)
    return results
