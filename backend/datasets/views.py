from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DatasetUploadSerializer
# Create your views here.
class DatasetUploadAPIView(APIView):
    parser_classes =[MultiPartParser, FormParser]

    def post(self, request):
        serializer = DatasetUploadSerializer(data = request.data)
        if serializer.is_valid():
            dataset = serializer.save()
            return Response(
                {"message":"dataset Uploaded Successfully!"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST,
        )