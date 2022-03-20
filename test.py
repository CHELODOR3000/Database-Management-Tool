import shelve
import numpy as np
import random
import string
import csv
from time import time


def generate_random_strings(num_of_surnames, length):
    surname_list = []
    letters = string.ascii_lowercase
    for j in range(num_of_surnames):
        rand_string = ''.join(random.choice(letters) for j in range(length))
        surname_list.append(rand_string)
    return surname_list


def generate_weights(num_of_iter):
    weight_list = []
    for j in range(num_of_iter):
        weight_list.append(str(random.randint(50, 100)))
    return weight_list


start = time()
with open("availableDB.csv", "r") as file:
    reader = csv.reader(file)
print("Время csv - ", time() - start)

start2 = time()
with shelve.open(f"ShelveData/test_10000", "w") as w_file:
    print("Открылось")
print("Время shelve - ", time() - start2)

'''
ID_10 = list(np.arange(1, 11))
ID_100 = list(np.arange(1, 101))
ID_1000 = list(np.arange(1, 1001))
'''
'''
fullname_10 = generate_random_strings(10, 8)
weight_category_10 = generate_weights(10)
sports_title_10 = generate_random_strings(10, 2)


with shelve.open('ShelveData/test_10') as m_file:
    i = 0
    while i < 10:
        m_file[str(i)] = [fullname_10[i], weight_category_10[i], sports_title_10[i]]
        i += 1

with shelve.open('ServiceFiles/test_10_service') as s_file:
    i = 0
    while i < 10:
        s_file[fullname_10[i]] = str(i)
        i += 1

with shelve.open('IDs/test_10_IDs') as IDs_file:
    IDs_file['ID'] = 10

with open("availableDB.csv", "a", encoding='utf-8') as file:
    writer = csv.writer(file, lineterminator="\r")
    writer.writerow(['test_10'])


fullname_100 = generate_random_strings(100, 8)
weight_category_100 = generate_weights(100)
sports_title_100 = generate_random_strings(100, 2)

with shelve.open('ShelveData/test_100') as m_file:
    i = 0
    while i < 100:
        m_file[str(i)] = [fullname_100[i], weight_category_100[i], sports_title_100[i]]
        i += 1

with shelve.open('ServiceFiles/test_100_service') as s_file:
    i = 0
    while i < 100:
        s_file[fullname_100[i]] = str(i)
        i += 1

with shelve.open('IDs/test_100_IDs') as IDs_file:
    IDs_file['ID'] = 100

with open("availableDB.csv", "a", encoding='utf-8') as file:
    writer = csv.writer(file, lineterminator="\r")
    writer.writerow(['test_100'])


fullname_1000 = generate_random_strings(1000, 8)
weight_category_1000 = generate_weights(1000)
sports_title_1000 = generate_random_strings(1000, 2)


with shelve.open('ShelveData/test_1000') as m_file:
    i = 0
    while i < 1000:
        m_file[str(i)] = [fullname_1000[i], weight_category_1000[i], sports_title_1000[i]]
        i += 1

with shelve.open('ServiceFiles/test_1000_service') as s_file:
    i = 0
    while i < 1000:
        s_file[fullname_1000[i]] = str(i)
        i += 1

with shelve.open('IDs/test_1000_IDs') as IDs_file:
    IDs_file['ID'] = 1000

with open("availableDB.csv", "a", encoding='utf-8') as file:
    writer = csv.writer(file, lineterminator="\r")
    writer.writerow(['test_1000'])


fullname_500 = generate_random_strings(500, 8)
weight_category_500 = generate_weights(500)
sports_title_500 = generate_random_strings(500, 2)


with shelve.open('ShelveData/test_500') as m_file:
    i = 0
    while i < 500:
        m_file[str(i)] = [fullname_500[i], weight_category_500[i], sports_title_500[i]]
        i += 1

with shelve.open('ServiceFiles/test_500_service') as s_file:
    i = 0
    while i < 500:
        s_file[fullname_500[i]] = str(i)
        i += 1

with shelve.open('IDs/test_500_IDs') as IDs_file:
    IDs_file['ID'] = 500

with open("availableDB.csv", "a", encoding='utf-8') as file:
    writer = csv.writer(file, lineterminator="\r")
    writer.writerow(['test_500'])
'''
