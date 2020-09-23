from django.db import models
from users.models import User


# Create your models here.

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

    def __repr__(self):
        return "答题人"


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
    status = models.IntegerField(choices=status_type, verbose_name='是否发布', default=0)
    desc = models.TextField(verbose_name="问卷说明", null=True, blank=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建者")

    def __str__(self):
        return self.title

    def __repr__(self):
        return "问卷表"


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

    def __repr__(self):
        return "选项表"


class Question(BaseTable):
    """
    试题表
    """

    class Meta:
        verbose_name = "试题"
        verbose_name_plural = verbose_name

    q_type = (
        (1, "单选题"),
        (2, "多选题"),
        (3, "填空题"),
    )

    title = models.CharField(max_length=100, verbose_name='题目标题')
    type = models.IntegerField(verbose_name='题目类型', choices=q_type, default=1)
    wjId = models.ForeignKey(Wj, on_delete=models.CASCADE, verbose_name="所属问卷")
    must = models.BooleanField(verbose_name='是否必填')
    options = models.ManyToManyField(Options, verbose_name="选项")
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建者")

    def __str__(self):
        return self.title

    # def __repr__(self):
    #     return "试题表"


class Answer(BaseTable):
    """
    回答表
    """

    class Meta:
        verbose_name = "回答表"
        verbose_name_plural = verbose_name

    wj = models.ForeignKey(Wj, on_delete=models.CASCADE, verbose_name="问卷")
    submitIp = models.CharField(max_length=15, verbose_name='提交人IP', null=True, blank=True)
    submitUser = models.ForeignKey(Respondents, verbose_name="提交人", on_delete=models.CASCADE, null=True, blank=True)
    useTime = models.IntegerField(verbose_name='答题耗时', null=True, blank=True)  # 单位：秒
    answerChoice = models.CharField(verbose_name='选择题答案', blank=True, null=True, max_length=255)
    answerText = models.TextField(verbose_name='文本答案', blank=True, null=True)

    def __str__(self):
        return self.wj.title

    def __repr__(self):
        return "回答表"
