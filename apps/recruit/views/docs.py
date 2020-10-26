from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def background_docs(request):
    """后台使用帮助文档啊"""
    return render(request, 'background_to_help_document.html')

def api_documentation(request):
    """API 接口文档"""
    return render(request, 'api_documentation.html')

