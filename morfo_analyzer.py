import re

def get_input():
    entry = input("Podaj hasło ")
    entry_list = entry.split()
    return entry_list

def eliminate PP

def analyzer():
    list_of_words = get_input()
    first_word = list_of_words[0]
    first_word_search = r".*;" + (re.escape(first_word)) + r";.*"
    f1 = open('polimorfologik-sample.txt', 'r', encoding='utf-8')
    first_word_features = re.findall(first_word_search, f1.read())
    print(first_word_features)
    first_word_pos_list = []
    for element in first_word_features:
        if 'subst:sg:nom' in element:
            first_word_pos_list.append('head')
            print(first_word_pos_list)
    if list_of_words[1]:
        second_word = list_of_words[1]
        second_word_search = r".*;" + (re.escape(second_word)) + r";.*"
        f2 = open('polimorfologik-sample.txt', 'r', encoding='utf-8')
        second_word_features = re.findall(second_word_search, f2.read())
        print(second_word_features)
    if list_of_words[2]:
        third_word = list_of_words[2]
        third_word_search = r".*;" + (re.escape(third_word)) + r";.*"
        f3 = open('polimorfologik-sample.txt', 'r', encoding='utf-8')
        third_word_features = re.findall(third_word_search, f3.read())
        print(third_word_features)


    # f = open('polimorfologik-2.1.txt', 'r', encoding='utf-8')
    # search_string = r".*;" + (re.escape(first_word)) + r";.*"
    # description = re.findall(search_string, f.read())
    #
    #
    #
    # # With PP
    # if first_word in ['do', 'przy', 'na']:
    #     pp = first_word + ' ' + second_word
    #     noun = third_word
    #     print(pp)
    # elif second_word in ['do','przy','na']:
    #     pp = second_word + ' ' + third_word
    #     noun = first_word
    #     print(pp)
    # elif third_word in ['do','przy','na']:
    #     print(f"Error! In {list_of_words} the last word is a preposition")
    #
    #


# with open("polimorfologik-2.1.txt", encoding="utf-8") as file:
#     found = re.findall(r".*;psa;.*", file.read())
#     print(found)


analyzer()