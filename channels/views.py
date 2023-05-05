from django.shortcuts import render


def chat_box(request):
    # we will get the chatbox name from the url
    return render(request, "chatbox.html")
