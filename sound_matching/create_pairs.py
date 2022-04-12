import pandas
import panphon.distance

freq_words = ['a', 'bout', 'cause', 'course', 'house']
popular_words_file = 'data/popular_words10000.txt'
filename = "data/en_US.txt"
myfile = open(filename, encoding='utf-8')
ipa = pandas.read_csv(myfile, encoding='utf-8', header=None,usecols=range(2))
ipa.columns = ["orig", "ipa"]
ipa = ipa.set_index("orig")
ipa = ipa.dropna()

with open(popular_words_file, "r") as pop_f:
    lines = pop_f.readlines()

freq_words = [w[:-1] for w in lines]


eng_words = ipa.index.tolist()
ipas = ipa.values.tolist()
new_words = []
short_words = []

length_thresholds_min, length_thresholds_max = 4, 5
ipa_dict = ipa.to_dict()['ipa']
for i, w in enumerate(freq_words):
    if w in ipa_dict:
        t = (str(w), str(ipa_dict[w]))
        new_words.append(t)
        if length_thresholds_min <= len(ipa_dict[w]) <= length_thresholds_max:
            short_words.append(t)

for i, w1 in enumerate(short_words):
    for j, w2 in enumerate(short_words[i+1:]):
        new_words.append((w1[0] + ' ' + w2[0], str(w1[1] + w2[1])))

with open('data/4and5_pairs_english_ipa.txt', 'w') as the_file:
    for i, t in enumerate(new_words):
        s = t[0] + ', ' + t[1] + '\n'
        the_file.write(s)
    print('length=', i)
