from django.shortcuts import render, redirect
from .models import Room, Message
from django.http import HttpResponse, JsonResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username') #Accessing the username from the url
    room_details = Room.objects.get(name=room) #getting the chatroom which has the name of room
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else: # if room doesn't exist, create a new room
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_msg = Message.objects.create(value=message, user=username, room=room_id)
    new_msg.save()
    # We're not rendering any html page. We just want to return the message back to the front-end/javascript
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    # We want to get messages of that particular room the user is in. When we get all the messages of the room, we're gonna return a JSON response of all the messages. Then from our front-end we're gonna use Ajax to access that JSON response and showcase it to the user
    room_details = Room.objects.get(name=room) #getting the chatroom which has the name of room
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({'messages':list(messages.values())}) #messages.values()- we're getting all the values from messages