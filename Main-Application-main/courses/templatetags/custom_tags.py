from django import template
from courses.models import Course, Lessons, UserLessons
from accounts.models import Notifications

register = template.Library()

@register.filter(name='get_percentage')
def get_percentage(course, user):
    # topic = courseTopic.objects.filter
    total = UserLessons.objects.filter(courselesson__course__id=course, user__id=user).count()
    done = UserLessons.objects.filter(courselesson__course__id=course, done=True, user__id=user).count()
    if done==0:
        return 0
    percentage = done / total
    return round(percentage*100, 2)

@register.filter(name='exclude')
def exclude(user, mark_as_read):
    # topic = courseTopic.objects.filter
    notifs = Notifications.objects.filter(mark_as_read=mark_as_read)
    if len(notifs)>0:
        return len(notifs)