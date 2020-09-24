from django.test import TestCase
import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wechatRecruit.settings')
import django


django.setup()
from recruit.utils import character_analysis

# Create your tests here.
if __name__ == '__main__':
    
    print(character_analysis.get_charater_detail(1))
