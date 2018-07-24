from django.contrib import admin

# Register your models here.
from dashcodrf.models import Client, BranchUser, RoutePlan, RoutePlanLog, Branch, Account

admin.site.register(Client)
admin.site.register(BranchUser)
admin.site.register(RoutePlan)
admin.site.register(RoutePlanLog)
admin.site.register(Branch)
admin.site.register(Account)
