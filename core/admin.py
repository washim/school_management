from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from django.forms import CheckboxSelectMultiple
from django.db import models
from core.models import Student, StudentPayment, Expense, Transaction, Config, Teacher


class StudentsImageFilter(admin.SimpleListFilter):
    title = 'Photo Exist'
    parameter_name = 'photo_exist'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'no':
            return queryset.filter(photo="")
        
        if self.value() == 'yes':
            return queryset.exclude(photo="")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_filter = ["identity_card_issued", StudentsImageFilter]
    actions = ["make_idcard_issued"]
    
    @admin.action(description="Mark ID Card Issued for selected")
    def make_idcard_issued(self, request, queryset):
        updated = queryset.update(identity_card_issued="yes")
        self.message_user(
            request,
            ngettext(
                "%d student was successfully marked as idcard issued.",
                "%d students were successfully marked as idcard issued.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


@admin.register(StudentPayment)
class StudentPaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Expense._meta.get_fields()]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Transaction._meta.get_fields()]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ["key", "value"]