from django.urls import path

from api.views import get_model

urlpatterns = [
    path('models/<slug:version>', get_model, name='api/model')
]
