from django.shortcuts import render, get_object_or_404, redirect
from .models import Hashtag, Feedback
from accounts.models import Profile
# from events.models import Event
from .forms import FeedbackForm

# # Create your views here.


def home(request, hashtag):
    form = FeedbackForm()
    hashtag = get_object_or_404(Hashtag, title=hashtag)
    user_profile = Profile.objects.get(user=request.user)
    queryset = user_profile.hashtags.filter(id=hashtag.id)
    follow=False
    if queryset:
        follow=True
#     events = Event.objects.filter()
    return render(request, 'hashtags/hashtag.html', {'hashtag':hashtag, 'follow':follow, 'form' : form})
    # return render(request, 'hashtags/hashtag.html', {'hashtag':hashtag, 'follow':follow})


def follow(request, hashtag):
    hashtag = get_object_or_404(Hashtag, title=hashtag)
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        queryset = user_profile.hashtags.filter(title=hashtag.title)
        if queryset:
            user_profile.hashtags.remove(hashtag)
            hashtag.followers -= 1
        else:
            user_profile.hashtags.add(hashtag)
            hashtag.followers += 1
        hashtag.save()
        return redirect('hashtags:home', hashtag)

def follow_dash(request, hashtag):
    hashtag = get_object_or_404(Hashtag, title=hashtag)
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        queryset = user_profile.hashtags.filter(title=hashtag.title)
        if queryset:
            user_profile.hashtags.remove(hashtag)
            hashtag.followers -= 1
        else:
            user_profile.hashtags.add(hashtag)
            hashtag.followers += 1
        hashtag.save()
        return redirect('topics', hashtag)

def feedback(request, hashtag):
    hashtag = get_object_or_404(Hashtag, title=hashtag)
    if request.method == "POST":
        Feedback.objects.create(text = request.POST['text'], hashtag=hashtag)
        return redirect('hashtags:home' , hashtag)            

    