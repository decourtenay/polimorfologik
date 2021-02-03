import re

# # Return lemma
# with open("polimorfologik-2.1.txt", encoding="utf-8") as file:
#     wordform = input(" Podaj słowo ")
#     polimorfologik = file.readlines()
#     for line in polimorfologik:
#         match = re.search(r"(.*);(.*);(.*)", line)
#         if wordform == match.group(2):
#             lemma = match.group(1)
#             print(f"Forma podstawowa słowa '{wordform}' to '{lemma}'")
#             if re.search("subst", match.group(3)):
#                 print("Jest to rzeczownik")


def get_info(wordform):
    with open("polimorfologik-2.1.txt", encoding="utf-8") as file:
        polimorfologik = file.readlines()
        for line in polimorfologik:
            match = re.search(r"(.*);(.*);(.*):?(.*)", line)
            if wordform == match.group(2):
                lemma = match.group(1)
                pos = "subst"
                print(f"Forma podstawowa słowa '{wordform}' to '{lemma}', jest to {pos}")
                # return lemma, pos

# Return statement terminates the loop


get_info("mam")