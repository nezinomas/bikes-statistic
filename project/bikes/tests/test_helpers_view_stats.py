from datetime import datetime, timedelta

import pandas as pd
import pandas.api.types as ptypes
import pytest

from ...core.factories import (ComponentFactory, ComponentStatisticFactory,
                               DataFactory)
from ..helpers.view_stats_helper import Filter as T

pytestmark = pytest.mark.django_db


@pytest.fixture(scope='module', autouse=True)
def components(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        ComponentFactory()


@pytest.fixture(scope='module', autouse=True)
def components_statistic(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        ComponentStatisticFactory()


@pytest.fixture(scope='module', autouse=True)
def data(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        d1 = DataFactory(date=datetime(2000, 1, 1).date())
        d2 = DataFactory(date=datetime(2000, 1, 31).date())
    yield
    with django_db_blocker.unblock():
        d1.delete()
        d2.delete()


def test_get_df():
    actual = T('bike', 1)._Filter__df

    assert 2 == len(actual)

    assert 'date' in actual.columns
    assert 'distance' in actual.columns

    assert ptypes.is_datetime64_dtype(actual['date'])
    assert ptypes.is_float_dtype(actual['distance'])


def test_get_components():
    actual = [*T('bike', 1)._Filter__components]

    assert 1 == len(actual)
    assert 'Component' == actual[0].name


def test_get_components_foreign_key_object():
    obj = T('bike', 1)._Filter__components
    actual = obj[0].components.all()

    assert 1 == len(actual)
    assert 'bike / Component / 2000-01-01 ... 2000-12-31' == str(actual[0])


def test_total_distance_one_month():
    actual = T('bike', 1).total_distance()

    assert 30 == actual


def test_total_distance_one_day():
    actual = T('bike', 1).total_distance('2000-01-01', '2000-01-01')

    assert 10 == actual

