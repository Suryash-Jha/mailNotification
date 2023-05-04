from django.shortcuts import render
from django.http import FileResponse, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json

totMailCount = 0


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
        delta = data['deltas'][0]
        typeOfDelta = delta['type']
        if typeOfDelta == 'message.created':
            global totMailCount
            totMailCount += 1

        response_data = {
            'data': data,
            'status': 'success',

        }

    return JsonResponse(response_data)


@csrf_exempt
def clientApi(request):
    if request.method == 'GET':
        return JsonResponse({'status': 'success', 'count': totMailCount})


# {'deltas': [
#     {'date': 1683222145, 'object': 'message', 'type': 'message.created', 'object_data': {'namespace_id': '53egjzdr5nnhnrnztgpwswjbr', 'account_id': '53egjzdr5nnhnrnztgpwswjbr', 'object': 'message', 'attributes': {'thread_id': 'bui5b7061388dljl6c8ukvyd8', 'received_date': 1683222125}, 'id': 'edm9zwql22p14mpd22iczts2i', 'metadata': None}}]
#  }
