from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """用户信息 blank=True)  # blank告诉django admin后台管理 该字段可以为空 """
    phone = models.BigIntegerField(null=True, blank=True)  # 用户手机号

    # upload_to 该字段用来存放用户上传头像的文件路径， 用户上传头像会自动放到avatar文件夹下面
    avatar = models.FileField(upload_to='avatar', default='avatar/default.png')  # 用户头像

    create_time = models.DateField(auto_now_add=True)  # 创建时间

    # 用户表与个人站点是一对一的关系
    blog = models.OneToOneField(to='Blog', null=True)

    class Meta:
        # 会在表名后面添加s
        # verbose_name = '用户表'
        verbose_name_plural = '用户表UserInfo'

    def __str__(self):
        return self.username


class Blog(models.Model):
    """个人站点"""
    site_name = models.CharField(max_length=55)  # 站点名称
    site_title = models.CharField(max_length=66)  # 站点标题
    # 存css. js 文件路径用于模板样式
    site_theme = models.CharField(max_length=200)  # 站点模板样式

    class Meta:
        # 会在表名后面添加s
        # verbose_name = '用户表'
        verbose_name_plural = '个人站点Blog'

    def __str__(self):
        return self.site_name


class Category(models.Model):
    """分类"""
    name = models.CharField(max_length=32)  # 分类名称

    # 个人站点与分类是一对多的关系
    blog = models.ForeignKey(to='Blog', null=True)  # 设置外键

    class Meta:
        # 会在表名后面添加s
        # verbose_name = '用户表'
        verbose_name_plural = '分类表Category'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """标签"""
    name = models.CharField(max_length=32)  # 标签名称

    # 个人站点与分类是一对多的关系
    blog = models.ForeignKey(to='Blog', null=True)  # 设置外键

    class Meta:
        # 会在表名后面添加s
        # verbose_name = '用户表'
        verbose_name_plural = '标签Tag'

    def __str__(self):
        return self.name


class Article(models.Model):
    """文章信息"""
    title = models.CharField(max_length=64)  # 文章标题
    desc = models.CharField(max_length=255)  # 描述信息

    content = models.TextField()  # 存放大文本字段
    create_time = models.DateField(auto_now_add=True)  # 创建时间

    # 数据库优化，可以采用向表中添加需要的额外字段
    comment_num = models.BigIntegerField(default=0)  # 评论数据量
    up_num = models.BigIntegerField(default=0)  # 点赞个数
    down_num = models.BigIntegerField(default=0)  # 点彩个数

    # 外键字段

    # 个人站点和文章是一对多的关系
    blog = models.ForeignKey(to='Blog', null=True)

    # 分类和文章是一对多的关系, 一篇文章只能在一个分类下面,
    category = models.ForeignKey(to='Category', null=True)

    # 标签和文章是多对多的关系, 一片文章可以有多个标签对他进行定义
    # 第三张表可以添加额外的字段             创建的第三张表       在那个表中创建关系谁就在前面
    tag = models.ManyToManyField(to='Tag', through='ArticleTag', through_fields=('article', 'tag'))  # 可以天机

    class Meta:
        # 会在表名后面添加s
        # verbose_name = '用户表'
        verbose_name_plural = '文章Article'

    def __str__(self):
        return self.title


class ArticleTag(models.Model):
    """文章和标签的关系是多对多的关系"""
    article = models.ForeignKey(to='Article')
    tag = models.ForeignKey(to='Tag')

    class Meta:
        # 会在表名后面添加s
        # verbose_name = '用户表'
        verbose_name_plural = '多对多ArticleTag'


class UpAndDown(models.Model):
    """
    点赞，点彩表
     一张表中的一条数据能否对应另外一张表的多条数据
    另外一张表的一条数据能够对应当前的表多条件
      user_id        article_id               is_up
        1               1                           1
        1               2                           0
        1               3                           1
        2               1                           1
    """
    # 表关系
    # 用户和点赞点彩表是一对多关系
    user = models.ForeignKey(to='UserInfo')
    # 文章和点赞点彩表是一对多关系
    article = models.ForeignKey(to='Article')

    # 是否点赞或点彩
    is_up = models.BooleanField()  # 点赞,还是点彩

    class Meta:
        # 会在表名后面添加s
        # verbose_name = '用户表'
        verbose_name_plural = '点赞UpAndDown'

    def __str__(self):
        return self.is_up


class Comment(models.Model):
    # 表之间关系
    # 用户表和评论是一对多的关系
    user = models.ForeignKey(to='UserInfo')

    # 文章和评论是一对多的关系?
    article = models.ForeignKey(to='Article')

    content = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)

    # 添加外键字段, 一对多评论表   自关联 在评论时候可能会有子评论
    parent = models.ForeignKey(to='self', null=True)

    class Meta:
        # 会在表名后面添加s
        # verbose_name = '用户表'
        verbose_name_plural = '评论Comment'

    # def __str__(self):
    #     return self.is_up
