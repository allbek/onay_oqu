from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=100, blank=True, null=True)
    SCHOOL_TYPE_CHOICES = [
        ('high_school', 'Старшая школа'),
        ('middle_school', 'Средняя школа'),
        ('university', 'Университет'),
        ('other', 'Другое'),
    ]
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPE_CHOICES, blank=True, null=True)
    graduation_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class University(models.Model):
    name = models.CharField('Название', max_length=200)
    location = models.CharField('Местоположение', max_length=100)
    founded_year = models.IntegerField('Год основания', null=True, blank=True)
    website_url = models.URLField('Веб-сайт', max_length=200)
    description = models.TextField('Описание', blank=True)
    favorites = models.ManyToManyField(User, related_name='favorite_universities', blank=True)

    class Meta:
        verbose_name = 'Университет'
        verbose_name_plural = 'Университеты'
        ordering = ['name']

    def __str__(self):
        return self.name

class Major(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='majors')
    major_name = models.CharField('Название специальности', max_length=100)
    degree_type = models.CharField('Тип степени', max_length=50)
    duration = models.IntegerField('Длительность обучения (лет)')
    tuition_fee = models.DecimalField('Стоимость обучения', max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    def __str__(self):
        return f"{self.major_name} ({self.university.name})"

class Exam(models.Model):
    exam_name = models.CharField('Название экзамена', max_length=100)
    description = models.TextField('Описание', blank=True)
    min_possible_score = models.IntegerField('Минимально возможный балл')
    max_possible_score = models.IntegerField('Максимально возможный балл')

    class Meta:
        verbose_name = 'Экзамен'
        verbose_name_plural = 'Экзамены'

    def __str__(self):
        return self.exam_name

class UniversityExamRequirement(models.Model):
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name='exam_requirements')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    min_score = models.IntegerField('Минимальный проходной балл')

    class Meta:
        verbose_name = 'Требование к экзамену'
        verbose_name_plural = 'Требования к экзаменам'
        unique_together = ['major', 'exam']

    def __str__(self):
        return f"{self.major.major_name} - {self.exam.exam_name}: {self.min_score}"
    
class UserExamResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField('Результат экзамена')

    class Meta:
        verbose_name = 'Результат экзамена пользователя'
        verbose_name_plural = 'Результаты экзаменов пользователей'

    def __str__(self):
        return f"{self.user.username} - {self.exam.exam_name}: {self.score}"

class SavedUniversity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_universities')
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='saved_by_users')

    class Meta:
        verbose_name = 'Сохраненный университет'
        verbose_name_plural = 'Сохраненные университеты'
        unique_together = ['user', 'university']

    def __str__(self):
        return f"{self.user.username} - {self.university.name}"
    
class ApplicationDeadline(models.Model):
    
    DEADLINE_TYPES = [
        ('early', 'Ранняя подача'),
        ('regular', 'Обычная подача'),
        ('rolling', 'Подача на постоянной основе'),
        ('priority', 'Приоритетная подача'),
        ('deferred', 'Отложенная подача'),
        ('transfer', 'Подача для перевода'),
    ]

    name = models.CharField('Тип дедлайна', max_length=50, choices=DEADLINE_TYPES)
    description = models.TextField('Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Тип дедлайна'
        verbose_name_plural = 'Типы дедлайнов'

    def __str__(self):
        return dict(self.DEADLINE_TYPES).get(self.name, self.name)
    
class UniversityDeadline(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='application_deadlines')
    deadline = models.ForeignKey(ApplicationDeadline, on_delete=models.CASCADE, related_name='university_deadlines')
    start_date = models.DateField('Дата начала подачи', null=True, blank=True)
    end_date = models.DateField('Дата конца подачи', null=True, blank=True)

    class Meta:
        verbose_name = 'Дедлайн университета'
        verbose_name_plural = 'Дедлайны университетов'
        unique_together = ['university', 'deadline']

    def __str__(self):
        return f"{self.university.name} - {self.deadline.name}: {self.start_date} - {self.end_date}"