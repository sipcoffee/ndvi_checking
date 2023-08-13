from .models import FileUpload
from rest_framework import serializers


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = [
            'nameRaster',
            'rasterImage',
            'fileEdited'
        ]