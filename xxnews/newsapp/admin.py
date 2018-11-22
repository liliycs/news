from django.contrib import admin
from newsapp.models import *
# Register your models here.

class TypeAdmin(admin.ModelAdmin):
    # 在admin中显⽰顺序
    list_display = ["id", "name"]
    # 给admin添加搜索功能
    search_fields = ["id", "name"]
    # 筛选字段
    list_filter = ["id", "name"]
    # 排序字段
    ordering = ["id"]


class UserInfoAdmin(admin.ModelAdmin):
    # 在admin中显⽰顺序
    list_display = ["username", "gender", "mobile", "email", "is_staff", "is_superuser"]
    # 给admin添加搜索功能
    search_fields = ["username", "gender", "mobile", "email"]
    # 筛选字段
    list_filter = ["username", "gender", "mobile", "email"]
    # 直接编辑字段
    list_editable = ["is_staff", "is_superuser"]
    # 排序字段
    ordering = ["id"]


class ContentAdmin(admin.ModelAdmin):
    # 在admin中显⽰顺序
    list_display = ["id", "title"]
    # 给admin添加搜索功能
    search_fields = ["id", "publish_time", "title"]
    # 排序字段
    ordering = ["-publish_time"]
    # 设置分页


class CommentAdmin(admin.ModelAdmin):
    # 在admin中显⽰顺序
    list_display = ["id", "content", "user_id", "news_id", "state"]
    # 给admin添加搜索功能
    search_fields = ["id", "publish_time", "user_id", "news_id"]
    # 直接编辑字段
    list_editable = ["state"]
    # 排序字段
    ordering = ["-publish_time"]


admin.site.register(Type, TypeAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Comment, CommentAdmin)
