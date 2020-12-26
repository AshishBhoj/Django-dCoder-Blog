from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    allPosts = Post.objects.all().order_by('-timeStamp')[:1]
    AllPosts = Post.objects.all().order_by('-views')[:1]
    context = {'allPosts': allPosts, 'AllPosts': AllPosts}
    return render(request, 'home/home.html', context)

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request, "home/contact.html")

def about(request): 
    return render(request, 'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query) > 77 :
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent,allPostsAuthor)
    if allPosts.count() == 0:
        messages.warning(request, "No search results found")
    
    params = {'allPosts':allPosts, 'query':query}
    return render(request, 'home/search.html',params)

def signup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorneous input
        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Password do not match")
            return redirect('home')

        # Create the User
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your dCoder account is successfully created")
        return redirect('home')

    else:
        return HttpResponse('ERROR 404 NOT FOUND')
 
def handlelogin(request):
    if request.method == 'POST':

        # Get the Login Post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully")
            return redirect('home')
        
        else:
            messages.error(request, "Enter correct username and password")
            return redirect('home')

    return HttpResponse('ERROR 404 NOT FOUND')

def handlelogout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')

def createblog(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        content = request.POST['content']
        blog = Post(title=title, author=author, content=content)
        blog.save()
        messages.success(request, "Your Post Has Been Submitted Successfully")
    return render(request, 'home/createblog.html')