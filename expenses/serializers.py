from rest_framework import serializers
from .models import User, Expense, ExpenseParticipant

class UserSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits = 10, decimal_places= 2 , read_only = True)
    class Meta:
        model = User
        fields =  ['id', 'user_id', 'name', 'email', 'mobile_number', 'balance']

class ExpenseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseParticipant
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    participants = ExpenseParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Expense
        fields = '__all__'
