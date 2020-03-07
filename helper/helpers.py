import os
# import datetime

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

RELIGION = (
    ('Islam', 'Islam'),
    ('Chriian', 'Christian'),
    ('African Tradition', 'ATR'),
    ('Others', 'Others'),
)


SUGGESTION_CATEGORY = (
    ('Teachers', 'Teachers'),
    ('Class Room', 'Class Room'),
    ('Academics', 'Academic'),
    ('Others', 'Others'),
)

LEVELS = (('JHS', 'JHS'), ('UP', 'UPPER_PRIMARY'),
          ('LP', 'LOWER PRIMARY'), ('PS', 'PRE_SCHOOL'))

CLASS_LEVELS = (
    ('JHS', ('JHS 0NE', 'JHS TWO', 'JHS THREE'), ),
    ('UPPER', ('PRIMARY FOUR', 'PRIMARY FIVE', 'PRIMARY SIX'), ),
    ('LOWER', ('PRIMARY THREE', 'PRIMARY TWO', 'PRIMARY ONE')),
    ('PRE_SCHOOL', ('CRECHE', 'KG ONE', 'KG TWO')),
)

CLASSES = (
    ('JHS 0NE', 'JHS 0NE'),
    ('JHS TWO', 'JHS TWO'),
    ('JHS THREE', 'JHS THREE'),
    ('PRIMARY SIX', 'PRIMARY SIX'),
    ('PRIMARY FIVE', 'PRIMARY FIVE'),
    ('PRIMARY FOUR', 'PRIMARY FOUR'),
    ('PRIMARY THREE', 'PRIMARY THREE'),
    ('PRIMARY TWO', 'PRIMARY TWO'),
    ('PRIMARY ONE', 'PRIMARY ONE'),
)

HOUSES = (
    ('0NE', '0NE'),
    ('TWO', 'TWO'),
    ('THREE', 'THREE'),
    ('FOUR', 'FOUR'),
    ('NOT ASSIGNED', 'NOT ASSIGNED'),
)


SOME_CHOICES = [
    ('db-value', 'Display Value'),
    ('db-value2', 'Display Value2'),
    ('db-value3', 'Display Value3'),
]

# datetime.date('Y')

INTS_CHOICES = [tuple([x, x]) for x in range(0, 100)]

YEARS = [x for x in range(2010, 2031)]

AC_YEARS = (
    ('2014/2015', '2014/2015'),
    ('2015/2016', '2015/2016'),
    ('2016/2017', '2016/2017'),
    ('2017/2018', '2017/2018'),
    ('2018/2019', '2018/2019'),
    ('2019/2020', '2019/2020'),
    ('2020/2021', '2020/2021'),
    ('2021/2022', '2021/2022'),
)

STAFF_TYPE = (
    ('Class Teacher', 'CLASS TEACHER'),
    ('School Cook', 'SCHOOL COOK'),
    ('School Electrician', 'SCHOOL ELECTRICIAN'),
    # ('', ''),
    # ('', ''),
)

STAFF_CATEGORY = (
    ('Teaching', 'TEACHING'),
    ('Non-Teaching', 'NON-TEACHING'),
    # ('Cook', 'COOK'),
    # ('Electrician', 'ELECTRICIAN'),
    # ('', ''),
    # ('', ''),
)

TERMS_LIST = (
    ('First Term', 'FIRST TERM'),
    ('Second Term', 'SECOND TERM'),
    ('Third Term', 'THIRD TERM'),
)

TERMS_LIST_NUMERIC = (
    ('1', 1),
    ('2', 2),
    ('3', 3),
)

PAYMENT_MODE = (
    ('Cash ', 'CASH'),
    ('Bank Draft', 'BANK DRAFT'),
    ('CHECK', 'CHECK'),
)
# colors
ALL_COLORS = (
    ('White', 'White'),
    ('Yellow', 'Yellow'),
    ('Blue', 'Blue'),
    ('Red', 'Red'),
)
MAIN_COLORS = (
    ('White', 'White'),
    ('Yellow', 'Yellow'),
    ('Blue', 'Blue'),
    ('Red', 'Red'),
)

SUBJECTS_LIST = (
    ('ENGLISH LANGUAGE', 'ENGLISH LANGUAGE'),
    ('MATHEMATICS', 'MATHEMATICS'),
    ('INTER SCIENCE', 'INTERGRATED SCIENCE'),
    ('NATURAL SCIENCE', 'NATURAL SCIENCE'),
    ('SOCIAL STUDIES', 'SOCIAL STUDIES'),
    ('INFORMATION and COMMUNICATION TECHNOLOGY',
     'INFORMATION and COMMUNICATION TECHNOLOGY'),
    ('RELIGIOUS and MORAL EDUCATION', 'RELIGIOUS and MORAL EDUCATION'),
    ('BASIC DESIGN and TECHNOLOGY', 'BASIC DESIGN and TECHNOLOGY'),
    ('FRENCH', 'FRENCH'),
    ('GHANAIAN LANGUAGE and CULTURE', 'GHANAIAN LANGUAGE and CULTURE'),
    ('CITIZENSHIP EDUCATION', 'CITIZENSHIP EDUCATION'),
    ('CREATIVE ART', 'CREATIVE ART'),
    ('PHYSICAL EDUCATION', 'PHYSICAL EDUCATION'),
)

SUBJECTS_CAT = (
    ('CORE', (
        ('vinyl', 'Vinyl'),
        ('cd', 'CD'),
    )
    ),
    ('ELECTIVES', (
        ('vhs', 'VHS Tape'),
        ('dvd', 'DVD'),
    )
    ),
)

ADDRESS_TYPE_CHOICES = (
    ('Permanent', 'Permanent'),
    ('Current', 'Current'),
    ('Temporary', 'Temporary'),
)
BLOOD_GROUP_CHOICES = (
    ('A1 -ve', 'A1 Negative '),
    ('A1 +ve', 'A1 Positive '),
    ('A1B -ve', 'A1B Negative '),
    ('A1B +ve', 'A1B Positive '),
    ('A2 -ve', 'A2 Negative '),
    ('A2 +ve', 'A2 Positive '),
    ('A2B -ve', 'A2B Negative '),
    ('A2B +ve', 'A2B Positive '),
    ('B -ve', 'B Negative '),
    ('B +ve', 'B Positive '),
    ('B1 +ve', 'B1 Positive '),
    ('O -ve', 'O Negative '),
    ('O +ve', 'O Positive ')
)

USER_TYPE = (('S', 'Student'), ('T', 'Teacher'),
             ('C', 'Contractor'), ('E', 'Employee'))
PHONE_CONNECTION_TYPE_CHOICES = (('M', 'Mobile Number'), ('F', 'Fixed Line'), )

PHONE_NUMBER_TYPE_CHOICES = (
    ('P', 'Personal'), ('E', 'Emergency'), ('H', 'Home'), )

MEDIA_CHOICES = (
    ('Audio', (
        ('vinyl', 'Vinyl'),
        ('cd', 'CD'),
    )
    ),
    ('Video', (
        ('vhs', 'VHS Tape'),
        ('dvd', 'DVD'),
    )
    ),
    ('unknown', 'Unknown'),
)
