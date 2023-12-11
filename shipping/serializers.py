# serializers.py
from rest_framework import serializers
from .models import Country, Category, Destination
from django.contrib.auth.models import User


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name', 'country_flag', 'country_currency']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'country', 'category_title', 'price_per_kilo']



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
        )
        return user
        
    

class DesinasiFilterSerializer(serializers.Serializer):
    search = serializers.CharField(required=False)



class CalculateFreightRequestSerializer(serializers.Serializer):
    country_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    destination_id = serializers.IntegerField()
    weight = serializers.FloatField()
