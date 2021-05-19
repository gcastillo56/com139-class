from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response

from .models import COVIDData
from .serializers import StateSexSerializer, StateSexAgeSerializer

import pandas as pd
# Create your views here.


def index(request):
    my_json = '[ { "region": "East", "fruit": "Apples", "count": "53245" }, { "region": "West", "fruit": ' \
                 '"Apples", "count": "28479" }]'
    context = {'data_json':my_json}
    return render(request, 'covid_app/donut.html', context)


def pie_chart(request):
    data = COVIDData.objects.all()
    covid_df = pd.DataFrame.from_records(data)
    my_json = '[ { "region": "East", "fruit": "Apples", "count": "53245" }, { "region": "West", "fruit": ' \
                 '"Apples", "count": "28479" }]'
    context = {'data_json':my_json}
    return render(request, 'covid_app/donut.html', context)


class StateSexSet(viewsets.ModelViewSet):
    queryset = COVIDData.objects.all()
    serializer_class = StateSexSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_fields = ['entidad_res', 'municipio_res']


class StateSexAgeSet(viewsets.ViewSet):
    queryset = COVIDData.objects.all()
    serializer_class = StateSexAgeSerializer

    def list(self, request, *args, **kwargs):
        age = request.GET['age']
        covid_df = pd.DataFrame.from_records(COVIDData.objects.filter(edad__gt=age). \
                                             values('id_registro', 'sexo', 'entidad_res', 'municipio_res', 'edad'))
        df = covid_df["sexo"].value_counts()
        print(df)
        return Response(str(covid_df.to_json(orient='records')))
