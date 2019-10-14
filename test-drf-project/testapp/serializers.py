from rest_framework import serializers

from .models import TestModel


class TestSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ("name",)
