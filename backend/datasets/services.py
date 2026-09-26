import os
import requests
from django.conf import settings

def profile_dataset(file_path):
    
    # ai_service_url= settings.AI_SERVICE_URL
    url = f"{settings.AI_SERVICE_URL}/profile/"
    with open(file_path, "rb") as file:
        # send file to FASTapi
        response= requests.post(
            url,
            files={
                "file":file
            },
            timeout=60,
        )
    response.raise_for_status()
    return response.json()


