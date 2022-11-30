
from django.shortcuts import redirect, render, get_object_or_404
from .models import Profile, Category, ForumPost, Comment, Reply
from .utils import update_views
from .forms import ForumPostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def home(request):
    forums = Category.objects.all()
    num_posts = ForumPost.objects.all().count()
    num_users = User.objects.all().count()
    num_categories = forums.count()
    try:
        last_post = ForumPost.objects.latest("date")
    except:
        last_post = []

    context = {
        "forums":forums,
        "num_posts":num_posts,
        "num_users":num_users,
        "num_categories":num_categories,
        "last_post":last_post,
        "title": "TechSnap forum app"
    }
    return render(request, "forum/forums.html", context)

def detail(request, slug):
    post = get_object_or_404(ForumPost, slug=slug)
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    
    if "comment-form" in request.POST:
        comment = request.POST.get("comment")
        new_comment, created = Comment.objects.get_or_create(user=profile, content=comment)
        post.comments.add(new_comment.id)

    if "reply-form" in request.POST:
        reply = request.POST.get("reply")
        commenr_id = request.POST.get("comment-id")
        comment_obj = Comment.objects.get(id=commenr_id)
        new_reply, created = Reply.objects.get_or_create(user=profile, content=reply)
        comment_obj.replies.add(new_reply.id)


    context = {
        "post":post,
        "title": "TechSnap: " + post.title,
    }
    update_views(request, post)

    return render(request, "forum/detail.html", context)

def posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = ForumPost.objects.filter(categories=category)
    paginator = Paginator(posts, 5)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) 

    context = {
        "posts":posts,
        "forum": category,
        "title": "TechSnap: Posts"
    }

    return render(request, "forum/posts.html", context)


@login_required
def create_post(request):
    context = {}
    form = ForumPostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print("\n\n its valid")
            profile = Profile.objects.get(user=request.user)
            new_post = form.save(commit=False)
            new_post.user = profile
            new_post.save()
            form.save_m2m()
            return redirect("home")
    context.update({
        "form": form,
        "title": "TechSnap: Create New Post"
    })
    return render(request, "forum/create_ForumPost.html", context)

def latest_posts(request):
    posts = ForumPost.objects.all()[:10]
    context = {
        "posts":posts,
        "title": "TechSnap: Latest 10 Posts"
    }

    return render(request, "forum/latest-posts.html", context)

def search_result(request):

    return render(request, "forum/search.html")