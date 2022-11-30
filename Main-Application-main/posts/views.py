import base64
import os
import json
import fitz
import tempfile
from django.http.response import HttpResponse, JsonResponse
import requests
from django.shortcuts import render, redirect

import posts
from .models import *
from django.views.generic import ListView, DetailView
from django.utils.text import slugify

imgbbkey='6f10f5615ec48ff5273a9930cc4bb194'

# Create your views here.
class PostsList(ListView):
    model = Posts
    template_name = 'posts_list.html'

class PostsDetail(DetailView):
    model = Posts
    template_name = 'post_detail.html'

def add_imgs(request):
    if request.method=='POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        post = Posts(profile=request.user.profile,
                     title=title,
                     desc=desc)
        post.save()
        i = 0
        postimages = []
        imgs = request.FILES.getlist('imgs')
        for img in imgs:
            req=requests.post("https://api.imgbb.com/1/upload", {'key': imgbbkey, 'image': base64.b64encode(img.read())})
            content=str(req.content)
            content=content.replace("true", "True").replace("false", "False").replace("null", "None")
            content=eval(eval(content))
            postimages.append(content['data']['url'].replace("\\",''))
            PostImage.objects.create(post=post, img_url=content['data']['url'].replace("\\",''), position=i)
            i += 1
        return redirect('feed', slug=request.user.profile.slug)
    return redirect('feed', slug=request.user.profile.slug)

def update_img_post(request, slug):
    if request.method=='POST':
        desc = request.POST.get('desc')
        # Updating
        post = Posts.objects.get(slug=slug)
        if desc:
            post.desc = desc
            post.save(update_fields=['desc'])

        i = 0
        postimages = []
        imgs = request.FILES.getlist('imgs')
        if not imgs:
            return redirect('feed', slug=request.user.profile.slug)
        # Deleting previous post images
        post.get_post_imgs().delete()
        for img in imgs:
            req=requests.post("https://api.imgbb.com/1/upload", {'key': imgbbkey, 'image': base64.b64encode(img.read())})
            content=str(req.content)
            content=content.replace("true", "True").replace("false", "False").replace("null", "None")
            content=eval(eval(content))
            postimages.append(content['data']['url'].replace("\\",''))
            PostImage.objects.create(post=post, img_url=content['data']['url'].replace("\\",''), position=i)
            i += 1
        return redirect('feed', slug=request.user.profile.slug)
    return redirect('feed', slug=request.user.profile.slug)

def add_pdf(request):
    if request.method=='POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        post = Posts(profile=request.user.profile,
                     title=title,
                     desc=desc)
        post.save()
        tempDir=tempfile.gettempdir()
        i = 0
        postimages = []
        pdfs = request.FILES.getlist('pdfs')
        imagefilenames=[]
        for pdf in pdfs:
            doc=fitz.open("pdf", pdf.read())
            for i in range(doc.page_count):
                page=doc.load_page(i)
                pix=page.get_pixmap()
                pix.save(tempDir+'/'+str(slugify(title))+str(i)+".png")
                imagefilenames.append(tempDir+'/'+str(slugify(title))+str(i)+".png")
        ite = 0
        for fname in imagefilenames:
            i=open(fname, 'rb')
            req=requests.post("https://api.imgbb.com/1/upload", {'key': imgbbkey, 'image': base64.b64encode(i.read())})
            content=str(req.content)
            content=content.replace("true", "True").replace("false", "False").replace("null", "None")
            content=eval(eval(content))
            postimages.append(content['data']['url'].replace("\\",''))
            #os.remove(fname)
            PostImage.objects.create(post=post, img_url=content['data']['url'].replace("\\",''), position=ite)
            ite += 1
        return HttpResponse('done')
    return HttpResponse('no')

def get_all_posts(request):
    posts = Posts.objects.all()
    ret = {}
    for post in posts:
        imgs = []
        for img in post.get_post_imgs():
            imgs.append(img.img_url)
        if post.profile.profile_pic:
            authorpfp = 'https://www.techsnap.in'+post.profile.profile_pic.url
        else:
            authorpfp = 'https://www.participate.nyc.gov/assets/decidim/default-avatar-43686fd5db4beed0141662a012321bbccd154ee1d9188b0d1f41e37b710af3cb.svg'
        ret[post.title] = {
            'title': post.title,
            'description': post.desc,
            'authorPfp': authorpfp,
            'createdOn': str(post.timestamp),
            'author': post.profile.user.username,
            'images': imgs,
        }
    return JsonResponse(ret)

def feeds(request, slug):
    posts = Posts.objects.all()
    following = [profile.user.username for profile in Profile.objects.filter(followers=request.user)]
    posts_ = []
    for post in posts:
        imgs = []
        for img in post.get_post_imgs():
            imgs.append(img.img_url)
        if post.profile.profile_pic:
            authorpfp = 'https://www.techsnap.in'+post.profile.profile_pic.url
        else:
            authorpfp = 'https://www.participate.nyc.gov/assets/decidim/default-avatar-43686fd5db4beed0141662a012321bbccd154ee1d9188b0d1f41e37b710af3cb.svg'
        
        comments = PostComment.objects.filter(post=post)
        comments_ = []
        for comment in comments:
            replies = PostReply.objects.filter(comment=comment)
            replies_ = []
            for reply in replies:
                if reply.reply_to_reply_code:
                    reply_ = {
                        'details':reply,
                        'reply_to': PostReply.objects.get(code=reply.reply_to_reply_code)
                    }
                    replies_.append(reply_)
                else :
                    replies_.append(reply)

            comment_ = {
                'replies': replies_,
                'details': comment
            }
            comments_.append(comment_)

        likes = []
        for user in post.likes.all().values_list('username'):
            likes.append(user[0])
        dislikes = []
        for user in post.dislikes.all().values_list('username'):
            dislikes.append(user[0])
        bookmarks = []
        for user in post.bookmarks.all().values_list('username'):
            bookmarks.append(user[0])

        reports = []
        for user in Report.objects.filter(post=post).values_list('user__username'):
            reports.append(user[0])

        ret = {
            'title': post.title,
            'description': post.desc,
            'pic': authorpfp,
            'created': str(post.timestamp),
            'author': post.profile,
            'images': imgs,
            'slug': post.slug,
            'id': post.id,
            'comments': comments_,
            'no_likes': len(likes),
            'no_dislikes': len(dislikes),
            'likes': likes,
            'dislikes': dislikes,
            'bookmarks': bookmarks,
            'reports': reports,
        }
        posts_.append(ret)
    return render(request, 'dash_feed.html', {'feeds': posts_, 'following': following})

def post_details(request, postslug):
    post = Posts.objects.get(slug=postslug)
    imgs = []
    for img in post.get_post_imgs():
        imgs.append(img.img_url)
    if post.profile.profile_pic:
        authorpfp = 'https://www.techsnap.in'+post.profile.profile_pic.url
    else:
        authorpfp = 'https://www.participate.nyc.gov/assets/decidim/default-avatar-43686fd5db4beed0141662a012321bbccd154ee1d9188b0d1f41e37b710af3cb.svg'
    
    comments = PostComment.objects.filter(post=post)
    comments_ = []
    for comment in comments:
        replies = PostReply.objects.filter(comment=comment)
        replies_ = []
        for reply in replies:
            if reply.reply_to_reply_code:
                reply_ = {
                    'details':reply,
                    'reply_to': PostReply.objects.get(code=reply.reply_to_reply_code)
                }
                replies_.append(reply_)
            else :
                replies_.append(reply)

        comment_ = {
            'replies': replies_,
            'details': comment
        }
        comments_.append(comment_)

    likes = []
    for user in post.likes.all().values_list('username'):
        likes.append(user[0])
    dislikes = []
    for user in post.dislikes.all().values_list('username'):
        dislikes.append(user[0])
    bookmarks = []
    for user in post.bookmarks.all().values_list('username'):
        bookmarks.append(user[0])

    reports = []
    for user in Report.objects.filter(post=post).values_list('user__username'):
        reports.append(user[0])

    ret = {
        'title': post.title,
        'description': post.desc,
        'pic': authorpfp,
        'created': str(post.timestamp),
        'author': post.profile,
        'images': imgs,
        'slug': post.slug,
        'id': post.id,
        'comments': comments_,
        'no_likes': len(likes),
        'no_dislikes': len(dislikes),
        'likes': likes,
        'dislikes': dislikes,
        'bookmarks': bookmarks,
        'reports': reports,
    }
    following = False
    if request.user in post.profile.followers.all():
        following  = True

    return render(request, 'postDetailsPage.html', {'feed': ret, 'following': following})

def create_comment(request):
    profile = Profile.objects.get(user=request.user)
    text = request.POST.get('comment')
    slug = request.POST.get('slug')
    post = Posts.objects.get(slug=slug)

    PostComment.objects.create(post=post, text=text, by=profile)
    return redirect('post-details', postslug=post.slug)

def create_reply(request):
    profile = Profile.objects.get(user=request.user)
    text = request.POST.get('text')
    comment_id = request.POST.get('id')
    comment = PostComment.objects.get(id=comment_id)
    reply_code = request.POST.get('reply_code')
    if reply_code:
        PostReply.objects.create(comment=comment, text=text, by=profile, reply_to_reply_code=reply_code)
    else:
        PostReply.objects.create(comment=comment, text=text, by=profile)
    return redirect('post-details', postslug=comment.post.slug)

def like(request, postslug, unlike):
    post = Posts.objects.get(slug=postslug)
    if unlike=="True":
        post.likes.remove(request.user)
    else :
        post.likes.add(request.user)
        post.dislikes.remove(request.user)
    return JsonResponse({'done': 'done!!!!!'})

def dislike(request, postslug, undislike):
    post = Posts.objects.get(slug=postslug)
    if undislike=="True":
        post.dislikes.remove(request.user)
    else :
        post.dislikes.add(request.user)
        post.likes.remove(request.user)
    return JsonResponse({'done': 'done!!!!!'})

def follow(request, postslug, unfollow):
    post = Posts.objects.get(slug=postslug)
    if unfollow=="True":
        post.profile.followers.remove(request.user)
    else :
        post.profile.followers.add(request.user)
    return JsonResponse({'done': 'done!!!!!'})
    
def bookmark(request, postslug, unmark):
    post = Posts.objects.get(slug=postslug)
    if unmark=="True":
        post.bookmarks.remove(request.user)
    else :
        post.bookmarks.add(request.user)
    return JsonResponse({'done': 'done!!!!!'})
    

def report(request, postslug):
    post = Posts.objects.get(slug=postslug)
    reason = request.GET.get('reason')
    Report.objects.create(post=post, user=request.user, reason=reason)
    return JsonResponse({'done': 'done!!!!!'})

def delete(request, slug):
    profile = Profile.objects.get(user=request.user)
    post = Posts.objects.get(slug=slug)
    post.archived = True
    post.save(update_fields=['archived'])
    return redirect('feed', slug=profile.slug)

def report_admin(request):
    if request.user.is_superuser:
        posts = Posts.objects.filter(reports__gt=0).order_by('-reports')
        return render(request, 'reports-panel/report_panel.html', {'posts': posts})
    
    return redirect('index')
    
def post_reports(request, slug):
    if request.user.is_superuser:
        post = Posts.objects.get(slug=slug)
        reports = Report.objects.filter(post=post)
        imgs = []
        for img in post.get_post_imgs():
            imgs.append(img.img_url)
        likes = []
        for user in post.likes.all().values_list('username'):
            likes.append(user[0])
        payload = {
            'post': post,
            'reports': reports,
            'likes': likes,
            'no_likes': len(likes),
            'images': imgs,
        }
        print(payload)
        return render(request, 'reports-panel/post_reports.html', payload)
    
    return redirect('index')