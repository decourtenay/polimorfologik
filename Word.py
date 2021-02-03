class Word:
    def __init__(self, lemma):
        self.lemma = lemma



pies = Word("pies")
print(pies)
print(pies.lemma)

# Two possible architectures

# Word()
# Noun(Word)
# pies = Noun("pies")
#
# It has the relevant properties: caseforms, gender, etc.
# You create it from the lemma
# if there is no such lemma, return possible lemmas