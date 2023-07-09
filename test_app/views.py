from django.shortcuts import render
from django.template.context_processors import request

from test_app.models import Building, Section


## Задание 1.
# Написать тело функции, которая для каждого конкретного объекта строительства
# будет возвращать список только родительских секций. У каждой родительской
# секции необходимо посчитать бюджет (стоимость всех расценок внутри).

def get_parent_sections(building_id: int) -> list[Section]:
    parent_sections = Section.objects.filter(building_id=building_id, parent=None)

    for section in parent_sections:
        budget = 0
        expenditures = section.expenditure_set.all()
        for expenditure in expenditures:
            budget += expenditure.count * expenditure.price
        section.budget = budget
    return parent_sections

