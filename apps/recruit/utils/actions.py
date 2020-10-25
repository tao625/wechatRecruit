from . import logger
from recruit.tasks import async_analysis

def force_analysis(modeladmin, request, queryset):
    for obj in queryset:
        flag = async_analysis(pk=obj.id)
