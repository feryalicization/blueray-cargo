# serializers.py
from rest_framework import serializers
from .models import Country, Category, Destination
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


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




class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = get_user_model().objects.filter(email=email).first()

            if user:
                if not user.check_password(password):
                    raise serializers.ValidationError('Invalid password')
            else:
                raise serializers.ValidationError('User not found')

        else:
            raise serializers.ValidationError('Must include "email" and "password"')

        attrs['user'] = user
        return attrs