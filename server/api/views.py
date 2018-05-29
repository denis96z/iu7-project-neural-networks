from django.http import JsonResponse
from django.views.decorators.http import require_GET

from api.models import NeuralNetworkModel
from api.serializers import NeuralNetworkModelSerializer
from api.settings import DJANGORESIZED_DEFAULT_SIZE


@require_GET
def get_model(request, version):
    if version == 'latest':
        model = NeuralNetworkModel.objects.first()
    else:
        try:
            version = version.replace('-', '.')
            model = NeuralNetworkModel.objects.get(version=version)
        except NeuralNetworkModel.DoesNotExist:
            model = None
    if model is None:
        response = {'error': 'model not found'}
        return JsonResponse(response, status=404)
    else:
        serializer = NeuralNetworkModelSerializer(model)
        return JsonResponse(serializer.data)
