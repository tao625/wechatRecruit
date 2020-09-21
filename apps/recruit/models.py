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

    title = models.CharField(max_length=255, verbose_name="试卷名", null=False, unique=True)
    status = models.IntegerField(choices=status_type, verbose_name='是否发布', default=0)
    desc = models.TextField(verbose_name="问卷说明", null=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建者")

    def __str__(self):
        return self.title


class Question(BaseTable):
    """
    问题表
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
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建者")

    def __str__(self):
        return self.title

class Options(BaseTable):
    """
    选项表
    """

    class Meta:
        verbose_name = "选项"
        verbose_name_plural = verbose_name

    questionId = models.ForeignKey(Question, verbose_name="关联题目", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='选项名')

    def __str__(self):
        return self.title

class Submit(BaseTable):
    """
    提交信息表
    """

    class Meta:
        verbose_name = "提交信息"
        verbose_name_plural = verbose_name

    wjId = models.IntegerField(verbose_name='关联问卷id')
    submitIp = models.CharField(max_length=15, verbose_name='提交ip', null=False)
    submitUser = models.ForeignKey(Respondents, verbose_name="提交人", on_delete=models.CASCADE)
    useTime = models.IntegerField(verbose_name='填写用时')  # 单位：秒

    def __str__(self):
        return Wj.objects.filter(id=self.wjId).title

class Answer(BaseTable):
    """
    回答表
    """

    class Meta:
        verbose_name = "回答表"
        verbose_name_plural = verbose_name

    questionId = models.IntegerField(verbose_name='关联问题id')
    submitId = models.IntegerField(verbose_name='关联提交id')
    wjId = models.IntegerField(verbose_name='问卷id')
    type = models.CharField(max_length=20, verbose_name='题目类型')
    answer = models.IntegerField(verbose_name='答案', blank=True, null=True)
    answerText = models.TextField(verbose_name='文本答案', blank=True, null=True)

    def __str__(self):
        return Submit.objects.filter(id=self.submitId).submitUser