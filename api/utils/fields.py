from rest_framework import serializers
from django.utils.timezone import localtime

class LocalDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        value = localtime(value)
        return super().to_representation(value)