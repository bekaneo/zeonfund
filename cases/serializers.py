from rest_framework import serializers
from .models import Images, Case, Categories


class CaseSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    case = serializers.ReadOnlyField()

    class Meta:
        model = Case
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.images.exists():
            images = ImageSerializer(instance.images.all(),
                                     many=True)
            representation['images'] = images.data
        return representation


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'

    def get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = self.get_image_url(instance)
        return representation


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
