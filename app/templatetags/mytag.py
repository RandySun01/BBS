"""
@author RansySun
@create 2019-11-05-23:52
"""
from django.template import Library

register = Library()
from app import models
from django.db.models import Count
from django.db.models.functions import TruncMonth


@register.inclusion_tag('08left_menu.html')
def index(username):
    """缺什么传什么"""
    user_obj = models.UserInfo.objects.filter(username=username).first()

    blog_obj = user_obj.blog
    # 1查询当前用户所有分类及分类下的所有文章数
    category_list = models.Category.objects.filter(blog=blog_obj).annotate(count_num=Count('article__pk')).values_list(
        'name', 'count_num', 'pk')
    # print(category_list)

    # 2.查询当前用户所有的标签及标签下的文章数
    tag_list = models.Tag.objects.filter(blog=blog_obj).annotate(count_num=Count('article__pk')).values_list('name',
                                                                                                             'count_num',
                                                                                                             'pk')
    # print(tag_list)
    # 3.根据年月统计文章数
    data_list = models.Article.objects.filter(blog=blog_obj).annotate(month=TruncMonth('create_time')).values(
        'month').annotate(count=Count('pk')).values_list('month', 'count')

    return locals()

    # return {'usernmae':username....}


@register.simple_tag
def get_css(username):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    blog_css = user_obj.blog.site_name
    print(blog_css)
    return blog_css
