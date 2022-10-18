from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer


class SensorView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def post(self, request):
        if request.data and request.data.get('name'):
            sensor = Sensor.objects.create(**request.data)
            return Response({'id': sensor.pk, 'name': sensor.name, 'description': sensor.description})
        else:
            return Response({'error': "'name' required"})


class SensorDetailView(RetrieveAPIView, UpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

    def patch(self, request, pk):
        if request.data:
            try:
                sensor = Sensor.objects.get(id=pk)
                if request.data.get('name'):
                    sensor.name = request.data.get('name')
                if request.data.get('description'):
                    sensor.description = request.data.get('description')
                sensor.save()
                return Response({'id': sensor.pk,
                                 'name': sensor.name,
                                 'description': sensor.description})
            except ObjectDoesNotExist:
                return Response({'error': 'Sensor does not exist'})
        else:
            return Response({'error': "'description' or 'name' required"})


class MeasurementView(ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def post(self, request):
        if not request.data.get('sensor_id'):
            return Response({'error': "''sensor_id' required'"})
        try:
            sensor = Sensor.objects.get(id=request.data.get('sensor_id'))
            request.data['sensor_id'] = sensor
        except ObjectDoesNotExist:
            return Response({'error': 'Sensor does not exist'})

        if request.data:
            measurement = Measurement.objects.create(**request.data)
            return Response({'sensor_id': measurement.sensor_id.pk,
                             'temperature': measurement.temperature,
                             'created_at': measurement.created_at})
        else:
            return Response({'error': 'Invalid request'})
