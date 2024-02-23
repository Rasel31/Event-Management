from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User, Student, Secretary, Moderator, Head
# Register your models here.


admin.site.register(User, UserAdmin)
admin.site.register(Head)
admin.site.register(Moderator)
admin.site.register(Secretary)
admin.site.register(Student)

