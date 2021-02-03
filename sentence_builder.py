import re
import random


def get_subjects():
    with open("polimorfologik-2.1.txt", encoding="utf-8") as file:
        subjects = []
        polimorfologik = file.readlines()
        for line in polimorfologik:
            match = re.search(r"(.*);(.*);([a-z]*):?(.*)", line)
            wordform = match.group(2)
            if wordform.lower() == wordform:
                if match.group(3) == 'subst':
                    if match.group(4):
                        if match.group(4) == 'sg:nom:m1':
                            subjects.append(wordform)
        # print(subjects)
    return subjects


def get_objects():
    with open("polimorfologik-2.1.txt", encoding="utf-8") as file:
        objects = []
        polimorfologik = file.readlines()
        for line in polimorfologik:
            match = re.search(r"(.*);(.*);([a-z]*):?(.*)", line)
            wordform = match.group(2)
            if wordform.lower() == wordform:
                if match.group(3) == 'subst':
                    if match.group(4):
                        if match.group(4) == 'sg:acc:m1':
                            objects.append(wordform)
    # print(objects)
    return objects


def build_sentence():
    verb = input("Podaj czasownik ")
    subjects = get_subjects()
    objects = get_objects()
    number_subject = random.randint(0, len(subjects)-1)
    number_object = random.randint(0, len(objects)-1)
    subject = subjects[number_subject]
    object = objects[number_object]
    sentence = f"{subject} {verb} {object}"
    print(sentence)


build_sentence()