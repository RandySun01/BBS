from django.test import TestCase

# Create your tests here.
import os


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BBS.settings")
    import django
    django.setup()
    from app import models
    Article_obj = models.Article.objects.all().first()
    print(Article_obj.blog.userinfo.username)


    user_obj = models.UserInfo.objects.filter(username='randy').first()

    blog_obj = user_obj.blog
    from django.db.models import Count
    # 查询当前用户所有分类下的文章数


    # category_list = models.Category.objects.filter(blog=blog_obj).annotate(count_num=Count('article__pk')).values('name','count_num')

    res = models.Category.objects.filter(blog=blog_obj).annotate(count_num=Count('article__pk')).values_list('count_num','name')
    print(res)

5