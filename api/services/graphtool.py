import graph_tool.all as gt
import numpy as np

from services.mysql import (
    get_viewers, get_content, get_engagement
)

v_is_content = None
v_person_key = None
v_race = None
v_gender = None
v_age = None
v_content_sk = None
v_program_name = None
v_program_type = None
v_program_summary = None
e_engagement = None

def build_tree(condition, size):
    global v_is_content
    global v_person_key
    global v_content_sk
    global v_program_name
    global v_program_type
    global v_program_summary
    global e_engagement
    global v_race
    global v_gender
    global v_age

    viewers = get_viewers(size, condition)
    engagement = get_engagement(viewers)
    content = get_content(viewers)
    viewers_map = {}
    content_map = {}
    g = gt.Graph()
    v_is_content = g.new_vertex_property("bool")
    v_person_key = g.new_vertex_property("string")
    v_race = g.new_vertex_property("string")
    v_gender = g.new_vertex_property("string")
    v_age = g.new_vertex_property("string")
    v_content_sk = g.new_vertex_property("int")
    v_program_name = g.new_vertex_property("string")
    v_program_type = g.new_vertex_property("string")
    v_program_summary = g.new_vertex_property("string")
    e_engagement = g.new_edge_property("int")
    g.vertex_properties["is_content"] = v_is_content
    g.vertex_properties['person_key'] = v_person_key
    g.vertex_properties['race'] = v_race
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
        # v_race[vertex] = v.get('RACE')
        # v_gender[vertex] = v.get('GENDER')
        # v_age[vertex] = v.get('AGE')
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

def build_block_model(condition, size, use_deg_corr, use_edge_weights):
    g = build_tree(condition, size)
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
        if v_is_content[v]:
            results[b[i]].append(f"C: {v_program_name[v]} ~~ {v_program_type[v]} ~~ {v_program_summary[v]}")
        else:
            results[b[i]].append(f"V: {v_person_key[v]} ~~ {v_age[v]} ~~ {v_gender[v]} ~~ {v_race[v]}")
    return results

def recurse(max_level, blocks, v, level, i, results):
    b = blocks[level]
    if level + 1 == max_level:
        if b[i] not in results:
            results[b[i]] = []
        if v_is_content[v]:
            results[b[i]].append(f"C: {v_program_name[v]} ~~ {v_program_type[v]} ~~ {v_program_summary[v]}")
        else:
            results[b[i]].append(f"V: {v_person_key[v]} ~~ {v_age[v]} ~~ {v_gender[v]} ~~ {v_race[v]}")
    else:
        if b[i] not in results:
            results[b[i]] = {}
        recurse(max_level, blocks, v, level + 1, b[i], results[b[i]])

def build_nest_block_model(condition, size, use_deg_corr, use_edge_weights):
    g = build_tree(condition, size)
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
        recurse(len(blocks), blocks, v, 0, i, results)
    return results
