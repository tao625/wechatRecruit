from django.test import TestCase
import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wechatRecruit.settings')
import django


django.setup()
from recruit.utils import character_analysis

# Create your tests here.
if __name__ == '__main__':
    from recruit import models

    # print(character_analysis.get_charater_detail(1))

    answer = character_analysis.get_answer_choices(26)
    print(answer)

    scores = character_analysis.get_scores(answer)
    print(scores)
