from django.shortcuts import render
from django.http import FileResponse, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json
import requests
from decouple import config

totMailCount = 0


def fetchDetails(messageId):
    access_token = config('API_KEY')
    print(access_token)
    message_url = f'https://api.nylas.com/messages/{messageId}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(message_url, headers=headers).json()
    print(response)
    dataDict = {}
    dataDict['email'] = response['from'][0]['email']
    dataDict['threadId'] = response['thread_id']
    dataDict['subject'] = response['subject']
    dataDict['body'] = response['snippet']

    # print( dataDict)
    return dataDict


def sendReply(data, messageId):
    access_token = config('API_KEY')
    messages_url = 'https://api.nylas.com/send'

    thread_id = data['threadId']
    subject = data['subject']
    email_id = data['email']
    body = data['body']
    payload = {
        'thread_id': thread_id,
        'reply_to_message_id': messageId,
        'subject': f'RE: {subject}',
        'body': f'Reply for Subject: {subject} and body: {body} to {email_id}',
        'to': [{'email': email_id}]
    }
    headers = {'Authorization': f'Bearer {access_token}',
               'Content-Type': 'application/json'}
    response = requests.post(
        messages_url, headers=headers, json=payload).json()
    return response


def replyToEmail(messageId, threadId):
    print("Data fetching started")
    data = fetchDetails(messageId)
    if data['email'] == config('Email_Nylas'):
        return 0
    global totMailCount
    totMailCount += 1
    print("Data fetching ended")
    response_data = sendReply(data, messageId)
    return response_data


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
        messageId = delta['object_data']['id']
        threadId = delta['object_data']['attributes']['thread_id']

        if typeOfDelta == 'message.created':

            print("Replying Started")
            responseData = replyToEmail(messageId, threadId)
            print(responseData)
            print("Replying Ended")

        response_data = {
            'data': data,
            'replied': 'success',
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
