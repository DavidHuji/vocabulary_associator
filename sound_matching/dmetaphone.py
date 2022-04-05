import pandas
import panphon.distance
import phonetics
lang="fr"
if lang=="en":
    src_word_arr = ["chair","sky","cat","sun"]
    filename = "en_US.txt"
elif lang=="ru":
    src_word_arr = ["дерево","Александр"]
    filename = "ru.csv"
elif lang=="fr":
    src_word_arr = ["femme", "homme", "ami", "maison", "monde", "travail", "école", "voyage", "livre", "lumière", "phrase"]
    filename = "data/fr_FR.txt"

myfile = open(filename, encoding='utf-8')
ipa = pandas.read_csv(myfile, encoding='utf-8', header=None,usecols=range(2))
ipa.columns = ["orig", "ipa"]
ipa = ipa.set_index("orig")
ipa = ipa.dropna()


myfile = open("data/english.csv", encoding='utf-8')
en_ipa = pandas.read_csv(myfile, encoding='utf-8', header=None,usecols=range(2))
en_ipa.columns = ["orig", "ipa"]
en_ipa = en_ipa.dropna()
en_ipa["dm"] = en_ipa.apply(lambda row : phonetics.dmetaphone(row["orig"])[0], axis = 1)


dst = panphon.distance.Distance()

for src_word in src_word_arr:
    dm_src_word = phonetics.dmetaphone(src_word)[0]
    src_phonim = ipa.loc[src_word].values[0]

    import datetime
    a = datetime.datetime.now()
    en_ipa['distance_dm'] = en_ipa.apply(lambda row: dst.fast_levenshtein_distance(dm_src_word, row["dm"]), axis=1)
    en_ipa['distance_ipa'] = en_ipa.apply(lambda row: dst.weighted_feature_edit_distance(src_phonim, row['ipa']), axis=1)

    b = datetime.datetime.now()

    print("time to run",b-a,"for word",src_word,"dmataphone",dm_src_word,"IPA",src_phonim)
    pandas.set_option('display.max_rows',100)
    en_ipa_dist0 = en_ipa.loc[en_ipa['distance_dm'] == 0]
    en_ipa_dist0 = en_ipa_dist0.sort_values(by=['distance_ipa'])
    print(en_ipa_dist0.head(100))
