from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib import messages
from .form import EventForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json
from django.contrib.auth import logout as auth_logout


def login(request):
    if request.user.is_authenticated:
        return redirect('show_calendar')
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def add_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_date"]
        end_time = form.cleaned_data["end_date"]
        location = form.cleaned_data["location"]
        college = form.cleaned_data["college"]
        category = form.cleaned_data["category"]
        created_by = request.user
        print(category,'sssssssssssssssssssssssss')

        event = Event.objects.create(title=title, description=description, 
                                     start_date=start_time, 
                                     end_date=end_time, location=location, 
                                     college=college,created_by=created_by)
        event.category.set(category)
        event.save()
        messages.success(request, 'event added successfully!')
        return redirect('show_calendar')

@login_required 
def show_calendar(request):
    user = request.user
    print(user,"uuuuuuuuuuuuuuuuuuu")
    user_events = Event.objects.filter(created_by=user)
    colab_events = Colabrations.objects.filter(colabrator=user)
    event_list = []
    for colab_event in colab_events:
        event_list.append({
                    "id": colab_event.event.id,
                    "title": colab_event.event.title,
                    "description": colab_event.event.description,
                    "start": colab_event.event.start_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": colab_event.event.end_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    "location": colab_event.event.location,
                    "college": colab_event.event.college,
                    "category": ", ".join(category.name for category in colab_event.event.category.all())
                })
        print(event_list,"wwwwwwwwwwwwwwwwwwwwww")

    form = EventForm()
    for eve in user_events:
        if eve.is_disabled == False:
            event_list.append(
                {
                    "id": eve.id,
                    "title": eve.title,
                    "description": eve.description,
                    "start": eve.start_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": eve.end_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    "location": eve.location,
                    "college": eve.college,
                    "category": ", ".join(category.name for category in eve.category.all())
                }
            )
    return render(request, 'home.html', {'events': event_list, 'form': form})
# Create your views here.

@login_required
def delete_event(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.is_disabled = True
        event.save()
        return JsonResponse({'message': 'Event deleted Successfully.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

@login_required
def add_collaborators(request):
    events = Event.objects.filter(created_by=request.user)
    print(events,"lllllllllllllllllllll")
    users = User.objects.exclude(id=request.user.id)
    access_levels=AccessLevels.objects.all()
    context = {
        'events': events,
        'users': users,
        'access_levels': access_levels
    }
    if request.method == 'POST':
        event_id = request.POST.get('event')
        user_id = request.POST.get('user')
        access_level = request.POST.get('access')
        print(event_id,"oooooooooooooo")
        if event_id=='None' or user_id=='None' or access_level=='None':
            messages.warning(request, 'Error! Please fill all fields.')
            return redirect('add_collaborators')  
        else:
            Colabration = Colabrations.objects.create(colabrator_id=user_id, event_id=event_id,
                                                    created_by=request.user,created_at=timezone.now())
            Colabration.access_levels.set(access_level)
            Colabration.save()
            messages.success(request, 'User Permission added successfully!')
            return redirect('add_collaborators')
            
    return render(request, 'add_collaborators.html',context)
