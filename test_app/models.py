from django.core.exceptions import ValidationError
from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Объект строительства'


class Section(models.Model):
    building = models.ForeignKey(Building, on_delete=models.PROTECT)
    parent = models.ForeignKey('self', on_delete=models.PROTECT,
                               verbose_name='Родительская секция',
                               blank=False, null=True)

    class Meta:
        verbose_name = 'Секция сметы'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id and self.parent and getattr(self.parent, 'parent', None):
            raise ValidationError('Максимальный уровень вложенности 2')
        super().save(force_insert, force_update, using, update_fields)


class Expenditure(models.Model):
    class Types:
        WORK = 'work'
        MATERIAL = 'material'
        choices = (
            (WORK, 'Работа'),
            (MATERIAL, 'Материал'),
        )

    section = models.ForeignKey(Section, on_delete=models.PROTECT,
                                help_text='Расценка может принадлежать только '
                                          'той секции, у которой указан parent'
                                )
    name = models.CharField(verbose_name='Название расценки', max_length=255)
    type = models.CharField(verbose_name='Тип расценки',
                            choices=Types.choices, max_length=8)
    count = models.DecimalField(verbose_name='Кол-во', max_digits=20,
                                decimal_places=8)
    price = models.DecimalField(verbose_name='Цена за единицу', max_digits=20,
                                decimal_places=2)

    class Meta:
        verbose_name = 'Расценка сметы'