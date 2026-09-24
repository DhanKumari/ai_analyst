from django.urls import path
from .views import DatasetUploadAPIView


urlpatterns = [
    path("upload/", DatasetUploadAPIView.as_view(), name = "dataset-upload",)
]