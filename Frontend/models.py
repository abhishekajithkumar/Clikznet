from django.db import models


# Create your models here.
class RegisterDB(models.Model):
    UserId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50, null=True, blank=True)
    Username = models.CharField(max_length=50, null=True, blank=True)
    Email = models.CharField(max_length=70, null=True, blank=True)
    Password = models.CharField(max_length=20, null=True, blank=True)
    DP = models.ImageField(upload_to="DP", default='default.jpg')
    Account_created = models.DateTimeField(auto_now_add=True)
    Status = models.IntegerField(default=0)


class PostDB(models.Model):
    PostId = models.AutoField(primary_key=True)
    UserId = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)
    Username = models.CharField(max_length=50, null=True, blank=True)
    Description = models.CharField(max_length=400, null=True, blank=True)
    PImage = models.ImageField(upload_to="PostImage", null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    no_of_likes = models.IntegerField(default=0)
    no_of_comments = models.IntegerField(default=0)


class LikeDB(models.Model):
    PostId = models.ForeignKey(PostDB, on_delete=models.CASCADE)
    UserId = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CommentDB(models.Model):
    PostId = models.ForeignKey(PostDB, on_delete=models.CASCADE)
    UserId = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)
    Comment = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class FollowerDB(models.Model):
    FollowerId = models.CharField(max_length=100, null=True)
    FollowingId = models.CharField(max_length=100, null=True)


class ReportDB(models.Model):
    PostId = models.ForeignKey(PostDB, on_delete=models.CASCADE)
    UserId = models.ForeignKey(RegisterDB, on_delete=models.CASCADE)
    Reason = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ReviewComment = models.CharField(max_length=100, null=True, blank=True)
    ReportStatus = models.IntegerField(default=0)


class HelpCenterDB(models.Model):
    UserId = models.ForeignKey(RegisterDB, on_delete=models.CASCADE, null=True, blank=True)
    Name = models.CharField(max_length=100, null=True, blank=True)
    Email = models.CharField(max_length=100, null=True, blank=True)
    Issue = models.CharField(max_length=50, null=True, blank=True)
    Details = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    MailComment = models.CharField(max_length=100, null=True, blank=True)
    MailStatus = models.IntegerField(default=0)
