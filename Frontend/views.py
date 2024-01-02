from django.shortcuts import render, redirect
from Frontend.models import RegisterDB, PostDB, LikeDB, FollowerDB, CommentDB, ReportDB, HelpCenterDB
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from itertools import chain
import random
import re
from django.http import JsonResponse


# Create your views here.
def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")


def save_register(request):
    if request.method == "POST":
        n = request.POST.get('name')
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        c = request.POST.get('confirmPassword')
        if RegisterDB.objects.filter(Username=u).exists():
            messages.error(request, "Username already exist..!!")
            return redirect(register)
        if RegisterDB.objects.filter(Email=e).exists():
            messages.error(request, "Email Id already exist..!!")
            return redirect(register)
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$", p):
            messages.error(request, "Password should be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
            return redirect(register)
        if p != c:
            messages.error(request, "Password mismatched..!!")
            return redirect(register)

        obj = RegisterDB(Name=n, Username=u, Email=e, Password=p)
        obj.save()
        messages.success(request, "Registration Successfully Completed..!!")
        return redirect(login)


def user_login(request):
    if request.method == "POST":
        un = request.POST.get('username')
        pwd = request.POST.get('password')
        if RegisterDB.objects.filter(Username=un, Password=pwd).exists():
            request.session['Username'] = un
            request.session['Password'] = pwd
            user = RegisterDB.objects.get(Username=un, Password=pwd)
            request.session['userid'] = user.UserId
            messages.info(request, "Logged in Successfully..!!")
            return redirect(timeline)
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect(login)
    return redirect(login)


def user_logout(request):
    del request.session['Username']
    del request.session['Password']
    del request.session['userid']
    return redirect(login)


def home(request):
    if 'userid' in request.session:
        profile = RegisterDB.objects.get(UserId=request.session['userid'])
        return render(request, "home.html", {'profile': profile})
    else:
        return redirect(login)


def timeline(request):
    if 'userid' in request.session:
        user_id = request.session.get('userid')
        posts = PostDB.objects.all()
        post = PostDB.objects.all().exclude(UserId_id=user_id)
        profile = RegisterDB.objects.get(UserId=request.session['userid'])
        like = LikeDB.objects.filter(UserId_id=user_id)

        likes = []
        for lk in like:
            likes.append(lk.PostId_id)

        user_following_list = []
        feed = []

        user_following = FollowerDB.objects.filter(FollowerId=user_id)

        for users in user_following:
            user_following_list.append(users.FollowingId)

        for uid in user_following_list:
            feed_list = PostDB.objects.filter(UserId_id=uid)
            feed.append(feed_list)

        feed_list = list(chain(*feed))
        # random.shuffle(feed_list)

        all_users = RegisterDB.objects.all()
        user_following_all = []

        for user in user_following:
            user_list = RegisterDB.objects.get(UserId=user.FollowingId)
            user_following_all.append(user_list)

        new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
        current_user = RegisterDB.objects.filter(UserId=user_id)
        final_suggestions = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
        random.shuffle(final_suggestions)

        username_profile = []
        username_profile_list = []

        for users in final_suggestions:
            username_profile.append(users.UserId)

        for ids in username_profile:
            profile_lists = RegisterDB.objects.filter(UserId=ids)
            username_profile_list.append(profile_lists)

        suggestions_username_profile_list = list(chain(*username_profile_list))

        context = {
            'post': feed_list,
            'profile': profile,
            'likes': likes,
            'suggestions': suggestions_username_profile_list[:4]
        }
        if profile.Status == 0:
            return render(request, "timeline.html", context)
        else:
            return redirect(disabled)
    else:
        return redirect(login)


def post_to_timeline(request):
    if request.method == "POST":
        un = request.POST.get('username')
        uid = RegisterDB.objects.get(UserId=request.session['userid'])
        d = request.POST.get('description')
        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = None
        obj = PostDB(Username=un, UserId=uid, Description=d, PImage=file)
        obj.save()
        messages.success(request, "Post added to Timeline")
        return redirect(timeline)


def like_post(request):
    if request.method == "POST" and request.is_ajax():
        post_id = request.POST.get('postid')
        user_id = request.session.get('userid')

        if LikeDB.objects.filter(PostId_id=post_id, UserId_id=user_id).exists():
            dislike = LikeDB.objects.filter(PostId_id=post_id, UserId_id=user_id)
            dislike.delete()
            post = PostDB.objects.get(PostId=post_id)
            post.no_of_likes -= 1
            post.save()
        else:
            obj = LikeDB(PostId_id=post_id, UserId_id=user_id)
            obj.save()
            post = PostDB.objects.get(PostId=post_id)
            post.no_of_likes += 1
            post.save()

        updated_likes_count = PostDB.objects.get(PostId=post_id).no_of_likes

        # Return JSON response with updated likes count
        return JsonResponse({'likes_count': updated_likes_count})

    # Handle other cases or invalid requests
    return JsonResponse({'error': 'Invalid request'}, status=400)


def userprofile(request, dataid):
    if 'userid' in request.session:
        profile = RegisterDB.objects.get(UserId=request.session['userid'])
        data = RegisterDB.objects.filter(Username=request.session['Username'])
        user = RegisterDB.objects.filter(UserId=dataid)
        post = PostDB.objects.filter(UserId=dataid)
        like = LikeDB.objects.filter(UserId_id=profile)

        likes = []
        for lk in like:
            likes.append(lk.PostId_id)

        follower = request.session.get('userid')
        following = dataid
        if FollowerDB.objects.filter(FollowerId=follower, FollowingId=following).first():
            button_text = 'Unfollow'
        else:
            button_text = 'Follow'

        followers_count = len(FollowerDB.objects.filter(FollowingId=dataid))
        following_count = len(FollowerDB.objects.filter(FollowerId=dataid))
        context = {
            'profile': profile,
            'button_text': button_text,
            'user': user,
            'data': data,
            'post': post,
            'likes': likes,
            'followers_count': followers_count,
            'following_count': following_count
        }
        if profile.Status == 0:
            return render(request, "userprofile.html", context)
        else:
            return redirect(disabled)
    else:
        return redirect(login)


def follow(request):
    if request.method == "POST":
        follower = request.POST.get('follower')
        following = request.POST.get('following')

        if FollowerDB.objects.filter(FollowerId=follower, FollowingId=following).first():
            delete_follower = FollowerDB.objects.get(FollowerId=follower, FollowingId=following)
            delete_follower.delete()
            return redirect('userprofile/'+following)
        else:
            new_follower = FollowerDB.objects.create(FollowerId=follower, FollowingId=following)
            new_follower.save()
            return redirect('userprofile/'+following)
    else:
        return redirect(timeline)


def my_profile(request):
    if 'userid' in request.session:
        user_id = request.session.get('userid')
        profile = RegisterDB.objects.get(UserId=request.session['userid'])
        data = RegisterDB.objects.filter(UserId=request.session['userid'])
        post = PostDB.objects.filter(UserId=request.session['userid'])
        like = LikeDB.objects.filter(UserId_id=user_id)

        likes = []
        for lk in like:
            likes.append(lk.PostId_id)

        user_following = FollowerDB.objects.filter(FollowerId=user_id)
        user_follower = FollowerDB.objects.filter(FollowingId=user_id)

        user_following_all = []
        user_followers_all = []
        for user in user_following:
            user_list = RegisterDB.objects.get(UserId=user.FollowingId)
            user_following_all.append(user_list)

        for user in user_follower:
            user_list = RegisterDB.objects.get(UserId=user.FollowerId)
            user_followers_all.append(user_list)

        followers_count = len(FollowerDB.objects.filter(FollowingId=profile.UserId))
        following_count = len(FollowerDB.objects.filter(FollowerId=profile.UserId))

        context = {
            'profile': profile,
            'data': data,
            'post': post,
            'likes': likes,
            'following_count': following_count,
            'followers_count': followers_count,
            'user_following_all': user_following_all,
            'user_followers_all': user_followers_all
        }
        if profile.Status == 0:
            return render(request, "myprofile.html", context)
        else:
            return redirect(disabled)
    else:
        return redirect(login)


def edit_profile(request):
    if 'userid' in request.session:
        profile = RegisterDB.objects.get(UserId=request.session['userid'])
        data = RegisterDB.objects.filter(UserId=request.session['userid'])
        if profile.Status == 0:
            return render(request, "edit_profile.html", {'profile': profile, 'data': data})
        else:
            return redirect(disabled)

    else:
        return redirect(login)


def update_profile(request, dataid):
    if request.method == "POST":
        fn = request.POST.get('name')
        un = request.POST.get('username')
        e = request.POST.get('email')
        existing_user = RegisterDB.objects.exclude(UserId=dataid).filter(Username=un).exists()
        existing_email = RegisterDB.objects.exclude(UserId=dataid).filter(Email=e).exists()
        if existing_user:
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('edit_profile')
        if existing_email:
            messages.error(request, "Email Id already exists. Please choose a different Email.")
            return redirect('edit_profile')
        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = RegisterDB.objects.get(UserId=dataid).DP
        RegisterDB.objects.filter(UserId=dataid).update(Name=fn, Username=un, Email=e, DP=file)
        request.session['Username'] = un
        messages.success(request, "Profile updated successfully..!!")
        return redirect(my_profile)


def change_password(request):
    if 'userid' in request.session:
        profile = RegisterDB.objects.get(UserId=request.session['userid'])
        if profile.Status == 0:
            return render(request, "change_password.html", {"profile": profile})
        else:
            return redirect(disabled)
    else:
        return redirect(login)


def update_password(request, userid):
    if request.method == "POST":
        old = request.POST.get('old-get')
        type_old = request.POST.get('oldPassword')
        new = request.POST.get('password')
        c_new = request.POST.get('confirmPassword')

        if old == type_old:
            if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$", new):
                messages.error(request, "Password should be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
                return redirect(change_password)
            else:
                if new == c_new:
                    RegisterDB.objects.filter(UserId=userid).update(Password=new)
                    messages.success(request, "Password updated successfully..!!")
                    return redirect(user_logout)
                else:
                    messages.error(request, "Password mismatched..!!")
                    return redirect(change_password)
        else:
            messages.error(request, "Re-enter old password..!!")
            return redirect(change_password)


def remove_post(request, dataid):
    like = LikeDB.objects.filter(PostId_id=dataid)
    like.delete()
    data = PostDB.objects.filter(PostId=dataid)
    data.delete()
    messages.error(request, "Post Removed..!!")
    return redirect(my_profile)


def Search(req):
    if 'userid' in req.session:
        data = RegisterDB.objects.filter(Username=req.session['Username'])
        profile = RegisterDB.objects.get(UserId=req.session['userid'])
        user_profile = RegisterDB.objects.all()

        if req.method == "POST":
            username = req.POST.get('username')
            username_object = RegisterDB.objects.filter(Username__contains=username)

            username_profile = []
            username_profile_list = []

            for users in username_object:
                username_profile.append(users.Username)

            for usernames in username_profile:
                profile_list = RegisterDB.objects.filter(Username=usernames)
                username_profile_list.append(profile_list)

            username_profile_list = list(chain(*username_profile_list))

        if profile.Status == 0:
            return render(req, 'search.html',{'username_profile_list': username_profile_list, 'data': data, 'profile': profile, 'username': username})
        else:
            return redirect(disabled)
    else:
        return redirect(login)


def view_post(request, dataid):
    if 'userid' in request.session:
        profile = RegisterDB.objects.get(UserId=request.session['userid'])
        post = PostDB.objects.get(PostId=dataid)
        comments = CommentDB.objects.filter(PostId_id=dataid)
        like = LikeDB.objects.filter(UserId_id=profile.UserId)
        likes = []
        for lk in like:
            likes.append(lk.PostId_id)
        if profile.Status == 0:
            return render(request, "viewpost.html", {'profile': profile, 'post': post, 'comments': comments, 'likes': likes})
        else:
            return redirect(disabled)
    else:
        return redirect(login)


def comment(request):
    if request.method == "POST":
        u = request.POST.get('user_id')
        p = request.POST.get('post_id')
        c = request.POST.get('comment')
        obj = CommentDB(UserId_id=u, PostId_id=p, Comment=c)
        obj.save()
        post = PostDB.objects.get(PostId=p)
        post.no_of_comments += 1
        post.save()
        return redirect('view_post/'+p)


def delete_comment(request):
    if request.method == "POST":
        c = request.POST.get('commentId')
        p = request.POST.get('postId')
        cmnt = CommentDB.objects.get(id=c)
        cmnt.delete()
        post = PostDB.objects.get(PostId=p)
        post.no_of_comments -= 1
        post.save()
        return redirect('view_post/'+p)


def disabled(request):
    if 'userid' in request.session:
        profile = RegisterDB.objects.get(UserId=request.session['userid'])
        if profile.Status == 1:
            return render(request, "disabled.html", {'profile': profile})
        else:
            return redirect(timeline)
    else:
        return redirect(login)


def report(request):
    if request.method == "POST":
        u = request.POST.get('userid')
        p = request.POST.get('postid')
        r = request.POST.get('reason')
        obj = ReportDB(UserId_id=u, PostId_id=p, Reason=r)
        obj.save()
        messages.success(request, "Thank You, we received your report.")
        return redirect(timeline)


def help_center(request):
    if 'userid' in request.session:
        profile = RegisterDB.objects.get(UserId=request.session['userid'])
        return render(request, "help_center.html", {'profile': profile})
    else:
        return render(request, "help_center.html")


def help_center_mail(request):
    if request.method == "POST":
        u = request.POST.get('userid')
        n = request.POST.get('name')
        e = request.POST.get('email')
        i = request.POST.get('issue')
        d = request.POST.get('details')
        obj = HelpCenterDB(UserId_id=u, Name=n, Email=e, Issue=i, Details=d)
        obj.save()
        return redirect(disabled)
