"""
useful for setup
sln -s /usr/local/Cellar/graph-tool/2.33/lib/python3.8/site-packages/graph_tool /Users/sletkeman/practicum/venv/lib/python3.8/site-packages
"""

from flask import abort
from operator import itemgetter
from services.graphtool import (
    build_block_model,
    build_nest_block_model
)

def get_condition(body):
    result = ''
    programName, programCategory, programTypeSummary, programType, network, \
      gender, useAge, age, useIncome, income, useChildren, children, useAdults, adults, \
      useViewingMinutes, viewingMinutes, countySize, educationLevel, language, size, hasCat, hasDog \
      = itemgetter('programName', 'programCategory', 'programTypeSummary', 'programType', 'network',
        'gender', 'useAge', 'age', 'useIncome', 'income', 'useChildren', 'children', 'useAdults',
        'adults', 'countySize', 'educationLevel', 'language', 'useViewingMinutes', 'viewingMinutes',
        'size', 'hasCat', 'hasDog')(body)
    if programName:
        result = f"{result} c.programname in ('{"','".join([name for name in programName])}')"
    if programCategory:
        result = f"{result} c.programcategory in ('{"','".join([cat for cat in programCategory])}')"
    if programTypeSummary:
        result = f"{result} c.programtypesummary in ('{"','".join([s for s in programTypeSummary])}')"
    if programType:
        result = f"{result} c.programtype in ('{"','".join([t for t in programCategory])}')"
    if network:
        result = f"{result} c.primarynetwork in ('{"','".join([net for net in network])}')"

def get_data(body):
    try:
        useNestedModel, useDegreeCorrection, useEdgeWeights, sampleSize = \
          itemgetter('useNestedModel', 'useDegreeCorrection', 'useEdgeWeights', 'sampleSize')(body)
        condition = get_condition(body)
        print(condition)
        # if useNestedModel:
        #     return build_nest_block_model(condition, sampleSize, useDegreeCorrection, useEdgeWeights)
        # else:
        #     return build_block_model(condition, sampleSize, useDegreeCorrection, useEdgeWeights)
        return 'Yay!', 200
    except Exception as ex:
        abort(500, ex.args[1])


