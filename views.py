from django.shortcuts import render , redirect 
import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import RegistrationForm
from django.contrib.auth.decorators import login_required
from .models import ProfileForm
from .models import Profile , ExpertProfile , ExpertProfileForm ,Session,SessionForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import Q

from django.shortcuts import render, get_object_or_404
from .models import Resource
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden
import base64
import requests
from django.urls import reverse
from django.conf import settings
from datetime import datetime, timedelta
import json
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user= form.save()
            Profile.objects.create(user=user)
            return redirect('login_view')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print("Username:", username)
        print("Password:", password)
        user = authenticate(request, username=username, password=password)
        print("User exists:", User.objects.filter(username=username).exists())
        if user is not None:
            print(f"Hashed password: {user.password}")
            print("Password is correct:", user.check_password(password))
            print("User is authenticated:", user.is_authenticated)
            login(request, user)
            request.session.set_expiry(604800)
            print("Logged in successfully")
            return redirect('home')
        else:
            print("Invalid credentials")
    return render(request, 'login.html')

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def profile_edit_view(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {'form': form})


@login_required
def delete_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    profile.delete()
    return redirect('home')

def wellness_resources(request):
    return render(request, 'wellness_resources.html')

def expert_connections(request):
    return render(request, 'expert.html')

# wellness/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Resource, Category, Topic, Favorite

def resource_list(request):
    resources = Resource.objects.all()
    query = request.GET.get('q')
    if query:
        resources = resources.filter(title__icontains=query)

    category = request.GET.get('category')
    if category:
        resources = resources.filter(category__name=category)

    topic = request.GET.get('topic')
    if topic:
        resources = resources.filter(topic__name=topic)

    categories = Category.objects.all()
    topics = Topic.objects.all()

    return render(request, 'resources_list.html', {
        'resources': resources,
        'categories': categories,
        'topics': topics,
    })

@login_required
def add_favorite(request, resource_id):
    resource = Resource.objects.get(id=resource_id)
    Favorite.objects.get_or_create(user=request.user, resource=resource)
    return redirect('resource_list')

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorite_list.html', {
        'favorites': favorites,
    })

USDA_API_KEY = 'qXDv5N0CUUPjt7FjxizML7PZafUD7UhA4Fig9qh5'

def fetch_advice(goal):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={goal}&api_key={USDA_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('foods', [])
    else:
        return []

@login_required
def advice_view(request):
    profile = Profile.objects.get(user=request.user)
    advice_list = fetch_advice(profile.wellness_goals)
    return render(request, 'advice.html', {'advice_list': advice_list, 'profile': profile})



@login_required
def create_expert_profile(request):
    if request.method == 'POST':
        form = ExpertProfileForm(request.POST, request.FILES)
        if form.is_valid():
            expert_profile = form.save(commit=False)
            expert_profile.user = request.user  # Set the current user
            expert_profile.save()
            return redirect(reverse('expert_profile_detail', kwargs={'pk': expert_profile.pk}))
        else:
            print(form.errors)  # This will print the form errors to the console
    else:
        form = ExpertProfileForm()

    return render(request, 'create_expert_profile.html', {'form': form})

def edit_expert_profile(request,pk):
    expert_profile = get_object_or_404(ExpertProfile, pk=pk)
    if request.user != expert_profile.user:
        return HttpResponseForbidden("You are not allowed to edit this profile.")
    if request.method == 'POST':
        form = ExpertProfileForm(request.POST, request.FILES, instance=expert_profile )
        if form.is_valid():
            form.save()
            return redirect('expert_profile_detail', expert_profile.id)
    else:
        form = ExpertProfileForm(instance=expert_profile)
    return render(request, 'edit_expert_profile.html', {'form': form , 'expert_profile': expert_profile})

@login_required
def expert_profile(request, expert_id):
    expert_profile = get_object_or_404(ExpertProfile, id=expert_id)
    return render(request, 'expert_profile.html', {'expert_profile': expert_profile})

@login_required
def delete_expert_profile(request, expert_id):
    expert_profile = get_object_or_404(ExpertProfile, id=expert_id, user=request.user)
    expert_profile.delete()
    return redirect('home')  # Redirect to the home page or wherever appropriate after deletion.

@login_required
def book_session(request, expert_id):
    expert = get_object_or_404(ExpertProfile, id=expert_id)
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.expert = expert
            session.save()
            # Add logic to generate Zoom link here
            return redirect('session_detail', session.id)
    else:
        form = SessionForm()
    return render(request, 'book_session.html', {'form': form, 'expert': expert})

@login_required
def session_calendar(request):
    sessions = Session.objects.filter(user=request.user)
    return render(request, 'session_calendar.html', {'sessions': sessions})

@login_required
def session_detail(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    return render(request, 'session_detail.html', {'session': session})


@login_required
def expert_list(request):
    experts = ExpertProfile.objects.all()
    return render(request, 'expert_list.html', {'experts': experts})
@login_required
def expert_profile_detail(request, pk):
    expert_profile = get_object_or_404(ExpertProfile, pk=pk)
    return render(request, 'expert_profile_detail.html', {
        'expert_profile': expert_profile
    })


#chat_area!!!!!!!!!!!
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserRelation, Messages
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from my_app.serializers import MessageSerializer
from django.contrib import messages as django_messages  


@login_required(login_url="login")
def chat(request, username):
    try:
        usersen = request.user
        friend = User.objects.get(username=username)
        exists = UserRelation.objects.filter(
            user=request.user, friend=friend, accepted=True
        ).exists()

        if not exists:
            django_messages.error(
                request, "You are not able to chat with this user."
            )  # Use the renamed variable here
            return redirect("house")
    except User.DoesNotExist:
        return redirect("house")

    messages = Messages.objects.filter(
        sender_name=usersen, receiver_name=friend
    ) | Messages.objects.filter(sender_name=friend, receiver_name=usersen)
    if request.method == "GET":
        return render(
            request,
            "chat.html",
            {
                "messages": messages,
                "curr_user": usersen,
                "friend": friend,
            },
        )


@login_required(login_url="login")
@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == "GET":
        messages = Messages.objects.filter(
            sender_name=sender, receiver_name=receiver, seen=False
        )
        serializer = MessageSerializer(
            messages, many=True, context={"request": request}
        )
        for message in messages:
            message.seen = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@login_required(login_url="login")
def delete_friend(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = request.user
        friend = User.objects.get(username=username)
        try:
            print("starts")
            exists = UserRelation.objects.filter(user=user, friend=friend).exists()
            print("sts")
            if exists:
                pass
            else:
                return HttpResponseRedirect(
                    request.META.get("HTTP_REFERER", reverse("house"))
                )
            user_relation = UserRelation.objects.get(user=user, friend=friend)
            user_relation.delete()

            user_relation_reverse = UserRelation.objects.get(user=friend, friend=user)
            user_relation_reverse.delete()
            messages.success(request, "Friend deleted successfully.")

        except UserRelation.DoesNotExist:
            messages.success(request, "Request deleted successfully.")
            pass
        return redirect("house")
    else:
        return redirect("house")


@login_required(login_url="login")
def accept_request(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = request.user
        friend = User.objects.get(username=username)
        accepted = True

        exists = UserRelation.objects.filter(user=user, friend=friend).exists()
        print("sts")
        if exists:
            return HttpResponseRedirect(
                request.META.get("HTTP_REFERER", reverse("home"))
            )
        user_relation = UserRelation(user=user, friend=friend, accepted=accepted)
        user_relation.save()

        user_relation_revrse = UserRelation.objects.get(user=friend, friend=user)
        user_relation_revrse.accepted = True
        user_relation_revrse.save()
        messages.success(request, "Friend Added successfully.")

        return redirect("house")
    else:
        return redirect("house")


@login_required(login_url="login")
def add_friend(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = request.user
        friend = User.objects.get(username=username)
        accepted = False
        print("starts")
        exists = UserRelation.objects.filter(user=user, friend=friend).exists()
        print("sts")
        if exists:
            print("star")
            return HttpResponseRedirect(
                request.META.get("HTTP_REFERER", reverse("home"))
            )
        user_relation = UserRelation(user=user, friend=friend, accepted=accepted)
        user_relation.save()
        messages.success(request, "Request sended successfully.")

        return redirect("house")
    else:
        return redirect("house")

@login_required(login_url="login")
def search(request):
    query = request.GET.get("q", "")
    
    # Get all active users
    users = User.objects.filter(is_active=True)
    
    # Get all expert profiles
    experts_list = ExpertProfile.objects.filter(user__in=users)

    # If there's a search query, filter the users
    if query:
        users = users.filter(username__icontains=query).order_by('username')
    
    context = {
        "query": query,
        "users": users,
        "experts_list": experts_list,
        "user": request.user.username,
    }

    return render(request, "search.html", context)



@login_required(login_url="login")
def userprofile(request, username):
    if username == request.user.username:
        return redirect("house")
    friend_dict = {}
    request_dict = {}
    friend_dict["accepted"] = False
    request_dict["accepted"] = False
    friend_dict["name"] = ""
    send_request = False
    not_accepted = False
    me_not_accepted = False
    is_friend = False
    try:
        user = User.objects.get(username=username)
        friends_data = UserRelation.objects.all()
        for obj in friends_data:
            if obj.user.username == request.user.username:
                if obj.friend.username == username:
                    friend_dict = {
                        "name": obj.friend.username,
                        "accepted": obj.accepted,
                    }
        for obj in friends_data:
            if obj.friend.username == request.user.username:
                if obj.user.username == username:
                    if obj.accepted:
                        me_not_accepted = False
                    else:
                        me_not_accepted = True

    except User.DoesNotExist:
        messages.error(request, "User does not exist.")
        return render(request, "friend.html")

    if friend_dict["name"] == "":
        if me_not_accepted == True:
            print("me not accepted")
        else:
            print("not a friend")
            send_request = True

    elif friend_dict["accepted"] == False:
        print("not_accepted")
        not_accepted = True

    else:
        print("friend")
        is_friend = True
    print("send_request = ", send_request)
    print("not_accepted = ", not_accepted)
    print("me_not_accepted = ", me_not_accepted)
    print("is_friend = ", is_friend)
    # You can now access user details, such as username, email, etc.
    user_details = {
        "username": user.username,
        "email": user.email,
        "send_request": send_request,
        "not_accepted": not_accepted,
        "is_friend": is_friend,
        "me_not_accepted": me_not_accepted,
    }

    return render(request, "friend.html", {"user_details": user_details})


@login_required(login_url="login")
def house(request):
    friends_data = UserRelation.objects.all()
    friends_list = []
    for obj in friends_data:
        if obj.user.username == request.user.username:
            friend_dict = {"username": obj.friend.username, "accepted": obj.accepted}
            friends_list.append(friend_dict)

    request_list = []
    for obj in friends_data:
        if obj.friend.username == request.user.username:
            if not obj.accepted:
                request_dict = {"username": obj.user.username}
                request_list.append(request_dict)

    data = {
        "email": request.user.email,
        "username": request.user.username,
        "friends": friends_list,
        "requests": request_list,
    }
    return render(
        request,
        "chat_home.html",
        {
            "data": data,
        },
    )


@login_required(login_url="login")
def EditProfile(request):
    success_message = None
    error_message = None

    if request.method == "POST":
        new_email = request.POST.get("email")
        new_username = request.POST.get("username")

        # Check if the new username is already taken
        if (
            new_username != request.user.username
            and User.objects.filter(username=new_username).exists()
        ):
            error_message = "Username already exists. Please choose a different one."
        elif (
            new_email != request.user.email
            and User.objects.filter(email=new_email).exists()
        ):
            error_message = "Email address already associated with another account. Please choose a different one."
        else:
            # Update email and username
            # print(request.user.id)
            request.user.email = new_email
            request.user.username = new_username
            request.user.save()
            success_message = "Profile updated successfully."

    # Pre-fill the form with the user's existing data
    initial_data = {
        "email": request.user.email,
        "username": request.user.username,
    }

    return render(
        request,
        "edit.html",
        {
            "initial_data": initial_data,
            "success_message": success_message,
            "error_message": error_message,
        },
    )

