from django.test import TestCase
import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wechatRecruit.settings')
import django
import pandas as pd

django.setup()
from recruit.utils import character_analysis
from recruit import tasks
from recruit.utils import upload

pd.set_option('display.max_columns', None)   #显示完整的列
pd.set_option('display.max_rows', None)  #显示完整的行

# Create your tests here.
if __name__ == '__main__':

    # obj = character_analysis.AnalyzeCharacter()
    # print(obj.execute(pk=26))
    # print(obj.execute(pk=27))
    # tasks.async_analysis(29)
    # upload.get_data(r"D:\test\试题.xls")
    tasks.check_token()