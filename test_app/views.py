from decimal import Decimal

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
    Возвращает список объектов строительства с общей стоимостью работ и
    материалов для каждого объекта.

    Возвращает:
        list[dict]: Список словарей, содержащих информацию об объектах
        строительства и детали стоимости.

        Каждый словарь в списке имеет следующие ключи:
            - 'id': Идентификатор объекта строительства.
            - 'works_amount': Общая стоимость работ.
            - 'materials_amount': Общая стоимость материалов.
    Примерный результат функции:
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


## Задание 3
# Пользователь хочет применить скидку для секции на стоимость всех расценок
# внутри. Написать функцию, которая обновит поле price у всех расценок внутри
# секции с учётом этой скидки.

def update_with_discount(section_id: int, discount: Decimal):
    """
        Обновляет поле price у всех расценок внутри секции с учетом скидки.

    Аргументы:
        section_id (int): Идентификатор секции, внутри которой нужно применить скидку.
        discount (Decimal): Размер скидки в процентах от Decimal(0) до Decimal(100).
    """
    section = Section.objects.get(id=section_id)
    expenditures = Expenditure.objects.filter(section=section)
    for expenditure in expenditures:
        original_price = Expenditure.price
        discount_price = original_price * (Decimal(1) - discount / Decimal(100))
        expenditure.price = discount_price
        expenditure.save()
