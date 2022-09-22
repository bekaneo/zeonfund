from rest_framework import serializers
from  .models import Images, Case


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(CaseSerializer, self).to_representation(instance)
        if instance.images.exists():
            representation['images'] = ImageSerializer(instance.images.all(),
                                                       many=True).data


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'
