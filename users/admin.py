from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Transaction


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'salary', 'financial_goal', 'is_staff']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'date')
    list_filter = ('transaction_type', 'date')
    search_fields = ('user__username', 'description')


admin.site.register(CustomUser, CustomUserAdmin)
