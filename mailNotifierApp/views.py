from django.shortcuts import render
from django.http import FileResponse, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json


@csrf_exempt
def index(request):
    return render(request, "mailNotifierApp/index.html")


@csrf_exempt
def callApi(request):
    data = {}
    response_data = {}
    if (request.method == 'POST'):
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        response_data = {
            'data': data,
            'status': 'success',

        }

    return JsonResponse(response_data)
