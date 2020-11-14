import graph_tool.all as gt
import numpy as np
import pandas as pd
from sklearn import preprocessing
from os import mkdir, path
from datetime import datetime

from services.mysql import (
    # get_viewers,
    # get_content,
    # get_engagement,
    recordData
)

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
v_network = None
e_engagement = None

def save_results(size, viewer_condition, content_condition, viewers, engagement, content, useOnDemand):
    now = datetime.now()
    nowStr = now.strftime("%b-%d_%H:%M:%S")
    mkdir(path.join('data', nowStr))
    recordData(viewer_condition, content_condition, size, nowStr, useOnDemand)

    fileName = path.join('data', nowStr, 'info.txt')
    with open(fileName, 'a') as file1:
        file1.write(f'useOnDemand: {useOnDemand}\n')
        file1.write(f'size: {size}\n')
        file1.write(f'viewer condition: {viewer_condition}\n')
        file1.write(f'content condition: {content_condition}\n')
        file1.close() 

    engagement_df = pd.DataFrame(engagement)
    engagement_df.to_csv(path.join('data', nowStr, 'engagement.csv'))
    viewers_df = pd.DataFrame(viewers)
    viewers_df.to_csv(path.join('data', nowStr, 'viewers.csv'))
    content_df = pd.DataFrame(content)
    content_df.to_csv(path.join('data', nowStr, 'content.csv'))


def build_tree(useOnDemand, viewer_condition, content_condition, size):
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
    global v_network

    viewers = get_viewers(size, viewer_condition, useOnDemand)
    print(f"Viewers: {len(viewers)}")
    if (len(viewers) < int(size)):
        raise Exception("Too few viewers were found using the given condtions")
    engagement = get_engagement(viewers, content_condition, useOnDemand)
    engagement_df = pd.DataFrame(engagement)
    engagement_df.loc[engagement_df['ENGAGEMENT'] > 100, ['ENGAGEMENT']] = 100
    engagement_df['SCALED_ENGAGEMENT'] = preprocessing.scale(engagement_df['ENGAGEMENT'])
    # engagement_df.to_csv('engagement.csv')
    print(f"Engagement: {len(engagement)}")
    content = get_content(viewers, content_condition, useOnDemand)
    print(f"Content: {len(content)}")
    save_results(size, viewer_condition, content_condition, viewers, engagement, content, useOnDemand)
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
    v_network = g.new_vertex_property("string")
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
    g.vertex_properties['network'] = v_network
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
        v_network[vertex] = c.get(case('primarynetwork'))
        content_map[c.get(case('contentsk'))] = vertex
    for key, e in engagement_df.iterrows():
        v = viewers_map[e.get(case('personkey'))]
        c = content_map[e.get(case('contentsk'))]
        edge = g.add_edge(v, c)
        eng = e.get('SCALED_ENGAGEMENT')
        e_engagement[edge] = eng
    return g, engagement_df

def get_result_item(v):
    if v_is_content[v]:
        return {
            "type": "content",
            "content_key": v_content_sk[v],
            "program_name": v_program_name[v],
            "program_type": v_program_type[v],
            "program_summary": v_program_summary[v],
            "network": v_network[v]
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

def addToCount(object, key):
    if key in object:
        object[key] += 1
    else:
        object[key] = 1

def initAggregates():
    content = {
        "program_type": {},
        "program_summary": {},
        "network": {}
    }
    viewers = {
        "age": 0,
        "gender": {},
        "county_size": {},
        "income": 0,
        "education": {}
    }
    return (content, viewers)

def aggregate_content(content, aggs):
    addToCount(aggs.get("program_type"), content.get("program_type"))
    addToCount(aggs.get("program_summary"), content.get("program_summary"))
    addToCount(aggs.get("network"), content.get("network"))

def aggregate_viewers(viewers, aggs):
    addToCount(aggs.get("gender"), viewers.get("gender"))
    addToCount(aggs.get("county_size"), viewers.get("county_size"))
    addToCount(aggs.get("education"), viewers.get("education"))
    aggs['age'] += int(viewers.get("age"))
    aggs['income'] += int(viewers.get("income"))

def build_block_model(useOnDemand, viewer_condition, content_condition, size, use_deg_corr, use_edge_weights):
    g, engagement_df = build_tree(useOnDemand, viewer_condition, content_condition, size)
    state_args = dict(recs=[g.ep.engagement],rec_types=["real-exponential"]) if use_edge_weights else dict()
    state = gt.minimize_blockmodel_dl(g
        , state_args=state_args
        , deg_corr=use_deg_corr
    )
    b = state.get_blocks()
    verticies = g.get_vertices()
    results = {
        "entropy": state.entropy(),
        "results": [],
        "edges": engagement_df.to_dict('records')
    }
    counter = { "count": 0 }
    for i, v in enumerate(verticies):
        matching = [x for x in results.get("results") if x.get('name') == b[i]]
        children = []
        block = {}
        if matching:
            # the block was found, so get it's children array so we can append a value
            block = matching[0]
            children = block.get("children")
        else:
            # the block does not yet have an entry in the result set, so add one
            counter['count'] += 1
            (content_aggs, viewer_aggs) = initAggregates()
            block = {
                "id": counter.get('count'),
                "name": b[i],
                "children": children,
                "viewer_count": 0,
                "content_count": 0,
                "viewer_aggs": viewer_aggs,
                "content_aggs": content_aggs
            }
            results['results'].append(block)

        if v_is_content[v]:
            # the vertex is content, so check whether we already have a list of content for this block
            block['content_count'] += 1
            match = [x for x in children if x.get('name') == 'Content']
            content = {"content": []}
            if match:
                # We have a content list, so get it
                content = match[0]['children'][0]
            else:
                # create a new content list
                counter['count'] += 1
                children.append({ "id": counter.get('count'), 'name': 'Content', 'children': [content]})
            result_item = get_result_item(v)
            aggregate_content(result_item, block.get("content_aggs"))
            content['content'].append(result_item)
        else:
            # the vertex is a viewer, so check whether we already have a list of viewers for this block
            block['viewer_count'] += 1
            match = [x for x in children if x.get('name') == 'Viewers']
            viewers = {"viewers": []}
            if match:
                # we have a viewer list, so get it
                viewers = match[0]['children'][0]
            else:
                # create a new viewer list
                counter['count'] += 1
                children.append({ "id": counter.get('count'), 'name': 'Viewers', 'children': [viewers]})
            result_item = get_result_item(v)
            aggregate_viewers(result_item, block.get("viewer_aggs"))
            viewers["viewers"].append(result_item)
    return results

def recurseDown(item, results, counter, vertex):
    matching = [x for x in results if x.get('name') == item[0]]
    children = []
    block = {}
    if matching:
        block = matching[0]
        children = block.get("children")
    else:
        counter['count'] += 1
        (content_aggs, viewer_aggs) = initAggregates()
        block = {
            "id": counter.get('count'),
            "name": item[0],
            "children": children,
            "viewer_count": 0,
            "content_count": 0,
            "viewer_aggs": viewer_aggs,
            "content_aggs": content_aggs
        }
        results.append(block)
    
    result_item = get_result_item(vertex)
    if v_is_content[vertex]:
        block['content_count'] += 1
        aggregate_content(result_item, block.get("content_aggs"))
    else:
        block['viewer_count'] += 1
        aggregate_viewers(result_item, block.get("viewer_aggs"))

    if type(item[1]) is tuple:
        recurseDown(item[1], children, counter, vertex)
    else:
        if v_is_content[vertex]:
            match = [x for x in children if x.get('name') == 'Content']
            content = {"content": []}
            if match:
                content = match[0]['children'][0]
            else:
                counter['count'] += 1
                children.append({ "id": counter.get('count'), 'name': 'Content', 'children': [content]})
            content['content'].append(result_item)
        else:
            match = [x for x in children if x.get('name') == 'Viewers']
            viewers = {"viewers": []}
            if match:
                viewers = match[0]['children'][0]
            else:
                counter['count'] += 1
                children.append({ "id": counter.get('count'), 'name': 'Viewers', 'children': [viewers]})
            viewers["viewers"].append(result_item)

def recurseUp(max_level, blocks, level, i, item, results, counter, vertex):
    if level == max_level:
        recurseDown(item, results, counter, vertex)
    else:
        b = blocks[level]
        recurseUp(max_level, blocks, level + 1, b[i], (b[i], item), results, counter, vertex)

def build_nest_block_model(useOnDemand, viewer_condition, content_condition, size, use_deg_corr, use_edge_weights):
    g, engagement_df = build_tree(useOnDemand, viewer_condition, content_condition, size)
    print("building model")
    state_args = dict(recs=[g.ep.engagement],rec_types=["real-normal"]) if use_edge_weights else dict()
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
    results = {
        "entropy": state.entropy(),
        "results": [],
        "edges": engagement_df.to_dict('records')
    }
    counter = { "count": 0 }
    for i, v in enumerate(verticies):
        recurseUp(len(blocks), blocks, 0, i, v, results.get("results"), counter, v)
    return results
