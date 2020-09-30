from django.test import TestCase
import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wechatRecruit.settings')
import django


django.setup()
from recruit.utils import character_analysis
from recruit import tasks

# Create your tests here.
if __name__ == '__main__':

    # obj = character_analysis.AnalyzeCharacter()
    # print(obj.execute(pk=26))
    # print(obj.execute(pk=27))
    tasks.async_analysis(29)