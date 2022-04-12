import pandas
import datetime
import panphon.distance
import IPA_soundex

dst = panphon.distance.Distance()

USE_ONLY_POPULAR_WORDS = False
USE_MULTY = False

def get_ipa_tables(lang='english'):
    # return 1. english IPA and 2. second language ipa
    if not USE_ONLY_POPULAR_WORDS and not USE_MULTY:
        myfile = open("data/freq_english_ipa.txt", encoding='utf-8')
    elif USE_ONLY_POPULAR_WORDS and USE_MULTY:
        myfile = open("data/4and5_pairs_english_ipa.txt", encoding='utf-8')
    else:
        myfile = open("data/english.csv")

    en_ipa = pandas.read_csv(myfile, encoding='utf-8', header=None,usecols=range(2))
    en_ipa.columns = ["orig", "ipa"]
    en_ipa = en_ipa.set_index("orig")
    en_ipa = en_ipa.dropna()
    en_ipa["soundex"] = en_ipa.apply(lambda row: IPA_soundex.convert(row["ipa"]), axis=1)

    if lang != 'english':
        if lang == 'french':
            filename = "data/french.txt"
        elif lang == "russian":
            filename = "data/russian.txt"
        elif lang == "spanish":
            filename = "data/espaniol.txt"
        elif lang == "esperanto":
            filename = "data/esperanto.txt"
        elif lang == "german":
            filename = "data/german.txt"
        elif lang == "hebrew":
            filename = "data/hebrew.txt"
        elif lang == "korean":
            filename = "data/korean.txt"
        myfile = open(filename, encoding='utf-8')
        ipa = pandas.read_csv(myfile, encoding='utf-8', header=None, usecols=range(2))
        ipa.columns = ["orig", "ipa"]
        ipa = ipa.set_index("orig")
        ipa = ipa.dropna()
        return ipa, en_ipa
    return en_ipa, en_ipa


def calc_matches(source_words, dst_function, lang='english'):
    source_ipa, en_ipa = get_ipa_tables(lang=lang)
    best_matches_arr = []
    src_phonim_arr = []
    src_soundex_arr = []

    for src_word in source_words:
        src_phonim = source_ipa.loc[src_word].values[0]
        soundex_src_word = IPA_soundex.convert(src_phonim)

        #a = datetime.datetime.now()
        en_ipa['distance'] = en_ipa.apply(lambda row: dst_function(src_phonim, row['ipa']), axis=1)
        en_ipa['distance_soundex'] = en_ipa.apply(lambda row : dst.fast_levenshtein_distance(soundex_src_word, row["soundex"]), axis = 1)
        #b = datetime.datetime.now()

        best_matches = en_ipa.sort_values(by=['distance_soundex', 'distance']).head(10)

        src_phonim_arr.append(src_phonim)
        src_soundex_arr.append(soundex_src_word)
        best_matches_arr.append(best_matches)

    return best_matches_arr, src_phonim_arr, src_soundex_arr


if __name__ == "__main__":
    pass

