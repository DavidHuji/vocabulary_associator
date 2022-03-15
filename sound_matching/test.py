import matcher

test_length = 2


def get_english_words_for_test():
    words_list = ["something", "tear", "informed", "chair", "sky", "cat", "sun"]
    return words_list


def get_french_words_for_test():
    words_list = ["femme", "homme", "ami", "maison", "monde", "travail", "école", "voyage", "livre", "lumière", "phrase"]
    return words_list


def get_russian_words_for_test():
    words_list = ["Авдей", "Алла", "порез", "узус", "уксус", "дерево", "Александр"]
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


def generic_test(dst_function="", lang='english'):
    dst_function = get_distance_function(dst_function)
    source_words = get_words_for_test(lang=lang)
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
    generic_test(dst_function="", lang='ru')
    generic_test(dst_function="", lang='french')

    print("\n\n\nfeature_edit_distance\n\n\n")
    generic_test(dst_function="feature_edit_distance", lang='ru')
    generic_test(dst_function="feature_edit_distance", lang='french')

    print("\n\n\nfast_levenshtein_distance\n\n\n")
    generic_test(dst_function="fast_levenshtein_distance", lang='ru')
    generic_test(dst_function="fast_levenshtein_distance", lang='french')

    print("\n\n\nhamming_feature_edit_distance\n\n\n")
    generic_test(dst_function="hamming_feature_edit_distance", lang='ru')
    generic_test(dst_function="hamming_feature_edit_distance", lang='french')
