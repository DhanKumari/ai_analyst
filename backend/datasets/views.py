from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import profile_dataset


from .serializers import DatasetUploadSerializer
# Create your views here.
class DatasetUploadAPIView(APIView):
    parser_classes =[MultiPartParser, FormParser]

    def post(self, request):
        serializer = DatasetUploadSerializer(data = request.data)
        if serializer.is_valid():
            dataset = serializer.save()

            try:
                # Get teh path of the saved excel file
                file_path = dataset.file.path
                result = profile_dataset(file_path)

                profile = result["profile"]

                # save the profile in PostgresSQL
                dataset.profile =profile
                dataset.row_count =profile["row_count"]
                dataset.column_count = profile["column_count"]
                dataset.save()
                return Response(
                    {
                        "message": "Dataset uploaded and profiled successfully!",
                        "profile": profile,
                    },
                    status=status.HTTP_201_CREATED,
                )
                    
            except Exception as e:

                #FastAPI/Pandas processing failed
                dataset.status ="failed"
                dataset.save(update_fields=["status"])
                
                return Response(
                    {
                        "message": "Dataset uploaded, but profiling failed.",
                        "error": str(e),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )



            # return Response(
            #     {"message":"dataset Uploaded Successfully!"},
            #     status=status.HTTP_201_CREATED,
            # )

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST,
        )