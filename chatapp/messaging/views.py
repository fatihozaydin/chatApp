from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, MessageForm
from .models import Message

def home(request):
    return render(request, 'messaging/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('incoming_messages')
    else:
        form = UserRegisterForm()
    return render(request, 'messaging/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('incoming_messages')
    else:
        form = AuthenticationForm()
    return render(request, 'messaging/login.html', {'form': form})

@login_required
def incoming_messages(request):
    messages = Message.objects.filter(recipient=request.user, is_deleted=False)
    return render(request, 'messaging/incoming_messages.html', {'messages': messages})

@login_required
def sent_messages(request):
    messages = Message.objects.filter(sender=request.user, is_deleted=False)
    return render(request, 'messaging/sent_messages.html', {'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('sent_messages')
    else:
        form = MessageForm()
    return render(request, 'messaging/send_message.html', {'form': form})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        if message.sender == request.user or message.recipient == request.user:
            message.is_deleted = True
            message.save()
        return redirect('incoming_messages' if message.recipient == request.user else 'sent_messages')
    return render(request, 'messaging/confirm_delete.html', {'message': message})

def logout_view(request):
    logout(request)
    return redirect('home')
