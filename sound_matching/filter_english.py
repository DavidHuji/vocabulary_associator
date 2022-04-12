import pandas
freq_words_whitelist_file = 'data/popular_words10000.txt'
short_words_whitelist_file = 'data/short_ipa.txt'
myfile = open("data/en_US.txt", encoding='utf-8')
ipa = pandas.read_csv(myfile, encoding='utf-8', header=None,usecols=range(2))
ipa.columns = ["orig", "ipa"]
ipa = ipa.set_index("orig")
ipa = ipa.dropna()

freq_words_whitelist = pandas.read_csv(freq_words_whitelist_file, header=None)[0].values
short_words_whitelist = pandas.read_csv(short_words_whitelist_file, header=None)[0].values

# filter
ipa_freq = ipa[ipa.index.isin(freq_words_whitelist)]
ipa_final = ipa_freq[(ipa_freq.index.str.len()>3) | (ipa_freq.index.isin(short_words_whitelist))]
ipa_final.to_csv('data/freq_english_ipa.txt', header=False)

