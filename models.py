from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.widgets import DateTimeInput
from django.db.models import Q
import uuid
from django.utils import timezone
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash password
        if commit:
            user.save()
        return user

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pictures' )
    wellness_goals = models.CharField(max_length=255)
    is_online = models.BooleanField(default = False)


    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture', 'wellness_goals')

 


from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'resource')

# models.py
from django.db import models
from django.contrib.auth.models import User

class ExpertProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=255)
    expert_email = models.EmailField()
    expert_phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='profile_pictures' )
    expertise = models.CharField(max_length=255)

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    expert = models.ForeignKey(ExpertProfile, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    confirmed = models.BooleanField(default=False)
    zoom_link = models.URLField(blank=True, null=True)

class Communication(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='communications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    # Add other fields as needed

class ExpertProfileForm(forms.ModelForm):
    class Meta:
        model = ExpertProfile
        fields = ['name','bio' , 'expert_email' , 'expert_phone', 'image' , 'expertise']  

class SessionForm(forms.ModelForm):
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    class Meta:
        model = Session
        fields = ['start_time', 'end_time']


class UserRelation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_relations"
    )
    friend = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friend_relations", default=None
    )
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"


class Messages(models.Model):
    description = models.TextField()
    sender_name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender"
    )
    receiver_name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    time = models.TimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        ordering = ("timestamp",)
