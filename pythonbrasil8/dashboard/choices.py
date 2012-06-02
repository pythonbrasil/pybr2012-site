# -*- coding: utf-8 -*-
from django.utils.translation import ugettext


ATTENDANT_CHOICES = (
    ('Student', ugettext('Student')),
    ('APyB', ugettext('APyB Associated')),
    ('Normal', ugettext('Normal'))
)

T_SHIRT_CHOICES = (
    (ugettext('Female'), (
            ('P', ugettext('P')),
            ('M', ugettext('M')),
            ('G', ugettext('G')),
        )
    ),
    ('Male', (
            ('P', ugettext('P')),
            ('M', ugettext('M')),
            ('G', ugettext('G')),
            ('GG', ugettext('GG')),
            ('GGX', ugettext('GGX')),
        )
    )
)

GENDER_CHOICES = (
    ('female', ugettext('Female')),
    ('male', ugettext('Male')),
    ('other', ugettext('Other'))
)

AGE_CHOICES = (
    ('--9', ugettext('<=9')),
    ('10-19', ugettext('10-19')),
    ('20-29', ugettext('20-29')),
    ('30-39', ugettext('30-39')),
    ('40-49', ugettext('40-49')),
    ('50-59', ugettext('50-59')),
    ('60-69', ugettext('60-69')),
    ('70-79', ugettext('70-79')),
    ('80-+', ugettext('>=80')),
)

PROFESSION_CHOICES = (
    ('student', ugettext('Student')),
    ('trainee', ugettext('Trainee')),
    ('developer', ugettext('Developer')),
    ('software engineer', ugettext('Software engineer')),
    ('manager', ugettext('Manager')),
    ('sysadmin', ugettext('Sysadmin')),
    ('teacher', ugettext('Teacher')),
    ('other', ugettext('Other')),
)
