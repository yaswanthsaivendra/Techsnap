from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from .models import Course, Lessons, Topic, UserCourses, UserLessons, UserTopics
from django.urls import reverse
from accounts.models import Profile
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.contrib.auth.models import User


class CourseListView(ListView):
    model = Course
    template_name = 'courses.html'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'

    def get_context_data(self, *args, **kwargs):
        lesson = self.request.GET.get('lesson')
        context = super(CourseDetailView, self).get_context_data(*args, **kwargs)
        user_topics = UserTopics.objects.filter(user=self.request.user, coursetopic__course__slug=self.kwargs['slug']).order_by('position')
        context['user_topics'] = user_topics
        if lesson:
            lesson_data = get_object_or_404(Lessons, slug=lesson)
            context['lesson_data'] = lesson_data.body
        return context

class TopicDetailView(DetailView):

    def get(self, request, course_slug, slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        topic = get_object_or_404(Topic, slug=slug)
        context = {'object': topic}
        return render(request, 'topic_detail.html', context)

class LessonDetailView(View, LoginRequiredMixin):

    def get(self, request, course_slug, topic_slug, lesson_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        topic = get_object_or_404(Topic, slug=topic_slug)
        lesson = get_object_or_404(Lessons, slug=lesson_slug)
        context = {'object': lesson}
        return render(request, 'lesson_detail.html', context)

@login_required
def course_enroll(request, slug):
    course = get_object_or_404(Course, slug=request.POST.get('slug'))
    profile = get_object_or_404(Profile, user=request.user)
    if request.user.profile in course.users.all():
        return HttpResponseRedirect(reverse('courses:course_detail', kwargs={'slug': course.slug}))
    if request.method=='POST':
        if profile.techsnap_cash >= course.total:
            course.users.add(request.user.profile)
            user_course = get_object_or_404(UserCourses, user=request.user)
            user_course.courses.add(course)
            user_course.save()
            lessons = Lessons.objects.filter(course=course)
            for lesson in lessons:
                UserLessons.objects.create(user=request.user, courselesson=lesson, position=lesson.position)
            topics = Topic.objects.filter(course=course)
            for topic in topics:
                user_topic = UserTopics.objects.create(coursetopic=topic, user=request.user, position=topic.position)
                for lesson in topic.get_topic_lessons():
                    user_lesson = UserLessons.objects.get(user=request.user, courselesson=lesson)
                    user_topic.courselessons.add(user_lesson)
                user_topic.save()
            profile.techsnap_cash = profile.techsnap_cash - course.cost
            profile.save()
            course.save()
            html_message = render_to_string('course_email.html', { 'context': 'You have successfully enrolled to the ' + course.title +' course'})
            plain_msg = strip_tags(html_message)
            send_mail('Welcome to: '+course.title, plain_msg, settings.EMAIL_HOST_USER, [request.user.email], html_message=html_message)
            return HttpResponseRedirect(reverse('dashboard', kwargs={'slug': request.user.profile.slug}))
        else:
            if request.user.is_superuser:
                return HttpResponseRedirect(reverse('courses:buy_techsnap_cash', kwargs={'slug': request.user.profile.slug}))
            else:
                return HttpResponse('You balance is not enough')
    else:
        return render(request, 'payment.html', {'course': course})

@login_required
def payment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.user.profile in course.users.all():
        return HttpResponseRedirect(reverse('courses:course_detail', kwargs={'slug': course.slug}))
    return render(request, 'payment.html', {'course':course})

def buy_techsnap_cash(request, slug):
    if request.user.is_superuser:
        profile = get_object_or_404(Profile, slug=slug)
        if request.method=='POST':
            amount = request.POST['amount']
            profile.techsnap_cash = profile.techsnap_cash + int(amount)
            profile.save()
            html_message = render_to_string('payment_email.html', { 'context': 'You have paid ' + amount})
            plain_msg = strip_tags(html_message)
            send_mail('Payment Successfull', plain_msg, settings.EMAIL_HOST_USER, [request.user.email], html_message=html_message)
            return HttpResponseRedirect(reverse('dashboard', kwargs={'slug': request.user.profile.slug}))
        else:
            return render(request, 'buy.html')
    else:
        return HttpResponse("You don't have access")

def mycourses(request):
    context = {}
    context['mycourses'] = request.user.profile.courseprofile()
    return render(request, 'mycourses.html', context)

def topiComp(request, id, topic_id):
    Lesson = UserLessons.objects.get(user=request.user, id=id)
    topic = get_object_or_404(UserTopics, id=topic_id)
    done = True
    if(Lesson.done == True):
        UserLessons.objects.filter(user=request.user, id=id).update(done = False)
        topic.num_com_lessons -= 1
        topic.save()
        user_profile = get_object_or_404(Profile, user=request.user)
        if user_profile.xp >= Lesson.courselesson.xp:
            user_profile.xp -= Lesson.courselesson.xp
        user_profile.save()
        done = False
    else:
        UserLessons.objects.filter(user=request.user, id=id).update(done=True)
        topic.num_com_lessons += 1
        topic.save()
        user_profile = get_object_or_404(Profile, user=request.user)
        user_profile.xp += Lesson.courselesson.xp
        user_profile.save()
        done=True
    data = {
        'done': done,
    }
    return HttpResponse(JsonResponse(data))


def reflect(request, slug):
    course = get_object_or_404(Course, slug=slug)
    topics = course.get_course_topics()
    lessons = course.get_course_lessons()

    for lesson in lessons:
        if UserLessons.objects.filter(courselesson=lesson).count()==0:
            user_courses = UserCourses.objects.filter(courses__id=lesson.course.id)
            for user_course in user_courses:
                UserLessons.objects.create(user=user_course.user, courselesson=lesson, done=False, position=lesson.position)

    for topic in topics:
        top_les = topic.get_topic_lessons()
        topic.num_lessons = len(top_les)
        top_min_time = 0
        for les in top_les:
            top_min_time += les.min_time
        topic.min_time = top_min_time
        topic.save()
        if UserTopics.objects.filter(coursetopic=topic).count()==0:
            user_courses = UserCourses.objects.filter(courses__id=topic.course.id)
            for user_course in user_courses:
                UserTopics.objects.create(user=user_course.user, coursetopic=topic, position=topic.position)

        user_topics = UserTopics.objects.filter(coursetopic=topic)

        for user_topic in user_topics:
            user_topic.courselessons.clear()
            for lesson in topic.get_topic_lessons():
                user_lesson = UserLessons.objects.get(user=user_topic.user, courselesson=lesson)
                user_topic.courselessons.add(user_lesson)
                user_topic.save()
    return redirect('courses:course_list')

def lesson_data(request, slug):
    lesson = get_object_or_404(Lessons, slug=slug)
    return HttpResponse(JsonResponse({'data': lesson.body}))