from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import tempfile
import os
import pyttsx3
from gtts import gTTS
import subprocess



@login_required(login_url="login")
def HomePage(request):
    if request.method == 'POST':
        text = request.POST.get('home')
        voice = request.POST.get('voice')

        if not text:
            return HttpResponse('No text to speak')

        # Specify the language based on the selected voice
        if voice == 'hindi':
            language = 'hi'
        else:
            language = 'en-in'

        # Convert the text to speech using GTTS
        tts = gTTS(text=text, lang=language)

        # Save the audio to a temporary file
        mp3_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        tts.save(mp3_file.name)
        mp3_file.close()

        # Serve the generated audio file as a response
        with open(mp3_file.name, 'rb') as f:
            audio_data = f.read()
            file_size = os.path.getsize(mp3_file.name)

        # Pass the audio data, file size, language, and voice to the template
        context = {
            'audio_data': audio_data,
            'file_size': file_size,
            'language': language,
            'voice': voice,
        }

        return render(request, 'home.html', context)

    return render(request, 'home.html')
def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if User.objects.filter(username=uname).exists():
            # Handle the case where the username already exists
            return HttpResponse('Username already exists. Please choose a different username.')

        if User.objects.filter(email=email).exists():
            # Handle the case where the email already exists
            return HttpResponse('Email already exists. Please choose a different email address.')

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            # Handle the case where the email format is invalid
            return HttpResponse('Invalid email format. Please enter a valid email address.')

        if pass1 != pass2:
            # Handle the case where the passwords do not match
            return HttpResponse('Passwords do not match. Please enter the same password in both fields.')

        # Create the new user
        my_user = User.objects.create_user(username=uname, email=email, password=pass1)
        my_user.save()
        return redirect('login')  # Redirect to the login page using the URL name

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')

        # Authenticate user
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            # User credentials are valid, log in the user
            login(request, user)
            return redirect('home')  # Redirect to the home page using the URL name
        else:
            # User credentials are invalid
            return HttpResponse('Invalid username or password. Please try again.')

    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect("login")
