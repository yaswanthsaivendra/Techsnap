from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Blogs, BlogComments
from django.contrib.auth.decorators import login_required
from .forms import BlogsForm
from django.urls import reverse
from django.http.response import HttpResponseRedirect

# Create your views here.
class BlogsListView(ListView):
	model = Blogs
	template_name = 'blog_list.html'

class BlogDetailView(DetailView):
	model = Blogs
	template_name = 'blog_detail.html'

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blogs
    template_name = 'blog_create.html'
    form_class = BlogsForm

    def post(self, request):
        status = self.request.GET.get('status')
        title = request.POST['title']
        body = request.POST['body']
        banner_img = request.FILES['banner_img']
        blog = Blogs.objects.create(author=request.user,
                                    title=title,
                                    body=body,
                                    banner_img=banner_img)
        if status=='review':
            blog.user_status = True
            blog.save()
            return HttpResponseRedirect(reverse('blogs:blogdetail', kwargs={'slug': blog.slug}))
        elif status=='draft':
            blog.save()
            return HttpResponseRedirect(reverse('blogs:blogedit', kwargs={'slug': blog.slug}))
        elif status=='preview':
            blog.save()
            return HttpResponseRedirect(reverse('blogs:blogdetail', kwargs={'slug': blog.slug}))

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blogs
    template_name = 'blog_edit.html'
    form_class = BlogsForm

    def get_context_data(self, *args, **kwargs):
        context = super(BlogUpdateView, self).get_context_data(*args, **kwargs)
        blog = get_object_or_404(Blogs, slug=self.kwargs['slug'])
        context['blog'] = blog
        if not blog.user_status and not blog.status:
            context['status'] = 'Draft'
        elif blog.user_status and not blog.status:
            context['status'] = 'Under Review'
        elif blog.user_status and blog.status:
            context['status'] = 'Published'
        return context

    def post(self, request, slug):
        status = self.request.GET.get('status')
        title = request.POST.get('title')
        body = request.POST.get('body')
        banner_img = request.FILES.get('banner_img')
        blog = get_object_or_404(Blogs, slug=slug)
        blog.title = title
        if blog.banner_img and banner_img:
            blog.banner_img = banner_img
        elif blog.banner_img is not None and banner_img:
            blog.banner_img = banner_img
        blog.body = body
        if status=='review':
            blog.user_status = True
            blog.save()
            return HttpResponseRedirect(reverse('blogs:blogdetail', kwargs={'slug': blog.slug}))
        elif status=='draft':
            blog.save()
            return HttpResponseRedirect(reverse('blogs:blogedit', kwargs={'slug': blog.slug}))
        elif status=='preview':
            blog.save()
            return HttpResponseRedirect(reverse('blogs:blogdetail', kwargs={'slug': blog.slug}))

def post_comment(request):
    if request.method=='POST':
        blogId = request.GET.get('blog')
        blog = get_object_or_404(Blogs, id=blogId)
        comment = request.POST.get('comment')
        commentid = request.POST.get('commentid')
        if commentid=='':
            blog_comment = BlogComments(blog=blog, comment=comment, user=request.user)
        else:
            parent_blog_comment = get_object_or_404(BlogComments, id=commentid)
            blog_comment = BlogComments(blog=blog, comment=comment, user=request.user, parent_blog=parent_blog_comment)
        blog_comment.save()
    return HttpResponseRedirect(reverse('blogs:blogdetail', kwargs={'slug': blog.slug}))