from django.shortcuts import render, get_object_or_404, redirect
from .models import Hashtag, Feedback
# from events.models import Event
# from .forms import FeedbackForm

# # Create your views here.


# def home(request, hashtag):
#     form = FeedbackForm()
#     hashtag = get_object_or_404(Hashtag, title=hashtag)
#     user_profile = Profile.objects.get(user=request.user)
#     queryset = user_profile.hashtags_followed.all().filter(title=hashtag.title)
#     follow=False
#     if queryset:
#         follow=True
#     events = Event.objects.filter()
#     return render(request, 'hashtags/home.html', {'hashtag':hashtag, 'follow':follow, 'form' : form})


# def follow(request, hashtag):
#     hashtag = get_object_or_404(Hashtag, title=hashtag)
#     user_profile = Profile.objects.get(user=request.user)
#     if request.method == 'POST':
#         queryset = user_profile.hashtags_followed.all().filter(title=hashtag.title)
#         if queryset:
#             user_profile.hashtags_followed.remove(hashtag)
#         else:
#             user_profile.hashtags_followed.add(hashtag)
#         return redirect('hashtags:home', hashtag)

# def feedback(request, hashtag):
#     hashtag = get_object_or_404(Hashtag, title=hashtag)
#     if request.method == "POST":
#         Feedback.objects.create(text = request.POST['text'], hashtag=hashtag)
#         return redirect('hashtags:home' , hashtag)            

    