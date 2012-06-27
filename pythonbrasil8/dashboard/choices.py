# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy


ATTENDANT_CHOICES = (
    ('Corporate', ugettext_lazy('Corporate')),
    ('Individual', ugettext_lazy('Individual')),
    ('Student', ugettext_lazy('Student')),
    ('APyB Associated', ugettext_lazy('APyB Associated'))
)

T_SHIRT_CHOICES = (
    (ugettext_lazy('Female'), (
            ('S', ugettext_lazy('S')),
            ('M', ugettext_lazy('M')),
            ('L', ugettext_lazy('L')),
        )
    ),
    (ugettext_lazy('Male'), (
            ('S', ugettext_lazy('S')),
            ('M', ugettext_lazy('M')),
            ('L', ugettext_lazy('L')),
            ('XL', ugettext_lazy('XL')),
            ('XXL', ugettext_lazy('XXL')),
        )
    )
)

GENDER_CHOICES = (
    ('female', ugettext_lazy('Female')),
    ('male', ugettext_lazy('Male')),
    ('other', ugettext_lazy('Other'))
)

AGE_CHOICES = (
    ('--9', ugettext_lazy('9 or less')),
    ('10-19', '10-19'),
    ('20-29', '20-29'),
    ('30-39', '30-39'),
    ('40-49', '40-49'),
    ('50-59', '50-59'),
    ('60-69', '60-69'),
    ('70-79', '70-79'),
    ('80-+', ugettext_lazy('80 or more')),
)

PROFESSION_CHOICES = (
    ('student', ugettext_lazy('Student')),
    ('trainee', ugettext_lazy('Trainee')),
    ('developer', ugettext_lazy('Developer')),
    ('software engineer', ugettext_lazy('Software engineer')),
    ('manager', ugettext_lazy('Manager')),
    ('sysadmin', ugettext_lazy('Sysadmin')),
    ('teacher', ugettext_lazy('Teacher')),
    ('researcher', ugettext_lazy('Researcher')),
    ('other', ugettext_lazy('Other')),
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
    ('00', ugettext_lazy('Other country'))
)
