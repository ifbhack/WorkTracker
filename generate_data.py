from random import *
from string import ascii_lowercase

def random_year(start_year, end_year):
    new_year = randint(start_year, end_year)
    date_month = randint(1,12)
    if len(str(date_month)) != 2:
        date_month = str(date_month).zfill(2)
    date_day = randint(1, 30)
    if len(str(date_day)) != 2:
        date_day = str(date_day).zfill(2)
    return str(new_year) + "-" + str(date_month) + "-" + str(date_day)

print(random_year(2002, 2010))

## Recursive function doing the same thing (for fun)
# name = ''
# def random_letter(num = 1):
#     global name
#     if num == 0:
#         return name.capitalize()
#     else:
#         letter = choice(ascii_lowercase)
#         name = name + letter
#         return random_letter(num - 1)

def random_letter(num = 1):
    gen_name = ''
    while num > 1:
        letter = choice(ascii_lowercase)
        gen_name = gen_name + letter
        num = num - 1
    return gen_name.capitalize()

remake = random_letter(randint(3, 9))

print(remake)