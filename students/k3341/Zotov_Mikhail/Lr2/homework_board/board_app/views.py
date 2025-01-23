from email.headerregistry import Group

from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import Http404, HttpResponseRedirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import User, Homework, GroupTeacher, Subject, UserHomework, StudyGroup


def home(request):
    return render(request, 'home.html')


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return HttpResponseRedirect('/success_registration')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect('/success_login')
        else:
            form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/')
    return render(request, 'logout.html')


def success_login(request):
    return render(request, 'success_login.html')


def success_register(request):
    return render(request, 'success_registration.html')


def show_homeworks(request):
    try:
        homeworks = Homework.objects.all()
    except Homework.DoesNotExist:
        raise Http404("Homeworks do not exist")

    return render(request, 'homeworks.html', {'homeworks': homeworks})


def show_grades(request):
    return render(request, 'grades.html')


def show_all_subjects_specific_group(request):
    try:
        if request.user.role == 'student' and request.user.group:
            study_group = request.user.group
            teachers = GroupTeacher.objects.filter(group__letter=study_group.letter,
                                                   group__group_grade=study_group.group_grade).values_list('teacher',
                                                                                                           flat=True)
            subjects = Subject.objects.filter(teacher__in=teachers)
    except GroupTeacher.DoesNotExist:
        raise Http404("Group Teachers do not exist")

    return render(request, 'subjects.html', {'subjects': subjects})


class AllGroups(ListView):
    model = StudyGroup
    template_name = 'groups.html'
    context_object_name = 'groups'
    ordering = ['group_grade', 'letter']


def group_detail(request, group_id):
    try:
        group = StudyGroup.objects.get(pk=group_id)
        students = User.objects.filter(group__letter=group.letter, group__group_grade=group.group_grade)
    except StudyGroup.DoesNotExist:
        raise Http404("Group does not exist")

    return render(request, 'group_detail.html', {'group': group, 'students': students})
