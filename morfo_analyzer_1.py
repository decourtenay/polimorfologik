import re

def get_input():
    entry = input("Podaj hasło ")
    entry_list = entry.split()
    return input_list


def analyzer():
    list_of_words = get_input()
    for word in list_of_words:
        f = open('polimorfologik-2.1.txt', 'r', encoding='utf-8')
        search_string = r".*;" + (re.escape(word)) + r";.*"
        description = re.findall(search_string, f.read())
        for element in description:
            analysis = []
            features = re.search(r"(.*);(.*);(.*):(..):(.*):(.*)+(.*)?:?(.*)?:?(.*)?:?(.*)?", element)
            # for group in features:
            #     analysis = analysis.append(features)
            print(analysis)

        print(description)


# # if group(1) = group(2) and subst = noun in nom sg., head
# if subst and nom pl = noun in nom pl, head
# if adjective and nom sg/pl = agreeing adjective
# if other noun = keep unchanged
# if pp = keep unchanged

# with open("polimorfologik-2.1.txt", encoding="utf-8") as file:
#     found = re.findall(r".*;psa;.*", file.read())
#     print(found)


analyzer()