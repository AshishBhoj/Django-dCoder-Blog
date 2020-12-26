from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extra
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.signals import pre_save
from django.utils.text import slugify 

def blogHome(request): 
    allPosts_list = Post.objects.all().order_by('-views')
    paginator = Paginator(allPosts_list, 3)
    page = request.GET.get('page')
    try:
        allPosts = paginator.page(page)
    except PageNotAnInteger:
        allPosts = paginator.page(1)
    except EmptyPage:
        allPosts = paginator.page(paginator.num_pages)
    context={'allPosts': allPosts}
    return render(request, "blog/blogHome.html", context)

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None).order_by('-timeStamp')
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post': post, 'comments':comments, 'user':request.user, 'replyDict':replyDict, 'replies':replies}
    return render(request, 'blog/blogPost.html',context)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comments = BlogComment(comment=comment, user=user, post=post)
            comments.save()
            messages.success(request, "Comment has been posted")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comments = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comments.save()
            messages.success(request, "Reply has been posted")
    return redirect(f"/blog/{post.slug}")

def pre_save_receiver(sender, instance, *args, **kwargs): 
    slug = slugify(instance.title)
    exists = Post.objects.filter(slug=slug).exists()
    if exists:
        slug = "%s-%s" %(slug, instance.sno)
    instance.slug = slug

pre_save.connect(pre_save_receiver, sender = Post) 