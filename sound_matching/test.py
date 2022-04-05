import matcher, gpt3

test_length = 2


def get_english_words_for_test():
    words_list = ["something", "tear", "informed", "chair", "sky", "cat", "sun"]
    return words_list


def get_french_words_for_test():
    words_list = ["femme", "homme", "ami", "maison", "monde", "travail", "école", "voyage", "livre", "lumière", "phrase"]
    return words_list


def french_test_with_translation():
    words_list = [("avoir", "possession"), ("pas", "footstep"), ("pouvoir", "power"), ("son", "sound"),
                  ("dire", "saying"), ("devoir", "duty"), ("avant", "front"), ("deux", "two"), ("bien", "good"),
                  ("fois", "time"), ("nouveau", "new"), ("vouloir", "desire"), ("moins", "minus"), ("temps", "time"), ("savoir", "knowledge"),
                  ("raison", "reason"), ("monde", "world"), ("jour", "day"), ("monsieur", "mister")]
    return [w[0] for w in words_list], [w[1] for w in words_list]


def get_russian_words_for_test():
    words_list = ["Авдей", "Алла", "порез", "узус", "уксус", "дерево", "Александр"]
    return words_list


def get_spanish_words_for_test():
    words_list = ["abane", "malo", "mujer", "hombre", "ciudad", "partir", "feliz"]
    return words_list


def get_german_words_for_test():
    words_list = ["werden", "zwei", "zwischen", "sagte", "Netzwerk", "zurecht", "geschieht"]
    return words_list


def get_esperanto_words_for_test():
    words_list = ["viro", "doni", "knabo", "geodo", "kapo", "lernejo", "arbo"]
    return words_list


def print_matches(source_words, matches):
    for i in range(len(source_words)):
        print('\n\nsource_word:  ', source_words[i])
        print('matches\n', matches[i])


def save_matches_to_file(source_words, matches, lang):
    pass


def get_words_for_test(lang='english'):
    if lang == 'english':
        return get_english_words_for_test()
    elif lang == 'french':
        return get_french_words_for_test()
    elif lang == 'ru':
        return get_russian_words_for_test()
    elif lang == 'spanish':
        return get_spanish_words_for_test()
    elif lang == 'esperanto':
        return get_esperanto_words_for_test()
    elif lang == 'german':
        return get_german_words_for_test()
    pass


def get_distance_function(name=""):
    import panphon.distance
    dst = panphon.distance.Distance()

    if name == "":
        return dst.weighted_feature_edit_distance  #dst.fast_levenshtein_distance#dst.feature_edit_distance#dst.hamming_feature_edit_distance
    elif name == "fast_levenshtein_distance":
        return dst.fast_levenshtein_distance  #dst.fast_levenshtein_distance#dst.feature_edit_distance#dst.hamming_feature_edit_distance
    elif name == "feature_edit_distance":
        return dst.feature_edit_distance  #dst.fast_levenshtein_distance#dst.feature_edit_distance#dst.hamming_feature_edit_distance
    elif name == "hamming_feature_edit_distance":
        return dst.hamming_feature_edit_distance  #dst.fast_levenshtein_distance#dst.feature_edit_distance#dst.hamming_feature_edit_distance


def create_sentence_and_image_and_save(triples_of_words, language=''):
    print(triples_of_words)
    for triple in triples_of_words:
        general_sentence = f'the_meaning_of_{triple[2]}_in_{language}_is_{triple[1]}_but_it_sounds_like_{triple[0]}_SO_REMEMBER-'
        gpt3.deployment_get_sentence_and_image(triple[0], triple[1], general_sentence)


def generic_test(dst_function="", lang='english', with_gpt=False):
    print(f'start test of {lang} with {dst_function}')
    dst_function = get_distance_function(dst_function)
    source_words = get_words_for_test(lang=lang)
    if with_gpt:
        source_words, translations = french_test_with_translation()
        matches = matcher.calc_matches(source_words, dst_function, lang=lang)
        best_matches = [m.head(1)['orig'].values[0] for m in matches]
        tripels = [(best_matches[i], translations[i], source_words[i]) for i in range(len(best_matches))]
        create_sentence_and_image_and_save(tripels, language=lang)
    else:
        matches = matcher.calc_matches(source_words, dst_function, lang=lang)
        print_matches(source_words, matches)
        save_matches_to_file(source_words, matches, lang=lang)


def english_test():
    generic_test(lang='english')


def french_test():
    generic_test(lang='french')


def russian_test():
    generic_test(lang='ru')


def spanish_test():
    generic_test(lang='spanish')


def esperanto_test():
    generic_test(lang='esperanto')


def german_test():
    generic_test(lang='german')


def run_few_languages_test():
    languages = ["english", "ru", "french", "spanish", "esperanto", "german"]
    for l in languages:
        generic_test(lang=l)


if __name__ == '__main__':
    generic_test(dst_function="", lang='french', with_gpt=True)
    exit()
    generic_test(dst_function="", lang='french')
    generic_test(dst_function="", lang='spanish')
    generic_test(dst_function="", lang='esperanto')
    generic_test(dst_function="", lang='german')
    generic_test(dst_function="", lang='english')
    exit()
    generic_test(dst_function="", lang='ru')

    print("\n\n\nfeature_edit_distance\n\n\n")
    generic_test(dst_function="feature_edit_distance", lang='ru')
    generic_test(dst_function="feature_edit_distance", lang='french')

    print("\n\n\nfast_levenshtein_distance\n\n\n")
    generic_test(dst_function="fast_levenshtein_distance", lang='ru')
    generic_test(dst_function="fast_levenshtein_distance", lang='french')

    print("\n\n\nhamming_feature_edit_distance\n\n\n")
    generic_test(dst_function="hamming_feature_edit_distance", lang='ru')
    generic_test(dst_function="hamming_feature_edit_distance", lang='french')
