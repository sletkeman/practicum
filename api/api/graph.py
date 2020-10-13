"""
useful for setup
sln -s /usr/local/Cellar/graph-tool/2.33/lib/python3.8/site-packages/graph_tool /Users/sletkeman/practicum/venv/lib/python3.8/site-packages
"""

from flask import abort
from json import dumps
from operator import itemgetter
from services.graphtool import (
    build_block_model,
    build_nest_block_model
)

def get_condition(body):
    result = 'TRUE'
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
        result = f"{result} AND c.programname in ('{joined}')"
    if programCategory:
        result = f"{result} AND c.programcategory = '{programCategory}'"
    if programTypeSummary:
        joined = "','".join(programTypeSummary)
        result = f"{result} AND c.programtypesummary in ('{joined}')"
    if programType:
        joined = "','".join(programType)
        result = f"{result} AND c.programtype in ('{joined}')"
    if network:
        joined = "','".join(network)
        result = f"{result} AND c.primarynetwork in ('{joined}')"

    # viewers
    if gender:
        result = f"{result} AND v.gender = '{gender[0]}'"
    if useAge:
        result = f"{result} AND v.age >= {age[0]} AND v.age <= {age[1]}"
    if useIncome:
        result = f"{result} AND v.income >= {income[0]} AND v.income <= {income[1]}"
    if useChildren:
        result = f"{result} AND v.numberofchildren >= {children[0]} AND v.numberofchildren <= {children[1]}"
    if useAdults:
        result = f"{result} AND v.numberofadults >= {adults[0]} AND v.numberofadults <= {adults[1]}"
    if  useViewingMinutes:
        result = f"{result} AND v.weekly_viewing_minutes >= {viewingMinutes[0]} AND v.weekly_viewing_minutes <= {viewingMinutes[1]}" 
    if countySize:
        result = f"{result} AND v.country_size_level = '{countySize}'"
    if educationLevel:
        result = f"{result} AND v.person_education_level = {educationLevel}"
    if language:
        result = f"{result} AND v.languageofhousehold = '{language}'"
    if size:
        result = f"{result} AND v.householdsize = '{size}'"
    if hasCat:
        result = f"{result} AND v.hascat"
    if hasDog:
        result = f"{result} AND v.hasdog"
    return result

def get_data(body):
    try:
        useNestedModel, useDegreeCorrection, useEdgeWeights, sampleSize = \
          itemgetter('useNestedModel', 'useDegreeCorrection', 'useEdgeWeights', 'sampleSize')(body)
        condition = get_condition(body)
        print(condition)
        if useNestedModel:
            return build_nest_block_model(condition, sampleSize, useDegreeCorrection, useEdgeWeights), 200
        else:
            return build_block_model(condition, sampleSize, useDegreeCorrection, useEdgeWeights), 200
    except Exception as ex:
        abort(500, str(ex))


