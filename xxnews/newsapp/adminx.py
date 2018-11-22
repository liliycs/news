#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import xadmin
from xadmin import views
from newsapp.models import *


class TypeAdmin(object):
    # 在admin中显⽰顺序
    list_display = ["id", "name"]
    # 给admin添加搜索功能
    search_fields = ["id", "name"]
    # 筛选字段
    list_filter = ["id", "name"]
    # 排序字段
    ordering = ["id"]


class ContentAdmin(object):
    # 在admin中显⽰顺序
    list_display = ["id", "title", "tag"]
    # 给admin添加搜索功能
    search_fields = ["id", "publish_time", "title", "tag"]
    # 排序字段
    ordering = ["-publish_time"]
    # 设置分页 每页显示数据的条数
    list_per_page = 10



class CommentAdmin(object):
    # 在admin中显⽰顺序
    list_display = ["id", "content", "user_id", "news_id", "state"]
    # 给admin添加搜索功能
    search_fields = ["id", "publish_time", "user_id", "news_id"]
    # 直接编辑字段
    list_editable = ["state"]
    # 排序字段
    ordering = ["-publish_time"]


# 基础功能设置
class BaseSetting:
    enable_themes = True
    use_bootswatch = True


# 全局设置
class GlobalSettings:
    # 标题设置
    site_title = "xxnews后台管理系统"
    # 底部信息
    site_footer = "老左新闻网站"
    # 折叠
    menu_style = "accordion"


xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(Type, TypeAdmin)
xadmin.site.register(Content, ContentAdmin)
xadmin.site.register(Comment, CommentAdmin)
