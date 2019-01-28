import json
from calendar import monthrange
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from . import forms, models
from ..bikes.models import Bike

from .library.insert_data import insert_data as inserter
from .library.overall import Overall


def save_data(request, context, form, start_date, end_date):
    data = {}

    if request.method == 'POST':
        if form.is_valid():

            """
            f = form.save(commit=False)
            f.distance = 999
            f.save()
            """
            form.save()
            #"""

            data['form_is_valid'] = True
            objects = models.Data.objects.prefetch_related(
                'bike').filter(date__range=(start_date, end_date))
            data['html_list'] = render_to_string(
                'reports/includes/partial_data_list.html', {'objects': objects, 'start_date': start_date, 'end_date': end_date})
        else:
            data['form_is_valid'] = False

    context['form'] = form
    data['html_form'] = render_to_string(
        'reports/includes/partial_data_update.html', context, request)

    return JsonResponse(data)


def test(request):

    return render(
        request,
        'reports/test.html',
        context={'var': 'kintamasis is view', 'var1': '? ar tikrai?'}
    )


@login_required()
def data_empty(request):
    now = datetime.now()
    return redirect(
        reverse(
            'reports:data_list',
            kwargs={
                'start_date': '{y}-{m:02d}-{d}'.format(y=now.year, m=now.month, d='01'),
                'end_date': '{y}-{m:02d}-{d:02d}'.format(y=now.year, m=now.month, d=monthrange(now.year, now.month)[1]),
            }
        )
    )


@login_required()
def data_partial(request, start_date):
    now = datetime.now()
    return redirect(
        reverse(
            'reports:data_list',
            kwargs={
                'start_date': start_date,
                'end_date': '{y}-{m:02d}-{d:02d}'.format(y=now.year, m=now.month, d=monthrange(now.year, now.month)[1]),
            }
        )
    )


@login_required()
def data_list(request, start_date, end_date):
    # paspaustas filter mygtukas
    if 'date_filter' in request.POST:
        filter_form = forms.DateFilterForm(request.POST)
        if filter_form.is_valid():
            data = filter_form.cleaned_data
            url = reverse_lazy('reports:data_list', kwargs={
                               'start_date': data['start_date'], 'end_date': data['end_date']})
            return redirect(url)

    qs = models.Data.objects.prefetch_related('bike').filter(date__range=(start_date, end_date))
    filter_form = forms.DateFilterForm(
        initial={'start_date': start_date, 'end_date': end_date})
    return render(
        request,
        'reports/data_list.html',
        {
            'objects': qs,
            'filter_form': filter_form,
            'start_date': start_date,
            'end_date': end_date
        })


@login_required()
def data_create(request, start_date, end_date):
    form = forms.DataFormNew(request.POST or None)
    context = {
        'url': reverse('reports:data_create', kwargs={'start_date': start_date, 'end_date': end_date})
    }
    return save_data(request, context, form, start_date, end_date)


@login_required
def data_delete(request, start_date, end_date, pk):
    object = get_object_or_404(models.Data, pk=pk)
    data = {}

    if request.method == 'POST':
        object.delete()
        data['form_is_valid'] = True
        objects = models.Data.objects.prefetch_related(
            'bike').filter(date__range=(start_date, end_date))
        data['html_list'] = render_to_string(
            'reports/includes/partial_data_list.html', {'objects': objects, 'start_date': start_date, 'end_date': end_date})
    else:
        context = {'object': object, 'start_date': start_date, 'end_date': end_date}
        data['html_form'] = render_to_string(
            'reports/includes/partial_data_delete.html', context, request)

    return JsonResponse(data)


@login_required()
def data_update(request, start_date, end_date, pk):
    object = get_object_or_404(models.Data, pk=pk)
    form = forms.DataFormNew(request.POST or None, instance=object)
    context = {
        'url': reverse('reports:data_update', kwargs={'start_date': start_date, 'end_date': end_date, 'pk': pk})
    }
    return save_data(request, context, form, start_date, end_date)


@login_required()
def data_table(request, start_date, end_date):
    # paspaustas filter mygtukas
    if 'date_filter' in request.POST:
        filter_form = forms.DateFilterForm(request.POST)
        if filter_form.is_valid():
            data = filter_form.cleaned_data
            url = reverse_lazy('reports:data_table', kwargs={'start_date': data['start_date'], 'end_date': data['end_date']})
            return redirect(url)

    # submit paspaustas pagrindinėje formoje
    if 'submit' in request.POST:
        formset = forms.DataFormset(request.POST)
        if formset.is_valid():
            formset.save()
            url = reverse_lazy('reports:data_table', kwargs={'start_date': start_date, 'end_date': end_date})
            return redirect(url)
    else:
        queryset = models.Data.objects.filter(date__range=(start_date, end_date))
        formset = forms.DataFormset(queryset=queryset)

    helper = forms.DataFormSetHelper()

    filter_form = forms.DateFilterForm(initial={'start_date': start_date, 'end_date': end_date})

    return render(
        request,
        "reports/data_form.html",
        {"formset": formset, 'helper': helper, 'filter_form': filter_form},
    )


@login_required()
def data_table_empty_date(request):
    now = datetime.now()
    return redirect(
        reverse(
            'reports:data_table',
            kwargs={
                'start_date': '{y}-{m:02d}-{d}'.format(y=now.year, m=now.month, d='01'),
                'end_date': '{y}-{m:02d}-{d:02d}'.format(y=now.year, m=now.month, d=monthrange(now.year, now.month)[1]),
            }
        )
    )


@login_required()
def data_table_no_end(request, start_date):
    now = datetime.now()
    return redirect(
        reverse(
            'reports:data_table',
            kwargs={
                'start_date': start_date,
                'end_date': '{y}-{m:02d}-{d:02d}'.format(y=now.year, m=now.month, d=monthrange(now.year, now.month)[1]),
            }
        )
    )


@login_required()
def insert_data(request):
    try:
        inserter(10)
        message = 'ok'
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return render(request, template_name='reports/get_data.html', context={'message': message})

    return redirect(reverse('reports:data_table_empty_date'))


def api_overall(request):

    obj = Overall(models.Data)

    chart = {'first': {
        'xAxis': {'categories': obj.create_categories()},
        'series': obj.create_series()[::-1]
    }}

    return JsonResponse(chart)


def overall(request):
    return render(request, template_name='reports/overall.html', context={})
