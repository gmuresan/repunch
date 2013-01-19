from django.contrib import admin
from punchcode.models import Reward


class RewardAdmin(admin.ModelAdmin):
    model = Reward
    inlines = []

admin.site.register(Reward, RewardAdmin)
