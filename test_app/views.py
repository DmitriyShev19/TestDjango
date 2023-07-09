from django.shortcuts import render
from django.template.context_processors import request

from test_app.models import Building, Section, Expenditure


## Задание 1.
# Написать тело функции, которая для каждого конкретного объекта строительства
# будет возвращать список только родительских секций. У каждой родительской
# секции необходимо посчитать бюджет (стоимость всех расценок внутри).

def get_parent_sections(building_id: int) -> list[Section]:
    """
        Получает список родительских секций для определенного объекта
        строительства и вычисляет бюджет (стоимость всех расценок внутри) для
        каждой родительской секции.

        Аргументы:
            building_id (int): Идентификатор объекта строительства.

        Возвращает:
            list[Section]: Список родительских секций с вычисленным бюджетом.
        """
    parent_sections = Section.objects.filter(building_id=building_id, parent=None)

    for section in parent_sections:
        budget = 0
        expenditures = section.expenditure_set.all()
        for expenditure in expenditures:
            budget += expenditure.count * expenditure.price
        section.budget = budget
    return parent_sections


## Задание 2.
# Написать функцию, которая вернёт список объектов строительства, у каждого
# объекта строительства необходимо посчитать стоимость всех работ и стоимость
# всех материалов.


def get_buildings() -> list[dict]:
    """
    Ожидаемый результат функции:
    [
        {
            'id': 1,
            'works_amount': 100.00,
            'materials_amount': 200.00,
        },
        {
            'id': 2,
            'works_amount': 100.00,
            'materials_amount': 0.00,
        },
    ]
    """
    buildings = Building.objects.all()
    result = []

    for building in buildings:
        works_amount = 0
        materials_amount = 0

        sections = Section.objects.filter(building=building)
        for section in sections:
            expenditures = Expenditure.objects.filter(section=section)
            for expenditure in expenditures:
                if expenditure.type == Expenditure.Types.WORK:
                    works_amount += expenditure.count * expenditure.price
                elif expenditure.type == Expenditure.Types.MATERIAL:
                    materials_amount += expenditure.count * expenditure.price
        building_data = {
            'id': building.id,
            'works_amount': works_amount,
            'materials_amount': materials_amount,
        }
        result.append(building_data)
    return result

