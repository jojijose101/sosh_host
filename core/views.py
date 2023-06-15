from pickle import NONE
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import profile,Post,LikePost,FollowerCount
from django.http import HttpResponse
from itertools import chain
import random
# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object =User.objects.get(username=request.user.username)
    user_profile = profile.objects.get(user=user_object)
    posts = Post.objects.all()
    user_following_list = []
    feed = []
    user_following = FollowerCount.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)
    for usernames in user_following_list:
        feed_list = Post.objects.filter(user=usernames)
        feed.append(feed_list)
    feed_lists = list(chain(*feed))
    #user new suggestion starts
    all_user = User.objects.all()
    user_following_all = []
    
    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestion_list = [x for x in list(all_user) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestion_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []
    for user in final_suggestions_list:
        username_profile.append(user.id)

    for ids in username_profile:
        profile_lists = profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)
    
    suggestions_username_profile_list = list(chain(*username_profile_list))



    return render(request, 'index.html',{'user_profile' : user_profile, 'posts': feed_lists, 'suggestions_username_profile_list':suggestions_username_profile_list})


def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = profile.objects.get(user=user_object)
    if request.method == "POST":
        Username = request.POST['username']
        username_object = User.objects.filter(username__icontains=Username)

        username_profile = []
        username_profile_list = []
        for users in username_object:
            username_profile.append(users.id)
        for ids in username_profile:
            profile_list = profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_list)
        username_profile_lists = list(chain(*username_profile_list))
    
      



    
    
    return render(request, 'search.html',{'user_profile':user_profile, 'username_profile_list':username_profile_lists})





def setting(request):  # sourcery skip: extract-duplicate-method
    user_profile = profile.objects.get(user=request.user)
    if request.method == 'POST':
        

        if request.FILES.get('image') is None:
           Image = user_profile.profileimg
           Bio =request.POST['bio']
           Location = request.POST['location']
           firstnm = request.POST['firstnm']
           lastnm = request.POST['lastnm']
           email = request.POST['email']



           user_profile.profileimg = Image
           user_profile.bio = Bio
           user_profile.location = Location
           user_profile.firstnm =firstnm
           user_profile.lastnm = lastnm
           user_profile.email = email
           user_profile.save()

          

        if request.FILES.get('image') != None:
            Image = request.FILES.get('image')
            Bio =request.POST['bio']
            Location = request.POST['location']
            firstnm = request.POST['firstnm']
            lastnm = request.POST['lastnm']
            email = request.POST['email']

            user_profile.profileimg = Image
            user_profile.bio = Bio
            user_profile.location = Location
            user_profile.firstnm =firstnm
            user_profile.lastnm = lastnm
            
            user_profile.save()

            

        return redirect('setting')
        
    return render(request, 'setting.html', {'user_profile':user_profile})
@login_required(login_url='signin')
def upload_post(request):
    if request.method == 'POST':
        user = request.user.username
        Image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        if Image is None or caption is None:
            messages.info(request,'No value added')
            return redirect("/") 
        else:
             user_post = Post.objects.create(user=user, image=Image, caption=caption)
             user_post.save
    
       
            
    return redirect("/")  
    
@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    Post_id = request.GET.get('post_id')
    print(Post_id)
    post = Post.objects.get(id=Post_id)
    like_filter = LikePost.objects.filter(post_id=Post_id, username=username).first()
    if like_filter is None:
        new_like = LikePost.objects.create(post_id=Post_id, username=username)
        new_like.save()
        post.no_of_like = post.no_of_like+1
    else:
        like_filter.delete()
        post.no_of_like = post.no_of_like-1

    post.save()
    return redirect('/')
@login_required(login_url='signin')
def profile_usr(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = profile.objects.get(user=user_object)
    user_post = Post.objects.filter(user=pk)
    user_post_length = len(user_post)

    follwr = request.user.username
    user = pk
    if FollowerCount.objects.filter(follower=follwr, user=pk).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    
    flwr_count = len(FollowerCount.objects.filter(user=pk))
    flwng_count = len(FollowerCount.objects.filter(follower=pk))

    
   
    
    context = {
        'user_object' : user_object,
        'user_profile' : user_profile,
        'user_post' : user_post,
        'user_post_length' : user_post_length,
        'button_text' : button_text,
        'flwr_count' : flwr_count,
        'flwng_count' : flwng_count


    }


    return render(request, 'profile.html', context)



def signup(request):

    if request.method != "POST":
        return render(request, 'signup.html')
    Password = request.POST['password']
    Password2 = request.POST['password2']
    if len(Password) < 8:
        messages.info(request, 'password must be at least 8 charecters')
        return redirect('signup')
        
    elif Password == Password2:
        Username = request.POST['username']
        Email = request.POST['email']
        if User.objects.filter(email=Email):
            messages.info(request, 'email already taken')
            return redirect('signup')
        elif User.objects.filter(username=Username):
            messages.info(request, 'username already exist')
            return redirect('signup')
        else:
            return _extracted_from_signup_17(Username, Email, Password, request)
    else:
        messages.info(request, 'password not matching')
        return redirect('signup')


#signup supporting function
def _extracted_from_signup_17(Username, Email, Password, request):
    user = User.objects.create_user(username=Username, email=Email, password=Password)
    user.save()
    #log user in and redirect to settings 
    user_login = auth.authenticate(username=Username, password=Password)
    auth.login(request, user_login)


    #create a profile object for new user
    user_model = User.objects.get(username=Username)
    new_profile = profile.objects.create(user=user_model, id_user=user_model.id)
    new_profile.save()
    return redirect('setting')


@login_required(login_url='signin')
def follower_count(request):
    if request.method == "POST":
        follower = request.POST['follower']
        user = request.POST['user']
        follow_count = FollowerCount.objects.filter(follower=follower, user=user).first()
        if follow_count is not None:
            follow_count.delete()
            return redirect("profile/"+user)
        else:
            new_follow = FollowerCount.objects.create(follower=follower, user=user)
            new_follow.save()
            return redirect('profile/'+user)


    else:
        return redirect("/")


    
def signin(request):
    if request.method == 'POST':

        Username = request.POST['username']
        Password = request.POST['password']
        user = auth.authenticate(username=Username, password=Password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credential invalid')
            return redirect('signin')

    return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

