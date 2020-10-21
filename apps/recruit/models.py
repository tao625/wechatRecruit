import binascii
import os

from django.db import models
from django.utils.html import format_html
from django.utils.encoding import python_2_unicode_compatible
from users.models import User
from rest_framework.authtoken.models import Token

# Create your models here.

@python_2_unicode_compatible
class BaseTable(models.Model):
    """
    公共字段序列
    """

    class Meta:
        abstract = True
        verbose_name = "公共字段序列"
        db_table = "BaseTable"

    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)


@python_2_unicode_compatible
class Respondents(BaseTable):
    """
    答题人
    """

    class Meta:
        verbose_name = "答题人"
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=255, verbose_name="姓名", null=False)
    email = models.CharField(max_length=30, verbose_name='个人邮箱', null=True)
    phone = models.CharField(verbose_name="手机号", null=False, max_length=15)
    intention_position = models.CharField(max_length=255, verbose_name='应聘职位', help_text='请填写应聘职位')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class RespondentToken(BaseTable):
    """自定义答题者Token"""
    class Meta:
        verbose_name = "Respondent Token"
        verbose_name_plural = verbose_name

    key = models.CharField(max_length=200, verbose_name="key", primary_key=True)
    respondents = models.OneToOneField(Respondents, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key() + '_' + str(self.respondents.id)
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

@python_2_unicode_compatible
class Wj(BaseTable):
    """
    问卷表
    """

    class Meta:
        verbose_name = "试卷"
        verbose_name_plural = verbose_name

    status_type = (
        (0, "未发布"),
        (1, "已发布"),
    )

    title = models.CharField(max_length=255, verbose_name="试卷名", unique=True)
    wj_alias = models.CharField(max_length=255, verbose_name="试卷别名", unique=True, null=True)
    status = models.IntegerField(choices=status_type, verbose_name='是否发布', default=0)
    desc = models.TextField(verbose_name="问卷说明", null=True, blank=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建者")
    type = models.IntegerField(verbose_name="分析类型", null=True)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Options(BaseTable):
    """
    选项表
    """

    class Meta:
        verbose_name = "选项"
        verbose_name_plural = verbose_name

    title = models.CharField(max_length=100, verbose_name='选项名')
    score = models.IntegerField(verbose_name="分数", null=True, blank=True)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Animal(BaseTable):
    """
    性格别名
    """
    class Meta:
        verbose_name = "性格别名"
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=100, verbose_name='性格别名')
    wj = models.ForeignKey(Wj, verbose_name="问卷", on_delete=models.CASCADE, null=True)
    feature = models.TextField(verbose_name='性格特征', null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Character(BaseTable):
    """
    性格分析
    """
    class Meta:
        verbose_name = "性格分析"
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="名称")
    animal = models.OneToOneField(Animal, null=True, blank=True, on_delete=models.CASCADE, help_text="仅PDP性格测试需要选择", verbose_name="性格别名")
    content = models.TextField(verbose_name='主要表现', null=True, blank=True)
    professional = models.TextField(verbose_name='代表职业', null=True, blank=True)
    wj = models.ForeignKey(Wj, on_delete=models.CASCADE, verbose_name="试卷", null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Question(BaseTable):
    """
    试题表
    """

    class Meta:
        verbose_name = "试题"
        verbose_name_plural = verbose_name
        unique_together = [["qid", "wjId"]]

    q_type = (
        (1, "单选题"),
        (2, "多选题"),
        (3, "主观题"),
    )
    qid = models.IntegerField(verbose_name='题目序号', null=True)
    title = models.CharField(max_length=100, verbose_name='题目标题')
    type = models.IntegerField(verbose_name='题目类型', choices=q_type, default=1)
    wjId = models.ForeignKey(Wj, on_delete=models.CASCADE, verbose_name="所属问卷")
    must = models.BooleanField(verbose_name='是否必填')
    options = models.ManyToManyField(Options, verbose_name="选项")
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建者")
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, null=True, blank=True, verbose_name='动物')

    def __str__(self):
        return self.title



@python_2_unicode_compatible
class Answer(BaseTable):
    """
    回答表
    """

    class Meta:
        verbose_name = "答卷"
        verbose_name_plural = verbose_name

    wj = models.ForeignKey(Wj, on_delete=models.CASCADE, verbose_name="问卷")
    submit_ip = models.CharField(max_length=15, verbose_name='提交人IP', null=True, blank=True)
    submit_user = models.ForeignKey(Respondents, verbose_name="提交人", on_delete=models.CASCADE, null=True, blank=True)
    use_time = models.IntegerField(verbose_name='答题耗时', null=True, blank=True)  # 单位：秒
    answer_choice = models.TextField(verbose_name='选择题答案', blank=True, null=True)
    answer_text = models.TextField(verbose_name='主观题答案', blank=True, null=True)

    def __str__(self):
        return self.wj.title


@python_2_unicode_compatible
class AnalysisData(BaseTable):
    """存储一些性格分析的资料信息,

    """
    class Meta:
        verbose_name = "性格分析资料"
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=255, verbose_name="文件名", null=True)
    tags = models.ManyToManyField(Animal, verbose_name="标记")
    content = models.TextField(verbose_name="内容", null=True, blank=True)
    wj = models.ManyToManyField(Wj, verbose_name="试卷")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Report(BaseTable):
    class Meta:
        verbose_name = "分析报告"
        verbose_name_plural = verbose_name

    respondenter = models.ForeignKey(Respondents, on_delete=models.CASCADE, verbose_name='答题者')
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE, verbose_name='答卷')
    result = models.TextField(verbose_name='最终报告', null=True, blank=True)

    def __str__(self):
        return self.result


@python_2_unicode_compatible
class UploadFile(BaseTable):
    class Meta:
        verbose_name = "批量添加试题"
        verbose_name_plural = verbose_name

    status_type = (
        (1, "存在"),
        (2, "已删除"),
    )

    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='excel_data', unique=True, null=True, blank=True)
    status = models.IntegerField(choices=status_type, default=1, verbose_name="文档是否存在")
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建者", null=True)

    def __str__(self):
        return self.name