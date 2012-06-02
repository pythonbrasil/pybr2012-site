# -*- coding: utf-8 -*-
from django.utils.translation import ugettext


ATTENDANT_CHOICES = (
    ('Student', ugettext('Student')),
    ('APyB', ugettext('APyB Associated')),
    ('Normal', ugettext('Normal'))
)

T_SHIRT_CHOICES = (
    (ugettext('Female'), (
            ('S', ugettext('S')),
            ('M', ugettext('M')),
            ('L', ugettext('L')),
        )
    ),
    ('Male', (
            ('S', ugettext('S')),
            ('M', ugettext('M')),
            ('L', ugettext('L')),
            ('XL', ugettext('XL')),
            ('XXL', ugettext('XXL')),
        )
    )
)

GENDER_CHOICES = (
    ('female', ugettext('Female')),
    ('male', ugettext('Male')),
    ('other', ugettext('Other'))
)

AGE_CHOICES = (
    ('--9', ugettext('9 or less')),
    ('10-19', '10-19'),
    ('20-29', '20-29'),
    ('30-39', '30-39'),
    ('40-49', '40-49'),
    ('50-59', '50-59'),
    ('60-69', '60-69'),
    ('70-79', '70-79'),
    ('80-+', ugettext('80 or more')),
)

PROFESSION_CHOICES = (
    ('student', ugettext('Student')),
    ('trainee', ugettext('Trainee')),
    ('developer', ugettext('Developer')),
    ('software engineer', ugettext('Software engineer')),
    ('manager', ugettext('Manager')),
    ('sysadmin', ugettext('Sysadmin')),
    ('teacher', ugettext('Teacher')),
    ('researcher', ugettext('Researcher')),
    ('other', ugettext('Other')),
)

LOCALE_CHOICES = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AM', 'Amazonas'),
    ('AP', 'Amapá'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MS', 'Mato Grosso do Sul'),
    ('MT', 'Mato Grosso'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('PR', 'Paraná'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('RS', 'Rio Grande do Sul'),
    ('SC', 'Santa Catarina'),
    ('SE', 'Sergipe'),
    ('SP', 'São Paulo'),
    ('TO', 'Tocantins'),
    ('00', ugettext('Other country'))
)
