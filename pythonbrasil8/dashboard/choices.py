ATTENDANT_CHOICES = (
    ('Student', 'Student'),
    ('APyB', 'APyB Associated'),
    ('Normal', 'Normal')
)

T_SHIRT_CHOICES = (
    ('Female', (
            ('P','P'),
            ('M', 'M'),
            ('G', 'G'),
        )
    ),
    ('Male', (
            ('P','P'),
            ('M', 'M'),
            ('G', 'G'),
            ('GG', 'GG'),
            ('GGX', 'GGX'),
        )
    )
)

GENDER_CHOICES = (
    ('female', 'female'),
    ('male', 'male'),
    ('transsexual', 'transsexual'),
    ('other', 'other')
)

AGE_CHOICES = (
    ('--9', '--9'),
    ('10-19', '10-19'),
    ('20-29', '20-29'),
    ('30-39', '30-39'),
    ('40-49', '40-49'),
    ('50-59', '50-59'),
    ('60-69', '60-69'),
    ('70-79', '70-79'),
    ('80-+', '80-+'),
)

PROFESSION_CHOICES = (
    ('student', 'student'),
    ('trainee', 'trainee'),
    ('developer', 'developer'),
    ('software engineer', 'software engineer'),
    ('manager', 'manager'),
    ('sys-admin', 'sys-admin'),
    ('teacher', 'teacher'),
    ('other', 'other'),
)
