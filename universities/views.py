from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Profile, University, SavedUniversity, Major, UniversityDeadline, Exam, UniversityExamRequirement, UserExamResult
from .forms import UserRegisterForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

def welcome_page(request):
    return render(request, 'universities/welcome.html')

def university_list(request):
    query = request.GET.get('q', '')
    selected_locations = request.GET.getlist('location')
    selected_majors = request.GET.getlist('major')
    
    # Извлечение фильтров по экзаменам
    exam_filters = {key.replace('exam_', ''): value for key, value in request.GET.items() if key.startswith('exam_')}

    universities = University.objects.all()

    # Фильтрация по названию университета
    if query:
        universities = universities.filter(name__icontains=query)

    # Фильтрация по локации
    if selected_locations:
        universities = universities.filter(location__in=selected_locations)

    # Фильтрация по специальностям
    if selected_majors:
        universities = universities.filter(majors__major_name__in=selected_majors)

    # Проверка, авторизован ли пользователь
    if request.user.is_authenticated:
        saved_universities = SavedUniversity.objects.filter(user=request.user).values_list('university_id', flat=True)
    else:
        saved_universities = []  # Пустой список для неавторизованных пользователей

    # Фильтрация по экзаменам
    if exam_filters:
        for exam_id, score in exam_filters.items():
            if score:
                universities = universities.filter(
                    majors__exam_requirements__exam_id=int(exam_id),  # Преобразование exam_id в число
                    majors__exam_requirements__min_score__lte=score
                )

    universities = universities.distinct()

    # Получение всех экзаменов для фильтров
    exams = Exam.objects.all()

    return render(request, 'universities/university_list.html', {
        'universities': universities,
        'query': query,
        'selected_locations': selected_locations,
        'selected_majors': selected_majors,
        'exams': exams,
        'saved_universities': saved_universities,
    })

def university_search(request):
    query = request.GET.get('q', '')
    selected_locations = request.GET.getlist('location')
    selected_majors = request.GET.getlist('major')

    universities = University.objects.all()

    # Фильтрация по названию университета
    if query:
        universities = universities.filter(name__icontains=query)

    # Фильтрация по локации
    if selected_locations:
        universities = universities.filter(location__in=selected_locations)

    # Фильтрация по специальностям
    if selected_majors:
        universities = universities.filter(majors__major_name__in=selected_majors)

    # Получение всех экзаменов
    exams = Exam.objects.all()

    # Динамическое получение уникальных локаций и программ из базы данных
    locations = University.objects.values_list('location', flat=True).distinct()
    programs = Major.objects.values_list('major_name', flat=True).distinct()

    return render(request, 'universities/university_search.html', {
        'universities': universities.distinct(),
        'query': query,
        'selected_locations': selected_locations,
        'selected_majors': selected_majors,
        'locations': locations,
        'programs': programs,
        'exams': exams,  # Передача экзаменов в шаблон
    })

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()

            # Сохранение данных профиля
            profile = user.profile
            profile.school_name = form.cleaned_data.get('school_name')
            profile.school_type = form.cleaned_data.get('school_type')
            profile.graduation_date = form.cleaned_data.get('graduation_date')
            profile.save()

            messages.success(request, 'Вы успешно зарегистрировались! Теперь вы можете войти.')
            return redirect('universities:login')
    else:
        form = UserRegisterForm()
    return render(request, 'universities/register.html', {'form': form})

def favorite_universities(request):
    saved_universities = SavedUniversity.objects.filter(user=request.user).select_related('university')
    deadlines = UniversityDeadline.objects.filter(university__in=[saved.university for saved in saved_universities])

    return render(request, 'universities/favorite_universities.html', {
        'saved_universities': saved_universities,
        'deadlines': deadlines,
    })

def remove_favorite(request, university_id):
    if request.method == 'POST':
        saved_university = get_object_or_404(SavedUniversity, university_id=university_id, user=request.user)
        saved_university.delete()
        return redirect('universities:favorite_universities')

def university_detail(request, university_id):
    university = get_object_or_404(University, id=university_id)
    return render(request, 'universities/university_detail.html', {'university': university})

def delete_exam_result(request, result_id):
    if request.method == 'POST':
        result = get_object_or_404(UserExamResult, id=result_id, user=request.user)
        result.delete()
        return redirect('universities:profile')
    
@login_required
def favorite_universities(request):
    saved_universities = SavedUniversity.objects.filter(user=request.user)
    return render(request, 'universities/favorite_universities.html', {'saved_universities': saved_universities})

@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        exam_id = request.POST.get('exam')
        score = request.POST.get('score')
        


        if exam_id and score:
            exam = Exam.objects.get(id=exam_id)
            UserExamResult.objects.create(user=request.user, exam=exam, score=score)
            return redirect('universities:profile')

    exams = Exam.objects.all()
    user_exam_results = UserExamResult.objects.filter(user=request.user)

    return render(request, 'universities/profile.html', {
        'exams': exams,
        'user_exam_results': user_exam_results,
        'profile': profile,
    })

@login_required
def save_university(request, university_id):
    university = get_object_or_404(University, id=university_id)
    SavedUniversity.objects.get_or_create(user=request.user, university=university)
    return redirect('universities:university_list')

@login_required
def remove_university(request, university_id):
    university = get_object_or_404(University, id=university_id)
    SavedUniversity.objects.filter(user=request.user, university=university).delete()
    return redirect('universities:university_list')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        # Обновление данных пользователя
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, 'Ваш профиль был успешно обновлен.')
        return redirect('universities:profile')

    return render(request, 'universities/edit_profile.html')

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        school_name = request.POST.get('school_name')
        school_type = request.POST.get('school_type')
        graduation_date = request.POST.get('graduation_date')

        # Обновление данных пользователя
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Обновление данных профиля
        profile.school_name = school_name
        profile.school_type = school_type
        profile.graduation_date = graduation_date
        profile.save()

        messages.success(request, 'Ваш профиль был успешно обновлен.')
        return redirect('universities:profile')

    return render(request, 'universities/edit_profile.html', {'profile': profile})

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()