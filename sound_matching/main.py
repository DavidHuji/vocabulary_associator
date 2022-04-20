import pandas
import panphon.distance

# for other languages -> https://github.com/open-dict-data/ipa-dict

lang = "en"
if lang == "en":
    src_word_arr = [ "limousines", "welsch", "something", "insulators", "tear", "informed", "chair", "sky", "cat", "sun"]
    filename = "data/en_US.txt"
elif lang == "ru":
    src_word_arr = ["дерево", "Александр"]
    filename = "data/ru.csv"
elif lang == "fr":
    src_word_arr = ["loger"]
    filename = "data/fr_FR.txt"

myfile = open(filename, encoding='utf-8')
ipa = pandas.read_csv(myfile, encoding='utf-8', header=None,usecols=range(2))
ipa.columns = ["orig", "ipa"]
ipa = ipa.set_index("orig")
ipa = ipa.dropna()

myfile = open("sound_matching/data/english.csv" if False else r"data\freq_english_ipa.txt", encoding='utf-8')
en_ipa = pandas.read_csv(myfile, encoding='utf-8', header=None,usecols=range(2))
en_ipa.columns = ["orig", "ipa"]
en_ipa = en_ipa.set_index("orig")
en_ipa = en_ipa.dropna()

dst = panphon.distance.Distance()
dst_function = dst.weighted_feature_edit_distance #dst.fast_levenshtein_distance#dst.feature_edit_distance#dst.hamming_feature_edit_distance

#print(dst.feature_edit_distance(ipa.loc['loon'].values[0],ipa.loc['moonlight'].values[0]))
for src_word in src_word_arr:
    src_phonim = ipa.loc[src_word].values[0]
    if lang=="ru":
        src_phonim = src_phonim[0]
    # src_phonim = "ˈnɑtˈpɑp"  # DBG
    import datetime
    a = datetime.datetime.now()
    en_ipa['distance'] = en_ipa.apply(lambda row : dst_function(src_phonim,row['ipa']), axis = 1)
    b = datetime.datetime.now()

    print("time to run",b-a,"for word |||  ", src_word, "   |||IPA",src_phonim)
    pandas.set_option('display.max_rows',100)

    a = datetime.datetime.now()
    en_ipa = en_ipa.sort_values(by=['distance'])
    b = datetime.datetime.now()
    print("time to sort",b-a,"for word |||  ",src_word,"   |||IPA",src_phonim)

    print(en_ipa.head(100))
