from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from .models import DatasetModel

class DatasetUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=["xlsx", "xls"]
            )
        ]
    )
    class Meta:
        model= DatasetModel
        fields="__all__"
        #client should not be able to send:
        read_only_fields=[
            "id",
            "status",
            "row_count",
            "column_count",
            "created_at",
            "updated_at",
        ]