from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from Frontend.models import RegisterDB, PostDB, FollowerDB, CommentDB, ReportDB, HelpCenterDB
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, "index.html")


def admin_login(request):
    return render(request, "admin_login.html")


def adminlogin(request):
    if request.method == "POST":
        un = request.POST.get('user_name')
        pwd = request.POST.get('pass_word')
        if User.objects.filter(username__contains=un).exists():
            user = authenticate(username=un, password=pwd)
            if user is not None:
                login(request, user)
                request.session['username'] = un
                request.session['password'] = pwd
                return redirect(user_data)
            else:
                return redirect(admin_login)
        else:
            return redirect(admin_login)


def admin_logout(request):
    del request.session['username']
    del request.session['password']
    return redirect(admin_login)


def user_data(request):
    if 'username' in request.session:
        data = RegisterDB.objects.all()
        return render(request, "user_data.html", {'data': data})
    else:
        return redirect(admin_login)


def remove_user(request, dataid):
    data = RegisterDB.objects.filter(UserId=dataid)
    following = FollowerDB.objects.filter(FollowingId=dataid)
    follower = FollowerDB.objects.filter(FollowerId=dataid)
    following.delete()
    follower.delete()
    data.delete()
    messages.warning(request, "Profile deleted successfully..!!")
    return redirect(user_data)


def delete_post(request, post_id):
    data = PostDB.objects.filter(PostId=post_id)
    data.delete()
    messages.warning(request, "Post deleted successfully..!!")
    return redirect(post_data)


def post_data(request):
    if 'username' in request.session:
        post = PostDB.objects.all()
        return render(request, "post_data.html", {'post': post})
    else:
        return redirect(admin_login)


def user_profile(request, dataid):
    if 'username' in request.session:
        user = RegisterDB.objects.filter(UserId=dataid)
        post = PostDB.objects.filter(UserId_id=dataid)
        followers_count = len(FollowerDB.objects.filter(FollowingId=dataid))
        following_count = len(FollowerDB.objects.filter(FollowerId=dataid))
        context = {
            'user': user,
            'post': post,
            'followers_count': followers_count,
            'following_count': following_count
        }
        return render(request, "user_profile.html", context)
    else:
        return redirect(admin_login)


def view_each_post(request, dataid):
    if 'username' in request.session:
        post = PostDB.objects.get(PostId=dataid)
        comments = CommentDB.objects.filter(PostId_id=dataid)
        context = {
            'post': post,
            'comments': comments
        }
        return render(request, "view_post.html", context)
    else:
        return redirect(admin_login)


def account_status(request):
    if request.method == "POST":
        u = request.POST.get('userid')
        user = RegisterDB.objects.get(UserId=u)
        if user.Status == 0:
            user.Status = 1
            user.save()
            return redirect('user_profile/'+u)
        elif user.Status == 1:
            user.Status = 0
            user.save()
            return redirect('user_profile/'+u)
        else:
            return redirect('user_profile/'+u)


def report_mail(request):
    if 'username' in request.session:
        mail = ReportDB.objects.all()
        ongoing = ReportDB.objects.filter(ReportStatus=0)
        pending = ReportDB.objects.filter(ReportStatus=1)
        closed = ReportDB.objects.filter(ReportStatus=2)
        return render(request, "report_mail.html", {'mail': mail, 'ongoing': ongoing, 'pending': pending, 'closed': closed})
    else:
        return redirect(admin_login)


def report_detail(request, dataid):
    if 'username' in request.session:
        details = ReportDB.objects.get(id=dataid)
        reports = ReportDB.objects.filter(PostId_id=details.PostId_id)
        return render(request, "report_detail.html", {'details': details, 'reports': reports})
    else:
        return redirect(admin_login)


def report_review(request):
    if request.method == "POST":
        rid = request.POST.get('report_id')
        c = request.POST.get('comment')
        s = request.POST.get('status')
        ReportDB.objects.filter(id=rid).update(ReportStatus=s, ReviewComment=c)
        return redirect(report_mail)


def help_mail(request):
    if 'username' in request.session:
        mails = HelpCenterDB.objects.all()
        waiting = HelpCenterDB.objects.filter(MailStatus=0)
        hold = HelpCenterDB.objects.filter(MailStatus=1)
        closed = HelpCenterDB.objects.filter(MailStatus=2)
        context = {
            'mails': mails,
            'waiting': waiting,
            'hold': hold,
            'closed': closed
        }
        return render(request, "help_mail.html", context)
    else:
        return redirect(admin_login)


def help_mail_detail(request, dataid):
    if 'username' in request.session:
        mail = HelpCenterDB.objects.get(id=dataid)
        return render(request, "help_mail_detail.html", {'mail': mail})
    else:
        return redirect(admin_login)


def help_mail_review(request):
    if request.method == "POST":
        m = request.POST.get('mail_id')
        c = request.POST.get('comment')
        s = request.POST.get('status')
        HelpCenterDB.objects.filter(id=m).update(MailStatus=s, MailComment=c)
        return redirect(help_mail)