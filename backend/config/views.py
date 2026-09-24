import requests
from django.conf import settings
from django.http import JsonResponse

def ai_health_check(request):
    try:
        print("inide try")
        response = requests.get(f"{settings.AI_SERVICE_URL}/health", timeout=5,)
        #check api status
        response.raise_for_status()
        return JsonResponse({
            "backend": "ok",
            "ai_service":response.json(),
        })   
    except requests.RequestException:
        print("error")
        return JsonResponse(
            {
                "backend": "ok",
                "ai_service": "unavailable",
            },
            status=503,)
