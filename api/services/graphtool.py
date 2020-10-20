import graph_tool.all as gt
import numpy as np

from services.mysql import (
    get_viewers, get_content, get_engagement
)

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
    engagement = get_engagement(viewers)
    content = get_content(viewers)
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
        v_person_key[vertex] = v.get('personkey')
        v_gender[vertex] = v.get('gender')
        v_age[vertex] = v.get('age')
        v_education[vertex] = v.get('person_education')
        v_income[vertex] = v.get('householdincome')
        v_county_size[vertex] = v.get('countysize')
        viewers_map[v.get('personkey')] = vertex
    for c in content:
        vertex = g.add_vertex()
        v_is_content[vertex] = True
        v_content_sk[vertex] = c.get('contentsk')
        v_program_name[vertex] = c.get('programname')
        v_program_type[vertex] = c.get('nhiprogramtype')
        v_program_summary[vertex] = c.get('programtypesummary')
        content_map[c.get('contentsk')] = vertex
    for e in engagement:
        v = viewers_map[e.get('personkey')]
        c = content_map[e.get('contentsk')]
        edge = g.add_edge(v, c)
        eng = e.get('engagement')
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

def recurseDown(item, results):
    if type(item[1]) is tuple:
        if item[0] not in results:
            results[item[0]] = {}
        recurseDown(item[1], results[item[0]])
    else:
        if item[0] not in results:
            results[item[0]] = []
        results[item[0]].append(get_result_item(item[1]))

def recurseUp(max_level, blocks, level, i, item, results):
    if level == max_level:
        recurseDown(item, results)
    else:
        b = blocks[level]
        recurseUp(max_level, blocks, level + 1, b[i], (b[i], item), results)

def build_nest_block_model(viewer_condition, content_condition, size, use_deg_corr, use_edge_weights):
    g = build_tree(viewer_condition, content_condition, size)
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

    levels = state.get_levels()
    blocks = []
    for level in levels:
        blocks.append(level.get_blocks())
    verticies = g.get_vertices()
    results = {}
    for i, v in enumerate(verticies):
        recurseUp(len(blocks), blocks, 0, i, v, results)
    return results
