from django.shortcuts import render, redirect
from course.models import *
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import auth, User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from accounts.models import Profile
from course.forms import *


def index(request):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    return render(request, 'course/index.html', {'student': profile})

def logout(request):
    auth.logout(request)
    return redirect('index')

def course_list(request):
    cr_list = Course.objects.filter(archive=False, released=True)
    return render(request, 'course/course_list.html', {'courses': cr_list})

def course_description(request, slug):
    profile = Profile.objects.get(user=request.user)
    user = profile
    enrolled = False
    update_available = False
    course = Course.objects.get(slug__iexact=slug)
    description = Description.objects.filter(course=course).first()
    what_u_get = WhatYouGet.objects.filter(description=description)
    testimonials = Testimonial.objects.filter(course=course)
    faqs = FrequentlyAskedQuestion.objects.filter(course=course)
    if len(UserCourseMap.objects.filter(course=course, user=user))>0:
        enrolled = True
        if UserCourseMap.objects.filter(course=course, user=user).first().version<course.version:
            update_available = True 
        
    units = Unit.objects.filter(course=course)
    contents = []
    for unit in units:
        lessons = UserLessonCompletion.objects.filter(user=user, lesson__unit=unit).values_list(
                'lesson__title', 'lesson__duration_Seconds', 'lesson__duration_Minutes', 'lesson__xp'
        )
        total_xp = 0
        for lesson in lessons:
            total_xp = total_xp + lesson[2]

        content = {
            'unit': unit, 
            'lessons': lessons, 
            'length': len(lessons),
            'total_xp': total_xp
        }
        contents.append(content)

    data = {
        'course': course,
        'enrolled': enrolled,
        'update_available': update_available,
        'description': description,
        'whatuget_points': what_u_get,
        'contents': contents,
        'testimonials': testimonials,
        'faqs': faqs
    }

    return render(request, 'course/course-intro.html', data)

def get_total_lessons(course=None, unit=None):
    if unit:
        return len(Lesson.objects.filter(unit=unit))
    num = 0
    for unit in Unit.objects.filter(course=course):
        num += len(Lesson.objects.filter(unit=unit))
    return num

def enroll_in_course(request, slug):
    profile = Profile.objects.get(user=request.user)
    user = profile
    course = Course.objects.get(slug__iexact=slug)
    # Enrollement
    if len(UserCourseMap.objects.filter(user=user, course=course))==0:
        user_course_map = UserCourseMap.objects.create(user=user, course=course)
    lesson_slug = "no-slug"
    #update_userlesson_completion(course, user)
    if not UserLessonCompletion.objects.filter(lesson__unit__course=course, user=user).exists():
        for lesson in Lesson.objects.filter(unit__course=course):
            time_left_min = lesson.duration_Minutes
            time_left_sec = lesson.duration_Seconds
            # previous lesson
            pre_lesson = None
            if lesson.order>1:
                pre_lesson = UserLessonCompletion.objects.get(user=user, lesson__unit__course=course, lesson__order=lesson.order-1)
            unlocked = False
            if time_left_min<=0 and time_left_sec<=0:
                unlocked=True
            elif pre_lesson and pre_lesson.timer_min_left<=0 and pre_lesson.timer_sec_left<=0:
                unlocked = True
            UserLessonCompletion.objects.create(user=user, lesson=lesson,
                                                timer_min_left=time_left_min,
                                                timer_sec_left=time_left_sec, unlocked=unlocked)
    
    lesson = Lesson.objects.filter(unit__course=course).first()

    if not Rating.objects.filter(course=course):
        Rating.objects.create(course=course)
    if lesson:
        complesson = UserLessonCompletion.objects.get(lesson=lesson, user=user)
        complesson.unlocked = True
        complesson.save(update_fields=['unlocked'])
        lesson_slug = lesson.slug

    # Creating log
    log = f" LOGGED IN to Course [{course.course_title}]"
    EnrollmentHistory.objects.create(user=user, log=log, course=course)

    return redirect('lesson-view', slug=lesson_slug, course_slug=course.slug)

def update_course(request, slug):
    user = Profile.objects.get(user=request.user)
    course = Course.objects.get(slug__iexact=slug)
    update_userlesson_completion(course, user)
    user_course_map = UserCourseMap.objects.get(course=course, user=user)
    user_course_map.version = course.version
    user_course_map.save(update_fields=["version"])
    return redirect('course-description', slug=slug)

def update_userlesson_completion(course, user):
    id_list = []
    user_course_map = UserCourseMap.objects.get(user=user, course=course)
    for user_lesson in UserLessonCompletion.objects.filter(user=user, lesson__unit__course=course):
        id_list.append(user_lesson.lesson.id)
    for lesson in Lesson.objects.filter(unit__course=course).exclude(id__in=id_list):
        time_left_min = lesson.duration_Minutes
        time_left_sec = lesson.duration_Seconds
        # previous lesson
        pre_lesson = UserLessonCompletion.objects.get(user=user, lesson__unit__course=course, lesson__order=lesson.order-1)
        unlocked = False
        if time_left_min<=0 and time_left_sec<=0:
            unlocked=True
        elif pre_lesson.timer_min_left<=0 and pre_lesson.timer_sec_left<=0:
            unlocked = True
        UserLessonCompletion.objects.create(user=user, lesson=lesson,
                                            timer_min_left=time_left_min,
                                            timer_sec_left=time_left_sec, unlocked=unlocked)
    user_course_map.total_lessons = len(UserLessonCompletion.objects.filter(user=user, lesson__unit__course=course))
    user_course_map.total_lessons_completed = len(UserLessonCompletion.objects.filter(user=user, lesson__unit__course=course, completed=True))
    if user_course_map.total_lessons>0:
        user_course_map.percentage_completion = user_course_map.total_lessons_completed / user_course_map.total_lessons * 100
    else :
        user_course_map.percentage_completion = 0
    user_course_map.save(update_fields=['total_lessons', 'total_lessons_completed', 'percentage_completion'])

def lesson_view(request, slug, course_slug):
    profile = Profile.objects.get(user=request.user)
    user = profile
    course = Course.objects.get(slug__iexact=course_slug)
    # Updating user_lesson for any new lesson
    # update_userlesson_completion(course, user)
    current_lesson = None
    if slug!='no-slug':
        current_lesson = UserLessonCompletion.objects.get(lesson__slug__iexact=slug, user=user)
    # Fetching data for course page
    user_course_map = UserCourseMap.objects.filter(course=course, user=user).first()
    units = Unit.objects.filter(course=course)
    contents = []
    for unit in units:
        lessons = UserLessonCompletion.objects.filter(user=user, lesson__unit=unit)
        comp = str(len(lessons.filter(completed=True)))+" / "+str(get_total_lessons(unit=unit))
        content = {
            'unit': unit, 
            'lessons': lessons, 
            'completed': comp
        }
        contents.append(content)
    # Announcements
    news = []
    anouncements = Anouncement.objects.filter(course=course)
    for anouncement in anouncements:
        comments = Comment.objects.filter(anouncement=anouncement)
        new = {
            'anouncement': anouncement,
            'comments': comments
        }
        news.append(new)
    # Ratings
    ratings = Rating.objects.filter(course=course)
    rating = ratings.first()
    all_five = []
    for i in ratings.values_list('five', 'four', 'three', 'two', 'one'):
        num = 5
        for any_o in i:
            per = 0
            if rating.get_total()!=0:
                per = any_o/rating.get_total()*100
            any_one = {'per': per, 'votes': any_o, 'for': num}
            all_five.append(any_one)
            num = num - 1
    ratings = {
        'all': all_five,
        'avg': rating.get_average(),
        'avg_per': rating.get_average()*20,
        'total': rating.get_total()
    }
    # Grades 
    grades = []
    for unit in units:
        lessons = Lesson.objects.filter(unit=unit)
        txp = 0
        for lesson in lessons:
            txp = txp + lesson.xp
        completed_on = "Not completed yet"
        last_lesson = UserLessonCompletion.objects.filter(user=user, lesson__unit=unit).last()
        if last_lesson.completed:
            completed_on = last_lesson.completed_on
        grade = {
            'name': unit.title,
            'videos': 0,
            'readings': len(lessons),
            'txp': txp,
            'due': completed_on
        }
        grades.append(grade)
    # Previous and next lesson
    pre_lesson = None
    next_lesson = None
    next_locked = None
    if current_lesson:
        nxt_locked = UserLessonCompletion.objects.filter(lesson__order__gt=current_lesson.lesson.order, unlocked=False)
        back = UserLessonCompletion.objects.filter(lesson__order=current_lesson.lesson.order-1)
        nxt = UserLessonCompletion.objects.filter(lesson__order=current_lesson.lesson.order+1)
        if nxt_locked.exists():
            next_locked = nxt_locked.first()
        if len(back)>0:
            pre_lesson = back.first()
        if len(nxt)>0:
            next_lesson = nxt.first()

    payload = {
        'current_lesson': current_lesson,
        'user_course_map': user_course_map,
        'contents': contents,
        'news': news,
        'ratings': ratings,
        'reviews': Review.objects.filter(course=course),
        'grades': grades,
        'back': pre_lesson,
        'next': next_lesson,
        'next_locked': next_locked,
        'user': user,
        'review_form': ReviewForm
    }
    return render(request, 'course/course-details.html', payload)

import datetime

def lesson_completed_or_redo(request, slug):
    profile = Profile.objects.get(user=request.user)
    user = profile
    redo = request.GET.get('redo')
    lesson = Lesson.objects.get(slug__iexact=slug)
    userLesson = UserLessonCompletion.objects.filter(user=user, lesson=lesson).first()
    # update_userlesson_completion(lesson.unit.course, user)
    if redo=="false":
        # Creating Log
        log = f" CHECKED lesson [{lesson.title}] as COMPLETED"
        EnrollmentHistory.objects.create(user=user, log=log, course=lesson.unit.course)
        # Updating lesson completed
        userLesson.completed = True
        # Updating UserCourseMap
        user_course_map = UserCourseMap.objects.get(user=user, course=userLesson.lesson.unit.course)
        user_course_map.total_xp += userLesson.lesson.xp
        userLesson.completed_on = datetime.datetime.now()
    else:
        # Creating Log
        log = f" UNCHECKED lesson [{lesson.title}] as NOT-COMPLETED"
        EnrollmentHistory.objects.create(user=user, log=log, course=lesson.unit.course)
        # Updating lesson completed
        userLesson.completed = False
        # Updating UserCourseMap
        user_course_map = UserCourseMap.objects.get(user=user, course=userLesson.lesson.unit.course)
        user_course_map.total_xp -= userLesson.lesson.xp
        userLesson.completed_on = None

    userLesson.save(update_fields=['completed', 'completed_on'])

    user_course_map.total_lessons = len(UserLessonCompletion.objects.filter(user=user, lesson__unit__course=userLesson.lesson.unit.course))
    user_course_map.total_lessons_completed = len(UserLessonCompletion.objects.filter(user=user, lesson__unit__course=userLesson.lesson.unit.course, completed=True))
    if user_course_map.total_lessons>0:
        user_course_map.percentage_completion = user_course_map.total_lessons_completed / user_course_map.total_lessons * 100
    else :
        user_course_map.percentage_completion = 0
    
    if user_course_map.percentage_completion==100:
        user_course_map.once_completed = True
        log = f"Course Completed!"
        EnrollmentHistory.objects.create(user=user, log=log, course=lesson.unit.course)
    user_course_map.save(update_fields=['percentage_completion', 'total_xp', "once_completed", 'total_lessons', 'total_lessons_completed'])
    print(user_course_map.percentage_completion)
    data = {
        'percentage': user_course_map.percentage_completion,
    }

    return JsonResponse({'data': data})

class ResetCourse(View):
    def get(self, request, slug):
        profile = Profile.objects.get(user=request.user)
        user_course_map = UserCourseMap.objects.filter(course__slug__iexact=slug)
        if user_course_map.exists():
            user_course_map = user_course_map.first()
            for i in UserLessonCompletion.objects.filter(lesson__unit__course__slug__iexact=slug, user=profile):
                i.delete()
            user_course_map.reset_count += 1
            user_course_map.total_lessons_completed = 0
            user_course_map.percentage_completion = 0
            user_course_map.save(update_fields=["reset_count", "total_lessons_completed", "percentage_completion"])
            return redirect('course-enrollment', slug=slug)
        return redirect('course-description', slug=slug)

class CoursePaymentView(View):
    def get(self, request, slug):
        profile = Profile.objects.get(user=request.user)
        user = profile
        course = Course.objects.filter(slug__iexact=slug).first()
        lessons = Lesson.objects.filter(unit__course=course)
        total_xp = 0
        for lesson in lessons:
            total_xp = total_xp + lesson.xp
        price = course.course_price
        affordable = False
        if price != 'FREE':
            price = int(price)
            if user.techsnap_cash > price:
                affordable = True
        else :
            affordable = True

        data = {
            'slug': course.slug,
            'title': course.course_title,
            'img': course.course_img,
            'duration': course.course_duration,
            'lessons': len(lessons),
            'total_xp': total_xp,
            'price': course.course_price,
            'affordable': affordable
        }

        return render(request, 'course/payment.html', data)
    
    def post(self, request, slug):
        profile = Profile.objects.get(user=request.user)
        user = profile
        course = Course.objects.filter(slug__iexact=slug).first()
        price = course.course_price
        if price != 'FREE':
            price = int(price)
            user.techsnap_cash = user.techsnap_cash - price
            user.save(update_fields=['techsnap_cash'])   
        return redirect('course-enrollment', slug=slug)
        
def log_out_course(request, slug):
    user = Profile.objects.get(user=request.user)
    course = Course.objects.get(slug=slug)

    # Creating log
    log = f" LOGGED OUT of Course [{course.course_title}]"
    EnrollmentHistory.objects.create(user=user, log=log, course=course)

    return redirect('course-description', slug=slug)

def get_history(request, slug, username):
    course = Course.objects.get(slug=slug)
    user = Profile.objects.get(user__username=username)

    logs = EnrollmentHistory.objects.filter(course=course, user=user)
    return render(request, 'course/logs.html', {'logs': logs, 'course': course, 'user': user})

def lesson_timer_update(request, pk):
    lesson = UserLessonCompletion.objects.filter(id=pk).first()
    minutes = request.GET.get('min')
    seconds = request.GET.get('sec')

    if int(lesson.timer_sec_left)>0 or int(lesson.timer_min_left)>0:
        print("fdS")
        if int(minutes)<=0 and int(seconds)<=0:
            next_lesson_user = UserLessonCompletion.objects.filter(
                lesson__order__gt=lesson.lesson.order, 
                unlocked=False, 
                user=request.user.profile, 
                lesson__unit__course=lesson.lesson.unit.course
                )
            if next_lesson_user.exists():
                next_lesson_user = next_lesson_user.first()
                next_lesson_user.unlocked = True
                next_lesson_user.save(update_fields=['unlocked'])
                
    lesson.timer_min_left = minutes
    lesson.timer_sec_left = seconds
    lesson.save(update_fields=['timer_min_left', 'timer_sec_left'])

    return JsonResponse({})

def create_review(request, slug, lesson_slug):
    course = Course.objects.get(slug__iexact=slug)
    profile = Profile.objects.get(user=request.user)
    form = ReviewForm(request.POST, request.FILES)
    if form.is_valid():
        review = form.save(commit=False)
        review.course = course
        review.img = profile.profile_pic
        review.name = profile.user.username
        review.save()
        return redirect('lesson-view', course_slug=slug, slug=lesson_slug)