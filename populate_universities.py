import os
import django
from datetime import datetime

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from django.db.utils import IntegrityError
from universities.models import (
    University, Major, Exam, 
    UniversityExamRequirement, ApplicationDeadline, 
    UniversityDeadline
)

def get_or_create_exam(exam_name):
    try:
        return Exam.objects.get(exam_name=exam_name)
    except Exam.DoesNotExist:
        print(f"⚠️ Экзамен {exam_name} не найден!")
        return None

def get_or_create_deadline_type(name):
    try:
        return ApplicationDeadline.objects.get(name=name)
    except ApplicationDeadline.DoesNotExist:
        print(f"⚠️ Тип дедлайна {name} не найден!")
        return None

def create_university(uni_data):
    uni, created = University.objects.get_or_create(
        name=uni_data['name'],
        defaults={
            'location': uni_data['location'],
            'founded_year': uni_data['founded_year'],
            'website_url': uni_data['website_url'],
            'description': uni_data['description']
        }
    )
    if created:
        print(f"✅ Добавлен университет: {uni.name}")
    else:
        print(f"⏩ Университет {uni.name} уже существует")
    return uni

def create_major(university, major_data):
    major, created = Major.objects.get_or_create(
        university=university,
        major_name=major_data['major_name'],
        degree_type=major_data['degree_type'],
        defaults={
            'duration': major_data['duration'],
            'tuition_fee': major_data.get('tuition_fee', 0)
        }
    )
    
    if created:
        print(f"  ✅ Добавлена программа: {major.major_name} ({major.degree_type})")
        
        # Требования к экзаменам
        for req in major_data.get('exam_requirements', []):
            exam = get_or_create_exam(req['exam'])
            if exam:
                UniversityExamRequirement.objects.get_or_create(
                    major=major,
                    exam=exam,
                    defaults={'min_score': req['min_score']}
                )
                print(f"    🔸 Требование: {exam.exam_name} ≥ {req['min_score']}")
        
        # Дедлайны
        for dl in major_data.get('deadlines', []):
            deadline_type = get_or_create_deadline_type(dl['type'])
            if deadline_type:
                try:
                    UniversityDeadline.objects.create(
                        university=university,
                        deadline=deadline_type,
                        start_date=dl['start'],
                        end_date=dl['end']
                    )
                    print(f"    📅 Дедлайн: {deadline_type.name} {dl['start']} - {dl['end']}")
                except IntegrityError:
                    print(f"    ⚠️ Дедлайн {deadline_type.name} уже существует")
    else:
        print(f"  ⏩ Программа {major_data['major_name']} уже существует")
    
    return major

def add_kazakhstan_universities():
    """Добавляем университеты Казахстана с расширенным списком программ"""
    kz_universities = [
        {
            'name': "Назарбаев Университет",
            'location': "Нур-Султан, Казахстан",
            'founded_year': 2010,
            'website_url': "https://nu.edu.kz",
            'description': "Ведущий исследовательский университет Казахстана с международными стандартами",
            'majors': [
                {
                    'major_name': "Компьютерные науки",
                    'degree_type': "Bachelor",
                    'duration': 4,
                    'tuition_fee': 8000,
                    'exam_requirements': [
                        {'exam': 'SAT', 'min_score': 1250},
                        {'exam': 'IELTS', 'min_score': 6.5}
                    ],
                    'deadlines': [
                        {'type': 'early', 'start': '2024-01-10', 'end': '2024-03-01'},
                        {'type': 'regular', 'start': '2024-03-02', 'end': '2024-05-01'}
                    ]
                },
                {
                    'major_name': "Бизнес-администрирование",
                    'degree_type': "Master",
                    'duration': 2,
                    'tuition_fee': 10000,
                    'exam_requirements': [
                        {'exam': 'GMAT', 'min_score': 550},
                        {'exam': 'IELTS', 'min_score': 6.5}
                    ],
                    'deadlines': [
                        {'type': 'regular', 'start': '2024-02-01', 'end': '2024-04-15'}
                    ]
                },
                {
                    'major_name': "Нефтегазовая инженерия",
                    'degree_type': "Bachelor",
                    'duration': 4,
                    'tuition_fee': 8500,
                    'exam_requirements': [
                        {'exam': 'SAT', 'min_score': 1200},
                        {'exam': 'IELTS', 'min_score': 6.0}
                    ],
                    'deadlines': [
                        {'type': 'early', 'start': '2024-01-10', 'end': '2024-03-01'}
                    ]
                }
            ]
        },
        {
            'name': "Казахский национальный университет им. Аль-Фараби",
            'location': "Алматы, Казахстан",
            'founded_year': 1934,
            'website_url': "https://www.kaznu.kz",
            'description': "Крупнейший классический университет Казахстана",
            'majors': [
                {
                    'major_name': "Международные отношения",
                    'degree_type': "Bachelor",
                    'duration': 4,
                    'tuition_fee': 3000,
                    'exam_requirements': [
                        {'exam': 'IELTS', 'min_score': 5.5}
                    ],
                    'deadlines': [
                        {'type': 'regular', 'start': '2024-06-01', 'end': '2024-08-25'}
                    ]
                },
                {
                    'major_name': "Химическая технология",
                    'degree_type': "Bachelor",
                    'duration': 4,
                    'tuition_fee': 3500,
                    'exam_requirements': [],
                    'deadlines': [
                        {'type': 'regular', 'start': '2024-06-01', 'end': '2024-08-25'}
                    ]
                },
                {
                    'major_name': "Филология",
                    'degree_type': "Master",
                    'duration': 2,
                    'tuition_fee': 4000,
                    'exam_requirements': [
                        {'exam': 'IELTS', 'min_score': 6.0}
                    ],
                    'deadlines': [
                        {'type': 'regular', 'start': '2024-05-15', 'end': '2024-07-15'}
                    ]
                }
            ]
        },
        {
            'name': "Южно-Казахстанский университет им. М. Ауэзова",
            'location': "Шымкент, Казахстан",
            'founded_year': 1975,
            'website_url': "https://www.ukgu.kz",
            'description': "Крупный региональный университет с техническим уклоном",
            'majors': [
                {
                    'major_name': "Информационные системы",
                    'degree_type': "Bachelor",
                    'duration': 4,
                    'tuition_fee': 2500,
                    'exam_requirements': [],
                    'deadlines': [
                        {'type': 'regular', 'start': '2024-07-01', 'end': '2024-09-01'}
                    ]
                },
                {
                    'major_name': "Строительная инженерия",
                    'degree_type': "Bachelor",
                    'duration': 4,
                    'tuition_fee': 2700,
                    'exam_requirements': [],
                    'deadlines': [
                        {'type': 'regular', 'start': '2024-07-01', 'end': '2024-09-01'}
                    ]
                }
            ]
        },
        {
            'name': "Карагандинский технический университет",
            'location': "Караганда, Казахстан",
            'founded_year': 1953,
            'website_url': "https://www.kstu.kz",
            'description': "Ведущий технический университет центрального Казахстана",
            'majors': [
                {
                    'major_name': "Горное дело",
                    'degree_type': "Bachelor",
                    'duration': 4,
                    'tuition_fee': 2800,
                    'exam_requirements': [],
                    'deadlines': [
                        {'type': 'regular', 'start': '2024-06-15', 'end': '2024-08-15'}
                    ]
                },
                {
                    'major_name': "Металлургия",
                    'degree_type': "Bachelor",
                    'duration': 4,
                    'tuition_fee': 2600,
                    'exam_requirements': [],
                    'deadlines': [
                        {'type': 'regular', 'start': '2024-06-15', 'end': '2024-08-15'}
                    ]
                }
            ]
        },
        {
            'name': "Евразийский национальный университет им. Л.Н. Гумилева",
            'location': "Нур-Султан, Казахстан",
            'founded_year': 1996,
            'website_url': "https://www.enu.kz",
            'description': "Крупный университет с акцентом на гуманитарные и социальные науки",
            'majors': [
                {
                    'major_name': "Международное право",
                    'degree_type': "Bachelor",
                    'duration': 4,
                    'tuition_fee': 3200,
                    'exam_requirements': [
                        {'exam': 'IELTS', 'min_score': 5.5}
                    ],
                    'deadlines': [
                        {'type': 'regular', 'start': '2024-06-10', 'end': '2024-08-20'}
                    ]
                },
                {
                    'major_name': "Журналистика",
                    'degree_type': "Bachelor",
                    'duration': 4,
                    'tuition_fee': 2900,
                    'exam_requirements': [],
                    'deadlines': [
                        {'type': 'regular', 'start': '2024-06-10', 'end': '2024-08-20'}
                    ]
                }
            ]
        }
    ]

    print("\n🔄 Добавляем университеты Казахстана...")
    for uni_data in kz_universities:
        university = create_university(uni_data)
        for major_data in uni_data['majors']:
            create_major(university, major_data)
    
    print("\n✅ Университеты Казахстана успешно добавлены!")

if __name__ == "__main__":
    add_kazakhstan_universities()