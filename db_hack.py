import random
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datacenter.models import Schoolkid, Subject, Lesson, Commendation, Mark, Chastisement


def get_child_name(name):
    try:
        return Schoolkid.objects.get(full_name__contains=name)
    except ObjectDoesNotExist:
        print(f'Ученик с именем "{name}" не найден.')
    except MultipleObjectsReturned:
        print(f'Найдено несколько учеников с именем "{name}".')
    return None


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    updated_count = bad_marks.update(points=5)
    print(f'Исправлено оценок: {updated_count}')


def remove_chastisements(schoolkid):
    deleted, _ = Chastisement.objects.filter(schoolkid=schoolkid).delete()
    print(f'Удалено замечаний: {deleted}')


def create_commendation(schoolkid_name, subject_title):
    kid = get_child_name(schoolkid_name)
    if not kid:
        return

    try:
        subject = Subject.objects.get(title=subject_title, year_of_study=kid.year_of_study)
    except Subject.DoesNotExist:
        print(f'Предмет "{subject_title}" для {kid.year_of_study} класса не найден.')
        return

    lesson = Lesson.objects.filter(
        subject=subject,
        year_of_study=kid.year_of_study,
        group_letter=kid.group_letter
    ).order_by('-date').first()

    if not lesson:
        print('Урок по этому предмету не найден.')
        return

    commendations = [
        'Молодец!',
        'Отлично!',
        'Хорошая работа!',
        'Ты меня приятно удивил!',
        'Замечательно!',
        'Великолепно!',
        'Прекрасно!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Уже существенно лучше!'
    ]

    Commendation.objects.create(
        text=random.choice(commendations),
        created=lesson.date,
        schoolkid=kid,
        subject=subject,
        teacher=lesson.teacher
    )

    print(f'Похвала добавлена для {kid.full_name} по предмету "{subject_title}".')
