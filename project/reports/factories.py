from datetime import datetime
from factory import DjangoModelFactory, SubFactory

from ..bikes.models import Bike
from .models import Data


class BikeFactory(DjangoModelFactory):
    class Meta:
        model = Bike

    full_name = 'xbike'
    short_name = 'xbike'
    date = datetime(1970, 1, 1).date()


class DataFactory(DjangoModelFactory):
    class Meta:
        model = Data

    bike = SubFactory(BikeFactory)
