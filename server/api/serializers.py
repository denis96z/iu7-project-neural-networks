from rest_framework import serializers, viewsets, routers

from api.models import NeuralNetworkModel


class NeuralNetworkModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NeuralNetworkModel
        fields = '__all__'
        depth = 1


class NeuralNetworkModelViewSet(viewsets.ModelViewSet):
    queryset = NeuralNetworkModel.objects.all()
    serializer_class = NeuralNetworkModelSerializer


router = routers.DefaultRouter()
router.register(r'models', NeuralNetworkModelViewSet)
