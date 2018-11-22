from datetime import datetime
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField



# Create your models here.
# 1.新闻类型　
class Type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "新闻类型"
        verbose_name_plural = verbose_name
        db_table = "news_type"


# 2.用户信息
# 方法一，使用一对一关联django自带的User表
# class UserInfo(models.Model):
#     user = models.OneToOneField(to=User, to_field="id", related_name="userinfo")
#     mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")
#     gender = models.CharField(max_length=1, choices=(('0', "男"), ("1", "女")))
#     image = models.ImageField(upload_to="image/%Y/%m/%d", verbose_name="头像")
#     birthday = models.DateTimeField(null=True, blank=True)
#
#     def __str__(self):
#         return "%s" % self.user
#
#     class Meta:
#         verbose_name = "用户信息"
#         verbose_name_plural = verbose_name
#         db_table = "news_user_info"

# 方法二，替换掉django自带的User,继承它的所有字段
class UserInfo(AbstractUser):
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")
    gender = models.CharField(max_length=1, choices=(('0', "男"), ("1", "女")), default="1", verbose_name="性别")
    image = models.ImageField(upload_to="image/%Y/%m/%d", verbose_name="头像", default="image/default.png")
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        db_table = "news_user_info"


# 3.新闻内容
class Content(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name="标题")
    user_id = models.ForeignKey(to="UserInfo", to_field="id", related_name="content", verbose_name="作者")
    type_id = models.ForeignKey(to="Type", to_field="id", related_name="content", verbose_name="新闻类型")
    publish_time = models.DateTimeField(verbose_name="发布时间",default=datetime.now)
    read_count = models.IntegerField(default=0, verbose_name="阅读量")
    tag = models.CharField(max_length=100, verbose_name="标签")
    content = RichTextUploadingField(verbose_name="新闻内容", null=True, blank=True)
    image = models.ImageField(upload_to="image/%Y/%m/%d", verbose_name="封面图", default="image/default.png")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章内容"
        verbose_name_plural = verbose_name
        db_table = "news_content"


# 4.新闻评论
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    news_id = models.ForeignKey(to="Content", to_field="id", related_name="comment", verbose_name="评论文章")
    user_id = models.ForeignKey(to="UserInfo", to_field="id", related_name="comment", verbose_name="评论作者")
    publish_time = models.DateTimeField(verbose_name="发布时间",default=datetime.now)
    state = models.BooleanField(default=True, verbose_name="审核状态")
    # 4.5 回复:评论　评论
    content = RichTextUploadingField(verbose_name="评论内容")
    restore = models.ForeignKey(to="self", to_field="id", verbose_name="回复对象", null=True, blank=True)
    restore_user = models.ForeignKey(to="UserInfo", to_field="id", related_name="restore", verbose_name="回复的用户",
                                     null=True, blank=True)
    def __str__(self):
            return "%s" % self.id

    class Meta:
        verbose_name = "评论/回复"
        verbose_name_plural = verbose_name
        db_table = "news_comment"
