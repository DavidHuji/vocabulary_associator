import pandas
import datetime, panphon
import panphon.distance
import phonetics


dst = panphon.distance.Distance()
add_also_soundex = True
USE_ONLY_POPULAR_WORDS_AND_MULTI = True

popular_words_file = 'data/popular_words10000.txt'


def get_ipa_tables(lang='english'):
    # return 1. english IPA and 2. second language ipa
    myfile = open("data/english.csv" if not USE_ONLY_POPULAR_WORDS_AND_MULTI else "data/4and5_pairs_english_ipa.txt", encoding='utf-8')
    en_ipa = pandas.read_csv(myfile, encoding='utf-8', header=None,usecols=range(2))
    en_ipa.columns = ["orig", "ipa"]
    # en_ipa = en_ipa.set_index("orig")
    en_ipa = en_ipa.dropna()
    en_ipa["dm"] = en_ipa.apply(lambda row: phonetics.dmetaphone(row["orig"])[0], axis=1)
    if lang != 'english':
        if lang == 'french':
            filename = "data/fr_FR.txt"
        elif lang == "ru":
            filename = "data/ru.csv"
        elif lang == "spanish":
            filename = "data/espaniol.txt"
        elif lang == "esperanto":
            filename = "data/esperanto.txt"
        elif lang == "german":
            filename = "data/german.txt"
        myfile = open(filename, encoding='utf-8')
        ipa = pandas.read_csv(myfile, encoding='utf-8', header=None, usecols=range(2))
        ipa.columns = ["orig", "ipa"]
        ipa = ipa.set_index("orig")
        fr_ipa = ipa.dropna()
        return fr_ipa, en_ipa
    return en_ipa, en_ipa


def calc_matches(source_words, dst_function, lang='english'):
    source_ipa, en_ipa = get_ipa_tables(lang=lang)
    all_best_matches = []
    dm_src_word=0
    for src_word in source_words:
        if add_also_soundex:
            dm_src_word = phonetics.dmetaphone(src_word)[0]
        src_phonim = source_ipa.loc[src_word].values[0]

        if lang == "ru":
            src_phonim = src_phonim[0]
        # src_phonim = "ˈnɑtˈpɑp"  # DBG
        a = datetime.datetime.now()
        en_ipa['distance'] = en_ipa.apply(lambda row: dst_function(src_phonim, row['ipa']), axis=1)
        if add_also_soundex:
            en_ipa['distance_dm'] = en_ipa.apply(lambda row : dst.fast_levenshtein_distance(dm_src_word, row["dm"]), axis = 1)
        b = datetime.datetime.now()

        print("time to run", b - a, "for word |||  ", src_word, "   |||IPA", src_phonim)
        pandas.set_option('display.max_rows', 100)

        a = datetime.datetime.now()
        if add_also_soundex:
            # best_matches = en_ipa.loc[en_ipa['distance_dm'] == 0]
            best_matches = en_ipa.sort_values(by=['distance_dm']).head(100)
            print(f'amount of soundex matches for | {dm_src_word} |{len(best_matches)}')
            best_matches = best_matches.sort_values(by=['distance']).head(10)
            b = datetime.datetime.now()
        else:
            en_ipa = en_ipa.sort_values(by=['distance'])
            b = datetime.datetime.now()
            best_matches = str(en_ipa.head(10))
        all_best_matches.append(best_matches)
        print("\n\n\ntime to sort", b - a, "for word |||  ", src_word, "   |||IPA", src_phonim)

    return all_best_matches


if __name__ == "__main__":
    pass

