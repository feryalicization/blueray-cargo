from rest_framework import generics
from .models import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CountryFilter, CategoryFilter
import requests
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from django.db.models import F
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token




class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': f'Token {token.key}'
        })
    

class CountryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CountryFilter
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]  


class CountryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated] 



class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated] 


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated] 


# ==========================================================================

class CalculateFreight(APIView):
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated] 
    @swagger_auto_schema(request_body=CalculateFreightRequestSerializer)
    def post(self, request, *args, **kwargs):
        serializer = CalculateFreightRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        country_id = serializer.validated_data['country_id']
        category_id = serializer.validated_data['category_id']
        destination_id = serializer.validated_data['destination_id']
        weight = serializer.validated_data['weight']

        country = get_object_or_404(Country, id=country_id)
        category = get_object_or_404(Category, id=category_id)

        international_price = float(weight * float(category.price_per_kilo)) 
        weight_g = int(weight * 1000)

        url = 'https://api.rajaongkir.com/starter/cost'
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'key': settings.RAJAONGKIR_API_KEY,
        }

        payload = {
            'origin': '501', 
            'destination': destination_id,
            'weight': weight_g,
            'courier': 'jne',
        }
     
        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            api_response = response.json()

            desired_service = 'REG' 

            shipping_costs = api_response['rajaongkir']['results'][0]['costs']
            desired_cost = next((cost['cost'][0]['value'] for cost in shipping_costs if cost['service'] == desired_service), None)
                    
            response_data = {
                'origin': country.country_name,
                'destination': api_response['rajaongkir']['destination_details']['city_name'],
                'category_name': category.category_title,
                'international_price': international_price,
                'domestic_price': desired_cost,
                'total_price': desired_cost + international_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            error_data = {
                'error': 'Failed to retrieve shipping costs from RajaOngkir API',
                'status_code': response.status_code,
            }
            return Response(error_data, status=response.status_code)






class DesinasiView(APIView):
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated] 
    @swagger_auto_schema(query_serializer=DesinasiFilterSerializer)
    def get(self, request, *args, **kwargs):
        url = 'https://api.rajaongkir.com/starter/city'
        headers = {'key': settings.RAJAONGKIR_API_KEY}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            results = data.get('rajaongkir', {}).get('results', [])
            
            serializer = DesinasiFilterSerializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)
            search_term = serializer.validated_data.get('search', '')

            filtered_results = [result for result in results if search_term.lower() in result.get('city_name', '').lower()]

            return Response(filtered_results, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Unable to fetch province data'}, status=response.status_code)