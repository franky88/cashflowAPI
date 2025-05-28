from rest_framework import serializers
from .models import Transaction, CalendarEvent, PettyCash, Bill, Sale
from .utils.fields import LocalDateTimeField

class BaseModelSerializer(serializers.ModelSerializer):
    def build_standard_field(self, field_name, model_field):
        field_class, field_kwargs = super().build_standard_field(field_name, model_field)
        if field_class == serializers.DateTimeField:
            field_class = LocalDateTimeField
        return field_class, field_kwargs

class TransactionSerializer(BaseModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

        read_only_fields = ('created_at',)
        extra_kwargs = {
            'title': {'required': True},
            'amount': {'required': True},
            'transaction_type': {'required': True},
            'date': {'required': True},
            'category': {'required': True},
        }

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return data
    
class CalendarEventSerializer(BaseModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = '__all__'

        read_only_fields = ('created_at',)
        extra_kwargs = {
            'title': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
            'description': {'required': False},
            'all_day': {'required': False},
            'user': {'required': False},
        }

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data
    
class PettyCashSerializer(BaseModelSerializer):
    class Meta:
        model = PettyCash
        fields = '__all__'

        read_only_fields = ('created_at', 'control_number')
        extra_kwargs = {
            'name': {'required': True},
            'amount': {'required': True},
            'date': {'required': True},
            'description': {'required': False},
            'isApproved': {'required': False},
        }

class BillSerializer(BaseModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'

        read_only_fields = ('created_at',)
        extra_kwargs = {
            'title': {'required': True},
            'amount': {'required': True},
            'due_date': {'required': True},
            'description': {'required': False},
            'is_paid': {'required': False},
        }

    # def validate(self, data):
    #     if data['amount'] <= 0:
    #         raise serializers.ValidationError("Amount must be greater than zero.")
    #     return data
    
class SaleSerializer(BaseModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

        read_only_fields = ('created_at',)
        extra_kwargs = {
            'title': {'required': True},
            'amount': {'required': True},
            'sale_date': {'required': True},
            'description': {'required': False},
        }

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return data