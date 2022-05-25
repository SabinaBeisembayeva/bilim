from django.shortcuts import render
from django.db.models import query
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import serializers, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
# Create your views here.

class BookingView(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    
    @action(detail=False, methods=['post'])
    def test(self, request):
        return 200