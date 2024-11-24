from rest_framework import serializers

from apps.xmodel.models.xmodel import XModel

class XModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = XModel
    fields = '__all__'

  