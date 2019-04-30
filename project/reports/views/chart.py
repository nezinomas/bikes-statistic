from django.http import JsonResponse
from django.shortcuts import render

from ..library.chart import get_color
from ..library.overall import Overall


def overall(request):
    o = Overall()

    series = []
    for i, bike in enumerate(o.bikes):
        item = {
            'name': bike,
            'data': o.distances[i],
            'color': get_color(i, 0.35),
            'borderColor': get_color(i, 1),
            'borderWidth': '0.5',
        }
        series.append(item)

    chart = {
        'overall': {
            'xAxis': o.years,
            'series': series[::-1],
        }
    }

    context = {
        'chart': chart,
        'tbody': o.totals_table,
        'tfooter': o.totals_grand
    }
    return render(request, template_name='reports/overall.html', context=context)
