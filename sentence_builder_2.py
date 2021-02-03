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

def get_verbs():
    with open("polimorfologik-2.1.txt", encoding="utf-8") as file:
        verbs = []
        polimorfologik = file.readlines()
        for line in polimorfologik:
            match = re.search(r"(.*);(.*);([a-z]*):?([a-z]*:[a-z]*:[a-z0-9]*)?.?", line)
            if match.group(2):
                wordform = match.group(2)
                if match.group(3) == 'verb':
                    if match.group(4):
                        if match.group(4) == 'praet:sg:m1':
                            verbs.append(wordform)
    # print(objects)
    return verbs

def continuation_question():
    answer = input("Czy chcesz kontynuować? ")
    return answer

def build_sentence():
    subjects = get_subjects()
    objects = get_objects()
    verbs = get_verbs()
    number_subject = random.randint(0, len(subjects)-1)
    number_object = random.randint(0, len(objects)-1)
    number_verb = random.randint(0, len(verbs)-1)
    subject = subjects[number_subject]
    object = objects[number_object]
    verb = verbs[number_verb]
    sentence = f"{subject} {verb} {object}"
    print(sentence)
    answer = continuation_question()
    while answer == "tak":
        print(sentence)

# TODO: poprawny sposób na ten loop, tylko 3 osoba!

build_sentence()