from django.contrib import admin
from .models import Page, Type, Stalker, HistoryType, History

# Register your models here.
admin.site.register(Page)
admin.site.register(Type)
admin.site.register(Stalker)
admin.site.register(History)
admin.site.register(HistoryType)