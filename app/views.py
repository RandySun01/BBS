from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse

# Create your views here.

from app.utitle.formregister import MyRegForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from app import models


def register(request):
    """
    注册功能实现
    :param request:
    :return:
    """
    # 组件校验数据
    form_obj = MyRegForm()

    if request.method == 'POST':

        # 向前台返回结果信息
        back_dic = {'code': 1000, "msg": ''}

        form_obj = MyRegForm(request.POST)
        # print(request.POST)
        # print(request.FILES)
        # 校验数据

        if form_obj.is_valid():  # 验证所有表单是否全部通过
            # form_obj.cleaned_data  # {'username': 'randy', 'password': '123456', 'confirm_password': '123456', 'email': '2214644978@qq.com'}
            cleaned_data = form_obj.cleaned_data  # 所有验证通过的键值对
            # 移除确认密码
            cleaned_data.pop('confirm_password')

            file_obj = request.FILES.get('avatar')  # 获取用户头像, 如果没有上传, 则为空

            if file_obj:
                """
                获取用户上传头像之后,一定要判断用户是否上传了,
                如果没有上传,字典中就不会加avatar键值对
                """

                cleaned_data['avatar'] = file_obj

            # 通过 ** 打散字典的方式作为参数, key必须与数据库中字段中一模一样
            models.UserInfo.objects.create_user(**cleaned_data)

            back_dic['url'] = '/login/'

        else:
            # 向前台返回发生错误信息
            back_dic['code'] = 2000
            back_dic['msg'] = form_obj.errors
            print(back_dic)
        return JsonResponse(back_dic)
    return render(request, '01register.html', locals())


def login(request):
    back_dic = {'code': 1000, 'msg': ""}
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code').upper()
        session_code = request.session.get('code').upper()
        if code == session_code:
            user_obj = auth.authenticate(username=username, password=password)
            if user_obj:
                back_dic['url'] = '/index/'
                # 保存用户登录状态
                auth.login(request, user_obj)  # 自动保存到session
            else:
                back_dic['code'] = ''
                back_dic['msg'] = '用户名或密码错误！'
        else:
            back_dic['code'] = ''
            back_dic['msg'] = '验证码错误！'
        return JsonResponse(back_dic)
    return render(request, '02login.html')


from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO, StringIO


def get_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def get_code(request):
    '图片验证'
    # img:标签支持1.图片二进制 2. 图片具体路径 3. 后端url请求
    # 推到思路1: 直接到后端获取目录下的路径,以二进制方式打开发送
    # with open(r'G:\python学习\Django\11Django项目\BBS\static\img\1.jpg', 'rb') as f:
    #     data = f.read()
    #
    # return HttpResponse(data)

    # 推到思路二: 利用模块产生图片, 在发送到前端 pillow

    # 1.生成一张图片对象
    # img_obj = Image.new('RGB', (260, 35), get_color())
    #
    # # 2.先利用文件操作将图片对象写入文件中
    # with open('code.png', 'wb') as f:
    #     img_obj.save(f, 'png')
    #
    # # 3. 在利用文件操作图片以二进制形式读取出来,返回给前端
    # with open('code.png', 'rb') as f:
    #     data = f.read()
    #
    # return HttpResponse(data)

    # 推到思路3: 不在利用文件获取数据 借助内存管理器

    # 1. 生成图片对象
    # img_obj = Image.new('RGB', (260, 35), get_color())
    # # 2. 生成一个内存管理器对象
    # io_obj = BytesIO()
    #
    # # 3.将io_obj当成文件句柄f
    # img_obj.save(io_obj, 'png')
    #
    # # 4 获取二进制图片发送给前端
    # return HttpResponse(io_obj.getvalue())

    # 推导思路四:在图片写入文字
    # 1. 生成图片对象
    img_obj = Image.new('RGB', (260, 35), get_color())

    # 2.生成一个画笔对象
    img_draw = ImageDraw.Draw(img_obj)

    # 3. 设置画笔字体样式(所有字体样式都是由.ttf结尾的文件控制)
    img_font = ImageFont.truetype(r'G:\python学习\Django\11Django项目\BBS\static\font\222.ttf', 30)

    # 生成随机验证码
    code = ''
    # 随机生成验证码  a~z  A~Z  0~9
    for i in range(5):
        random_upper = chr(random.randint(65, 90))
        random_lower = chr(random.randint(97, 122))
        random_int = str(random.randint(0, 9))
        res = random.choice([random_upper, random_lower, random_int])

        # 将产生的随机字符串写到图片上
        img_draw.text((i * 45 + 45, 0), res, get_color(), img_font)

        code += res

    print(code)

    # 将随机验证码存储起来, 以便其他函数调用
    request.session['code'] = code

    io_obj = BytesIO()
    img_obj.save(io_obj, 'png')

    return HttpResponse(io_obj.getvalue())


from app.utils.mypage import Pagination


@login_required
def index(request):
    article_list = models.Article.objects.all()
    # 分页器
    page_obj = Pagination(current_page=request.GET.get('page', 1), all_count=article_list.count())
    article_list = article_list[page_obj.start: page_obj.end]
    return render(request, '03index.html', locals())


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect('/login/')


def set_password(request):
    print(request.POST)
    back_dic = {"code": 1000, 'msg': ''}
    if request.POST:
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        # 判断两次密码是否一样
        if new_password == confirm_password:
            if request.user.check_password(old_password):
                request.user.set_password(new_password)
                request.user.save()
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '旧密码输入错误！'
        else:
            back_dic['code'] = 3000
            back_dic['msg'] = '两次密码输入不一样！'
        return JsonResponse(back_dic)
    return redirect('/index/')


from django.db.models import Count
from django.db.models.functions import TruncMonth  # 可以切割日期对日期进行分组


@login_required
def site(request, username, **kwargs):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    if not user_obj:
        return render(request, '04error.html')
    blog_obj = user_obj.blog

    # 查询当前用户所有文章数
    article_list = models.Article.objects.filter(blog=blog_obj)

    # 侧边栏数据查询
    if kwargs:
        condition = kwargs.get('condition')
        param = kwargs.get('param')
        if condition == 'category':
            # 根据分类中的id进行筛选
            article_list = article_list.filter(category=param)

        elif condition == 'tag':
            # 连表查询实现便签类别的id查询
            article_list = article_list.filter(tag__id=param)
        else:
            # 根据年月进行查询
            year, month = param.split('-')
            article_list = article_list.filter(create_time__year=year, create_time__month=month)

        print(kwargs)

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
    # print(data_list)

    return render(request, '05site.html', locals())


def article_detail(request, username, article_id):
    """
    文章展示
    :param request:
    :param username:
    :param article_id:
    :return:
    """
    print(article_id)
    article_obj = models.Article.objects.filter(pk=article_id).first()
    comment_obj = models.Comment.objects.filter(article_id=article_id)
    return render(request, '07article_detail.html', locals())


import json

from django.db.models import F
from django.utils.safestring import mark_safe  # 模板语法标签


def UpAndDown(request):
    """
    点赞
    :param request:
    :return:
    """
    if request.is_ajax():
        if request.method == 'POST':
            back_dic = {'code': 1000, 'msg': ''}

            # 1.判断用户是否登录
            if request.user.is_authenticated:
                isUp = request.POST.get('isUp')
                article_id = request.POST.get('article_id')
                isUp = json.loads(isUp)
                print(isUp, type(isUp))

                # 2.判断用户点赞的当前文章是否是自己的文章
                article_obj = models.Article.objects.filter(pk=article_id).first()
                print(request.user == article_obj.blog.userinfo)
                if not (request.user == article_obj.blog.userinfo):

                    # 3.校验用户是否已经点过了
                    is_click = models.UpAndDown.objects.filter(user=request.user, article=article_id)
                    if not is_click:
                        # 4.操作文章数据库,更新记录
                        if isUp:
                            models.Article.objects.filter(pk=article_id).update(up_num=F('up_num') + 1)
                            back_dic['msg'] = '点赞成功'
                        else:
                            models.Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
                            back_dic['msg'] = '点踩成功'

                        # 5 操作点赞点彩表
                        models.UpAndDown.objects.create(user=request.user, article=article_obj, is_up=isUp)
                    else:
                        back_dic['code'] = 1001
                        back_dic['msg'] = '你已经点过了'
                else:
                    back_dic['code'] = 1002
                    back_dic['msg'] = '不能给自己点赞'
            else:
                back_dic['code'] = 1002
                back_dic['msg'] = '请先<a href="/login/">登录</a>'

            print(back_dic)
            return JsonResponse(back_dic)


from django.db import transaction


def comment(request):
    """
    评论
    :param request:
    :return:
    """
    if request.is_ajax():
        print(request.POST)
        if request.method == 'POST':
            back_dic = {'code': 1000, 'msg': ''}
            article_id = request.POST.get('article_id')
            content = request.POST.get('content')
            parent_id = request.POST.get('parent_id')

            print(request.POST)
            print(content)

            with transaction.atomic():
                models.Article.objects.filter(pk=article_id).update(comment_num=F('comment_num') + 1)
                models.Comment.objects.create(user=request.user, article_id=article_id, content=content,
                                              parent_id=parent_id)

            back_dic['msg'] = '评论成功！'
            print(back_dic)
            return JsonResponse(back_dic)


def backend(request):
    """
    后天管理
    :param request:
    :return:
    """
    article_obj_list = models.Article.objects.filter(blog=request.user.blog)
    return render(request, 'backend/02backend.html', locals())


from bs4 import BeautifulSoup


def add_article(request):
    """
    后台添加文章
    :param request:
    :return:
    """
    # 选择分类和标签内容
    category_obj_list = models.Category.objects.filter(blog=request.user.blog)
    tag_obj_list = models.Tag.objects.filter(blog=request.user.blog)

    if request.method == 'POST':

        # 获取内容
        title = request.POST.get('title')
        content = request.POST.get('comment')
        category = request.POST.get('category')
        tag_list = request.POST.getlist('tag')
        print(request.POST)
        print(tag_list)

        # 生成一个对象
        soup = BeautifulSoup(content, 'html.parser')
        # 获取所有的tag标签名称
        soup_list = soup.find_all()

        # 取出xxs攻击
        for tag in soup_list:
            if tag.name == 'script':
                # 删除script标签
                tag.decompose()
        # 截取文章信息
        desc = soup.text[0:150]

        # 添加文章内容
        article_obj = models.Article.objects.create(title=title, desc=desc, content=str(soup), blog=request.user.blog,
                                                    category_id=category)

        # 绑定标签关系
        tag_article_list = []
        for tag1 in tag_list:
            tag_article_list.append(models.ArticleTag(article=article_obj, tag_id=tag1))

        # 批量绑定标签内容, bulk_create效率高
        models.ArticleTag.objects.bulk_create(tag_article_list)

        return redirect('/backend/')

    return render(request, 'backend/03add_article.html', locals())


import os
from BBS import settings


def upload_img(request):
    """
//成功时
            {
                    "error" : 0,
                    "url" : "http://www.example.com/path/to/file.ext"
            }
            //失败时
            {
                    "error" : 1,
                    "message" : "错误信息"
            }
    :param request:
    :return:
    """
    if request.method == 'POST':
        back_dic = {'error': 0, 'message': ''}
        file_obj = request.FILES.get('imgFile')
        file_dir = os.path.join(settings.BASE_DIR, 'media', 'article_img')
        print(file_dir)
        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)
        # 凭借图片保存路径
        file_path = os.path.join(file_dir, file_obj.name)

        # 保存图片
        with open(file_path, 'wb') as f:
            for line in file_obj:
                f.write(line)
        back_dic['url'] = f'/media/article_img/{file_obj.name}/'
        print(back_dic)
        return JsonResponse(back_dic)


@login_required
def set_img(request):
    username = request.user.username
    if request.method == 'POST':
        img_obj = request.FILES.get('avatar')
        print(img_obj)
        # 上传头像,路径则不会包含路径不完整,
        # user_obj = models.UserInfo.objects.filter(username=request.user.username).update(avatar=img_obj)
        user_obj = models.UserInfo.objects.filter(username=request.user.username).first()
        user_obj.avatar = img_obj
        user_obj.save()
        print(user_obj)

    return render(request, '09set_img.html', locals())
