import re
import csv

polimorfologik = 'polimorfologik-2.1.txt'
input_file = 'input.txt'
output_file = 'output.txt'


def get_input(phrase):
    entry = phrase
    entry_preprocessed = entry.replace(';',' ')
    entry_list = entry_preprocessed.split()
    print('Processing entry' + entry_list[2])
    return entry_list


def find_pp(phrase):
    list_of_words = get_input(phrase)
    prepositions = ['o','od','ode','na','nad','nade','do','przy','przed','przede','po','pod','za','zza','ze','w','we',
                    'obok','około','koło','bez','beze','dla','poza','u']
    first_word = {'no.': '1', 'form': list_of_words[1], 'pos': ''}
    if len(list_of_words) > 2:
        second_word = {'no.': '2', 'form': list_of_words[2], 'pos': ''}
    else:
        second_word = {'no.': '2', 'form': '', 'pos': ''}
    if len(list_of_words) > 3:
        third_word = {'no.': '3', 'form': list_of_words[3], 'pos': ''}
    else:
        third_word = {'no.': '3', 'form': '', 'pos': ''}
    if len(list_of_words) > 4:
        fourth_word = {'no.': '4', 'form': list_of_words[4], 'pos': 'additional'}
    else:
        fourth_word = {'no.': '4', 'form': '', 'pos': ''}
    if len(list_of_words) > 5:
        fifth_word = {'no.': '5', 'form': list_of_words[5], 'pos': 'additional'}
    else:
        fifth_word = {'no.': '5', 'form': '', 'pos': ''}
    sixth_word = {'no.': '6', 'form': list_of_words[0], 'pos': 'additional'}
    if list_of_words[1] in prepositions:
        first_word['pos'] = 'prep'
        if len(list_of_words) > 2:
            second_word['pos'] = 'prep_comp'
    elif len(list_of_words) > 2:
        if list_of_words[2] in prepositions:
            second_word['pos'] = 'prep'
            if len(list_of_words) > 3:
                third_word['pos'] = 'prep_comp'
    list_of_words_pos = [first_word, second_word, third_word, fourth_word, fifth_word, sixth_word]
    return list_of_words_pos

def find_head(phrase):
    list_of_words_pos = find_pp(phrase)
    for word in list_of_words_pos:
        if word['pos'] not in ['prep', 'prep_comp']:
            word_search_string = r".*;" + (re.escape(word['form'])) + r";.*"
            f1 = open(polimorfologik, 'r', encoding='utf-8')
            word_features = re.findall(word_search_string, f1.read())
            for feature_set in word_features:
                feature_set_analysis = re.search(r"(.*?);(.*?);([a-z]*):?(..)?:?([a-zA-Z.]*)?:?([a-z0-9]*)?.*?",
                                                 feature_set)
                if feature_set_analysis.group(3) != 'ger':
                    if feature_set_analysis.group(3) == 'subst':
                        if feature_set_analysis.group(1) == feature_set_analysis.group(2):
                            word['pos'] = 'head_noun'
                            word['number'] = feature_set_analysis.group(4)
                            word['gender'] = feature_set_analysis.group(6)
                        elif feature_set_analysis.group(4) == 'pl':
                            plural_feature_set_analysis = re.search(r"pl:nom", feature_set)
                            if plural_feature_set_analysis is not None:
                                word['pos'] = 'head_noun'
                                word['form'] = feature_set_analysis.group(1)
                                word['number'] = 'sg'
                                word['gender'] = feature_set_analysis.group(6)
                    elif feature_set_analysis.group(3) == 'adj':
                        if word['pos'] != 'additional':
                            word['form'] = feature_set_analysis.group(1)
                            word['pos'] = 'adj_agreeing'
                            word['number'] = feature_set_analysis.group(4)
                            word['gender'] = feature_set_analysis.group(6)
                    else:
                        word['pos'] = 'compl'
                        word['number'] = feature_set_analysis.group(4)
                        word['gender'] = feature_set_analysis.group(6)
    return list_of_words_pos


def agreement(phrase):
    list_of_words_pos = find_head(phrase)
    for word in list_of_words_pos:
        if word['pos'] == 'head_noun':
            gender = word['gender']
            number = word['number']
            for adj in list_of_words_pos:
                if adj['pos'] == 'adj_agreeing':
                    adj['gender'] = gender
                    adj['number'] = number
    return list_of_words_pos


def find_forms(phrase):
    list_of_words_pos = agreement(phrase)
    plural_words = []
    for word in list_of_words_pos:
        forms_search_string = r"\b" + (re.escape(word['form'])) + r";.*"
        if word['pos'] in ['prep', 'prep_comp', '', 'compl', 'additional']:
            word['number'] = 'sg'
            for case in ['nom','gen','dat','acc','inst','loc','voc']:
                word[case] = word['form']
            word_pl = dict(word)
            word_pl['number'] = 'pl'
            plural_words.append(word_pl)
        elif word['pos'] == 'head_noun':
            f1 = open(polimorfologik, 'r', encoding='utf-8')
            case_forms = re.findall(forms_search_string,f1.read())
            for case in ['nom','gen','dat','acc','inst','loc','voc']:
                word[case] = word['form']
                case_form_search_string = r".*?;([^-]*?);subst:.*?" + word['number'] + r":.*?" + case + r":.*"
                for form in case_forms:
                    case_form = re.search(case_form_search_string,form)
                    if case_form is not None:
                        word[case] = case_form.group(1)
            if word['number'] == 'sg':
                word_pl = {}
                word_pl['no.'] = word['no.']
                word_pl['form'] = word['form']
                word_pl['nom'] = ''
            else:
                word_pl = dict(word)
                word_pl['number'] = 'pl'
                word = {}
                word['no.'] = word_pl['no.']
                word['form'] = word_pl['form']
                word['nom'] = ''
            if word_pl['nom'] == '':
                for case in ['nom', 'gen', 'dat', 'acc', 'inst', 'loc', 'voc']:
                    word_pl[case] = word['form']
                    case_form_search_string = r".*?;([^-]*?);subst:.*?pl:" + case + r":.*"
                    for form in case_forms:
                        case_form = re.search(case_form_search_string, form)
                        if case_form is not None:
                            word_pl[case] = case_form.group(1)
            elif word['nom'] == '':
                for case in ['nom', 'gen', 'dat', 'acc', 'inst', 'loc', 'voc']:
                    word[case] = word['form']
                    case_form_search_string = r".*?;([^-]*?);subst:sg:" + case + r":.*"
                    for form in case_forms:
                        case_form = re.search(case_form_search_string, form)
                        if case_form is not None:
                            word[case] = case_form.group(1)
            word_pl['pos'] = 'head_noun'
            word['pos'] = 'head_noun'
            word_pl['number'] = 'pl'
            word['number'] = 'sg'
            plural_words.append(word_pl)
        elif word['pos'] == 'adj_agreeing':
            word['number'] = 'sg'
            word_pl = {}
            word_pl['number'] = 'pl'
            word_pl['gender'] = word['gender']
            word_pl['no.'] = word['no.']
            f1 = open(polimorfologik, 'r', encoding='utf-8')
            case_forms = re.findall(forms_search_string,f1.read())
            for case in ['nom','gen','dat','acc','inst','loc','voc']:
                word[case] = word['form']
                case_form_search_string = r".*?;([^-]*?);.*?adj:sg:.*?" + case + r".*?" + word['gender'] + r".*?:pos"
                for form in case_forms:
                    case_form = re.search(case_form_search_string,form)
                    if case_form is not None:
                        word[case] = case_form.group(1)
            for case in ['nom','gen','dat','acc','inst','loc','voc']:
                word_pl[case] = word['form']
                case_form_search_string = r".*?;([^-]*?);.*?adj:pl:[a-z.]*?" + case + r"[a-z.]*?:[a-z0-9.]*?" \
                                          + word['gender'] + r"[a-z0-9.]*?:pos"
                for form in case_forms:
                    case_form = re.search(case_form_search_string,form)
                    if case_form is not None:
                        word_pl[case] = case_form.group(1)
            plural_words.append(word_pl)
    final_forms_sg = {}
    final_forms_pl = {}
    first_sg = list_of_words_pos[0]
    second_sg = list_of_words_pos[1]
    third_sg = list_of_words_pos[2]
    fourth_sg = list_of_words_pos[3]
    fifth_sg = list_of_words_pos[4]
    mid = list_of_words_pos[5]
    type = list_of_words_pos[6]
    first_pl = plural_words[0]
    second_pl = plural_words[1]
    third_pl = plural_words[2]
    fourth_pl = plural_words[3]
    fifth_pl = plural_words[4]
    for case in ['nom', 'gen', 'dat', 'acc', 'inst', 'loc', 'voc']:
        if second_sg[case] == '':
            final_forms_sg[case] = first_sg[case]
        elif third_sg[case] == '':
            final_forms_sg[case] = first_sg[case] + ' ' + second_sg[case]
        elif fourth_sg[case] == '':
            final_forms_sg[case] = first_sg[case] + ' ' + second_sg[case] + ' ' + third_sg[case]
        elif fifth_sg[case] == '':
            final_forms_sg[case] = first_sg[case] + ' ' + second_sg[case] + ' ' + third_sg[case] + ' ' + fourth_sg[
                case]
        else:
            final_forms_sg[case] = first_sg[case] + ' ' + second_sg[case] + ' ' + third_sg[case] + ' ' + fourth_sg[
                case] + ' ' + fifth_sg[case]
    for case in ['nom', 'gen', 'dat', 'acc', 'inst', 'loc', 'voc']:
        if second_pl[case] == '':
            final_forms_pl[case] = first_pl[case]
        elif third_pl[case] == '':
            final_forms_pl[case] = first_pl[case] + ' ' + second_pl[case]
        elif fourth_pl[case] == '':
            final_forms_pl[case] = first_pl[case] + ' ' + second_pl[case] + ' ' + third_pl[case]
        elif fifth_pl[case] == '':
            final_forms_pl[case] = first_pl[case] + ' ' + second_pl[case] + ' ' + third_pl[case] + ' ' + fourth_pl[
                case]
        else:
            final_forms_pl[case] = first_pl[case] + ' ' + second_pl[case] + ' ' + third_pl[case] + ' ' + fourth_pl[
                case] + ' ' + fifth_pl[case]
    final_forms_sg_str = mid['form'] + ';' + type['form'] + ';' + final_forms_sg['nom'] + ';' + 'singular' + ';' \
                         + final_forms_sg['nom'] + ';' + final_forms_sg['gen'] + ';' + final_forms_sg['dat'] + ';' \
                         + final_forms_sg['acc'] + ';' + final_forms_sg['inst'] + ';' + final_forms_sg['loc'] + ';' \
                         + final_forms_sg['voc'] + '\n'
    final_forms_pl_str = mid['form'] + ';' + type['form'] + ';' + final_forms_sg['nom'] + ';' + 'plural' + ';' \
                         + final_forms_pl['nom'] + ';' + final_forms_pl['gen'] + ';' + final_forms_pl['dat'] + ';' \
                         + final_forms_pl['acc'] + ';' + final_forms_pl['inst'] + ';' + final_forms_pl['loc'] + ';' \
                         + final_forms_pl['voc'] + '\n'
    with open(output_file, 'a', encoding='utf-8') as output_data:
        output_data.write(final_forms_sg_str)
        output_data.write(final_forms_pl_str)


def morpho_analyzer():
    processed_list = []
    with open(input_file, 'r+', encoding='utf-8') as input_data:
        for phrase in input_data.readlines():
            if phrase not in processed_list:
                find_forms(phrase)


if __name__ == '__main__':
    morpho_analyzer()








