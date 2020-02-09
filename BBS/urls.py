"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from app import views
from django.views.static import serve
from BBS import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', views.register),  # 注册
    url(r'^login/', views.login),  # 登录
    url(r'^get_code/', views.get_code),  # 验证码请求
    url(r'^index/', views.index),  # 首页

    url(r'^logout/', views.logout),  # 注销

    # 评论功能
    url(r'^comments/', views.comment),

    # 点赞点彩
    url(r'^UpAndDown/', views.UpAndDown),

    # 后端管理
    url(r'^backend/', views.backend),

    # 添加文章
    url(r'^add_article/', views.add_article),

    # 文本编辑器上传图片
    url(r'^upload_img/', views.upload_img),

    # 修改头像
    url(r'^set_img/', views.set_img),

    # 暴露给外界后端文件资源, 上传文件会自动生成目录，不用加斜杠 media类似接口前缀,需要导入模块
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),

    # 放到上面因为会匹配不到,侧边栏查询
    url(r'^(?P<username>\w+)/(?P<condition>category|tag|archive)/(?P<param>.*)', views.site),

    # 个人站点搭建,匹配任意字符/给username
    url(r'^(?P<username>\w+)/$', views.site),

    # 侧边栏筛选功能
    # url(r'^(?P<username>\w+)/category/(\d+)/', views.site),
    # url(r'^(?P<username>\w+)/tag/(\d+)/', views.site),
    # url(r'^(?P<username>\w+)/archive/(\w+)/', views.site),

    # # 兼容上面三条url
    #
    # """
    #
    # url(r'^(?P<username>\w+)/', views.site),
    # url(r'^(?P<username>\w+)/(?P<condition>category|tag|archive)/(?P<param>.*)', views.site)
    # 两条url会冲突所以可以使用有两种方式解决方式一:对正则表达式下手，编写新的（添加一个$），方式二: 将第二条url放到第一条的上面
    #
    # """

    # 文章详情页
    # url(r'^(?P<username>\w+)/article/(?P<article_id>\d+)', views.article_detail),
    url(r'^(?P<username>\w+)/article/(?P<article_id>\d+)/', views.article_detail),

]
