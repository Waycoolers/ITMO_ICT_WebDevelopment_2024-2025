from django.contrib import admin
from .models import User, Subject, Homework, UserHomework, GroupTeacher, StudyGroup

admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Homework)
admin.site.register(UserHomework)
admin.site.register(GroupTeacher)
admin.site.register(StudyGroup)
