from django.contrib import admin
from .models import Predict, Comment

# Register your models here.
class PredictAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'created_at', 'updated_at',)


admin.site.register(Predict, PredictAdmin)
admin.site.register(Comment)
