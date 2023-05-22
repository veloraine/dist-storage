from .models import *
from rest_framework import serializers

class FileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')

    class Meta:
        model = File
        fields = ['id','name', 'uploaded_at']


    def get_name(self, obj):
        return obj.uploaded_file.name