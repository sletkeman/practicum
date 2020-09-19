from services.snowflake import (
    get_viewers, get_content, get_engagement
)
from flask import abort
# import graph_tool.all as gt

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

# def build_tree():
#     global v_is_content
#     global v_person_key
#     global v_content_sk
#     global v_program_name
#     global v_program_type
#     global v_program_summary
#     global e_engagement
#     global v_race
#     global v_gender
#     global v_age
#     viewer_condition = "v.hascat and v.age > 60 and v.gender = 'F'"
#     viewers = get_viewers(200, viewer_condition)
#     engagement = get_engagement(viewers)
#     content = get_content(viewers)
#     viewers_map = {}
#     content_map = {}
#     g = gt.Graph()
#     v_is_content = g.new_vertex_property("bool")
#     v_person_key = g.new_vertex_property("string")
#     v_race = g.new_vertex_property("string")
#     v_gender = g.new_vertex_property("string")
#     v_age = g.new_vertex_property("string")
#     v_content_sk = g.new_vertex_property("int")
#     v_program_name = g.new_vertex_property("string")
#     v_program_type = g.new_vertex_property("string")
#     v_program_summary = g.new_vertex_property("string")
#     e_engagement = g.new_edge_property("int")
#     g.vertex_properties["is_content"] = v_is_content
#     g.vertex_properties['person_key'] = v_person_key
#     g.vertex_properties['race'] = v_race
#     g.vertex_properties['gender'] = v_gender
#     g.vertex_properties['age'] = v_age
#     g.vertex_properties['content_sk'] = v_content_sk
#     g.vertex_properties['program_name'] = v_program_name
#     g.vertex_properties['program_type'] = v_program_name
#     g.vertex_properties['program_summary'] = v_program_summary
#     g.edge_properties['engagement'] = e_engagement
#     for v in viewers:
#         vertex = g.add_vertex()
#         v_is_content[vertex] = False
#         v_person_key[vertex] = v['PERSONKEY']
#         v_race[vertex] = v['RACE']
#         v_gender[vertex] = v['GENDER']
#         v_age[vertex] = v['AGE']
#         viewers_map[v['PERSONKEY']] = vertex
#     for c in content:
#         vertex = g.add_vertex()
#         v_is_content[vertex] = True
#         v_content_sk[vertex] = c['CONTENTSK']
#         v_program_name[vertex] = c['PROGRAMNAME']
#         v_program_type[vertex] = c['NHIPROGRAMTYPE']
#         v_program_summary[vertex] = c['PROGRAMTYPESUMMARY']
#         content_map[c['CONTENTSK']] = vertex
#     for e in engagement:
#         v = viewers_map[e['PERSONKEY']]
#         c = content_map[e['CONTENTSK']]
#         edge = g.add_edge(v, c)
#         e_engagement[edge] = e['ENGAGEMENT']
#     return g

def get_data():
    try:
        # g = build_tree()
        # state = gt.minimize_blockmodel_dl(g
        #     # , state_args=dict(recs=[g.ep.engagement],rec_types=["real-exponential"])
        #     , deg_corr=True
        # )
        # print(state.entropy())
        # b = state.get_blocks()
        # verticies = g.get_vertices()
        results = {}
        # for i, v in enumerate(verticies):
        #     if b[i] not in results:
        #         results[b[i]] = []
        #     if v_is_content[v]:
        #         results[b[i]].append(f"C: {v_program_name[v]} ~~ {v_program_type[v]} ~~ {v_program_summary[v]}")
        #     else:
        #         results[b[i]].append(f"V: {v_person_key[v]} ~~ {v_age[v]} ~~ {v_gender[v]} ~~ {v_race[v]}")
        return results
    except Exception as e:
        abort(500, e)

# def recurse(max_level, blocks, v, level, i, results):
#     b = blocks[level]
#     if level + 1 == max_level:
#         if b[i] not in results:
#             results[b[i]] = []
#         if v_is_content[v]:
#             results[b[i]].append(f"C: {v_program_name[v]} ~~ {v_program_type[v]} ~~ {v_program_summary[v]}")
#         else:
#             results[b[i]].append(f"V: {v_person_key[v]} ~~ {v_age[v]} ~~ {v_gender[v]} ~~ {v_race[v]}")
#     else:
#         if b[i] not in results:
#             results[b[i]] = {}
#         recurse(max_level, blocks, v, level + 1, b[i], results[b[i]])

# def get_data():
#     try:
#         g = build_tree()
#         state = gt.minimize_nested_blockmodel_dl(g
#             # , state_args=dict(recs=[g.ep.engagement],rec_types=["real-exponential"])
#             , deg_corr=True
#         )
#         print(state.entropy())
#         levels = state.get_levels()
#         blocks = []
#         for level in levels:
#             blocks.append(level.get_blocks())
#             print(levels)
#         verticies = g.get_vertices()
#         results = {}
#         for i, v in enumerate(verticies):
#             recurse(len(blocks), blocks, v, 0, i, results)
#         return results
#     except Exception as e:
#         abort(500, e)