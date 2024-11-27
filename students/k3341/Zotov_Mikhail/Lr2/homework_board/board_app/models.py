from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    GROUP_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='student')
    group = models.CharField(max_length=10, choices=GROUP_CHOICES, blank=True, null=True)

    def clean(self):
        if self.role == 'student' and not self.group:
            raise ValidationError('You must select a group')

    def save(self, *args, **kwargs):
        if not self.is_superuser:
            self.clean()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class Subject(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    start_date = models.DateField()
    deadline = models.DateTimeField(null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    penalty = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.subject} - {self.text}"


class UserHomework(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    submission_datetime = models.DateTimeField(auto_now_add=True)
    solution = models.TextField(max_length=1000)
