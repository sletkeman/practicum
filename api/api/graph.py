"""
useful for setup
sln -s /usr/local/Cellar/graph-tool/2.33/lib/python3.8/site-packages/graph_tool /Users/sletkeman/practicum/venv/lib/python3.8/site-packages
"""

from flask import abort
from json import dump, load
from operator import itemgetter
from services.graphtool import (
    build_block_model,
    build_nest_block_model
)

def get_condition(body):
    viewer_condition = 'TRUE'
    content_condition = 'TRUE'
    programName, programCategory, programTypeSummary, programType, network, \
      gender, useAge, age, useIncome, income, useChildren, children, useAdults, adults, \
      useViewingMinutes, viewingMinutes, countySize, educationLevel, language, size, hasCat, hasDog \
      = itemgetter('programName', 'programCategory', 'programTypeSummary', 'programType', 'network',
        'gender', 'useAge', 'age', 'useIncome', 'income', 'useChildren', 'children', 'useAdults', 'adults',
        'useViewingMinutes', 'viewingMinutes', 'countySize', 'educationLevel', 'language', 'size', 'hasCat', 'hasDog'
        )(body)

    # content
    if programName:
        joined = "','".join(programName)
        content_condition = f"{content_condition} AND programname in ('{joined}')"
    if programCategory:
        content_condition = f"{content_condition} AND programcategory = '{programCategory}'"
    if programTypeSummary:
        joined = "','".join(programTypeSummary)
        content_condition = f"{content_condition} AND programtypesummary in ('{joined}')"
    if programType:
        joined = "','".join(programType)
        content_condition = f"{content_condition} AND nhiprogramtype in ('{joined}')"
    if network:
        joined = "','".join(network)
        content_condition = f"{content_condition} AND primarynetwork in ('{joined}')"

    # viewers
    if gender:
        viewer_condition = f"{viewer_condition} AND v.gender = '{gender[0]}'"
    if useAge:
        viewer_condition = f"{viewer_condition} AND v.age >= {age[0]} AND v.age <= {age[1]}"
    if useIncome:
        viewer_condition = f"{viewer_condition} AND v.income >= {income[0]} AND v.income <= {income[1]}"
    if useChildren:
        viewer_condition = f"{viewer_condition} AND v.numberofchildren >= {children[0]} AND v.numberofchildren <= {children[1]}"
    if useAdults:
        viewer_condition = f"{viewer_condition} AND v.numberofadults >= {adults[0]} AND v.numberofadults <= {adults[1]}"
    if  useViewingMinutes:
        viewer_condition = f"{viewer_condition} AND v.weekly_viewing_minutes >= {viewingMinutes[0]} AND v.weekly_viewing_minutes <= {viewingMinutes[1]}" 
    if countySize:
        viewer_condition = f"{viewer_condition} AND v.country_size_level = '{countySize}'"
    if educationLevel:
        viewer_condition = f"{viewer_condition} AND v.person_education_level = {educationLevel}"
    if language:
        viewer_condition = f"{viewer_condition} AND v.languageofhousehold = '{language}'"
    if size:
        viewer_condition = f"{viewer_condition} AND v.householdsize = '{size}'"
    if hasCat:
        viewer_condition = f"{viewer_condition} AND v.hascat"
    if hasDog:
        viewer_condition = f"{viewer_condition} AND v.hasdog"
    return viewer_condition, content_condition

def get_data(body):
    try:
        useNestedModel, useDegreeCorrection, useEdgeWeights, sampleSize = \
          itemgetter('useNestedModel', 'useDegreeCorrection', 'useEdgeWeights', 'sampleSize')(body)
        viewer_condition, content_condition = get_condition(body)
        result = {}
        if useNestedModel:
            result = build_nest_block_model(viewer_condition, content_condition, sampleSize, useDegreeCorrection, useEdgeWeights)
        else:
            result = build_block_model(viewer_condition, content_condition, sampleSize, useDegreeCorrection, useEdgeWeights)
        with open('result.json', 'w') as fp:
            dump(result, fp)
        return result, 200
    except Exception as ex:
        abort(500, str(ex))

# def get_data(body):
#     try:
#         f = open('result.json')
#         data = load(f)
#         return data, 200
#     except Exception as ex:
#         abort(500, str(ex))