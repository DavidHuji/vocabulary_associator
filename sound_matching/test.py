import matcher, gpt3, images
from pathlib import Path
import datetime
from data.words_for_test import get_top_20nouns_test


USE_TOP_20_NOUNS = True


def english_test_with_translation():
    orig = ["kiwi","something", "tear", "informed", "chair", "sky", "cat", "sun"]
    return orig, orig


def korean_test_with_translation():
    orig = ["오늘", "년", "주", "초", "시계", "가다", "웃다", "보다", "멀리", "작은"]
    trans = ["Today", "Year", 'week', 'second', 'clock', "go", 'laugh', "see", "far", "small"]
    challenging_words = ["사용하다", "만들다", "못생긴"]
    challenging_trans = ["use", "make", "ugly"]
    return orig + challenging_words, trans + challenging_trans


def french_test_with_translation():
    orig = ["baguette", "dire", "rire", "petit", "belle", "monde", "jour", "bon", "seul", "fille", "ami", "argent"]
    trans = ["bread", "say", "laugh", "small", "beautiful", "world", "day", "good", "alone", "daughter", "friend", "money"]
    challenging_words = ["avoir", "pas", "pouvoir", "son"]
    challenging_trans = ["have", "not", "can", "sound"]
    return orig + challenging_words, trans + challenging_trans


def hebrew_test_with_translation():
    orig = ["גרון", "עיר", "סוס", "ילד", "מקרר", "כיסא", "כלב"]
    trans = ["throat", "city", "hourse", "boy", "fridge", "chair", "dog"]
    challenging_words = ["שקד", "שלג", "במקום", "גלויה", "זהב", "כתיבה"]
    challenging_trans = ["almond","snow", "instead", "postcard", "gold", "writing"]
    return orig + challenging_words, trans + challenging_trans


def russian_test_with_translation():
    orig = ["мужчина", "порез", "уксус", "дерево", "Александр"]
    trans = ["male", "cut", "viniger", "tree", "alexander"]
    challenging_words = []
    challenging_trans = []
    return orig + challenging_words, trans + challenging_trans


def spanish_test_with_translation():
    orig = ["abane", "malo", "mujer", "hombre", "ciudad", "partir", "feliz"]
    trans =["abandon", "bad", "woman", "man", "city", "depart", "happy"]
    challenging_words = []
    challenging_trans = []
    return orig + challenging_words, trans + challenging_trans


def german_test_with_translation():
    orig = ["werden", "zwei", "zwischen", "sagte", "Netzwerk", "zurecht", "geschieht"]
    trans = ["become", "two", "between", "said", "network", "rightly", "happens"]
    challenging_words = []
    challenging_trans = []
    return orig + challenging_words, trans + challenging_trans


def esperanto_test_with_translation():
    orig = ["viro", "doni", "knabo", "kapo", "lernejo", "arbo"]
    trans = ["man", "give", "boy", "head", "school", "tree"]
    challenging_words = []
    challenging_trans = []
    return orig + challenging_words, trans + challenging_trans


def get_words_for_test(lang='english'):
    if USE_TOP_20_NOUNS:
        return get_top_20nouns_test(lang)
    if lang == 'english':
        return english_test_with_translation()
    elif lang == 'french':
        return french_test_with_translation()
    elif lang == 'russian':
        return russian_test_with_translation()
    elif lang == 'spanish':
        return spanish_test_with_translation()
    elif lang == 'esperanto':
        return esperanto_test_with_translation()
    elif lang == 'german':
        return german_test_with_translation()
    elif lang == 'hebrew':
        return hebrew_test_with_translation()
    elif lang == 'korean':
        return korean_test_with_translation()
    pass


def get_distance_function(name="weighted_feature_edit_distance"):
    import panphon.distance
    dst = panphon.distance.Distance()

    if name == "weighted_feature_edit_distance":
        return dst.weighted_feature_edit_distance
    elif name == "fast_levenshtein_distance":
        return dst.fast_levenshtein_distance
    elif name == "feature_edit_distance":
        return dst.feature_edit_distance
    elif name == "hamming_feature_edit_distance":
        return dst.hamming_feature_edit_distance

def log_to_file(str, filename):
    print (str)
    with open(f"logs/{filename}",  mode='a', encoding='utf-8') as text_file:
        text_file.write(str+"\n")

def generate_file_name():
    Path("./logs").mkdir(parents=True, exist_ok=True)
    format_data = "%d_%m_%y_%H_%M_%S"
    log_filename = f"log{datetime.datetime.now().strftime(format_data)}.txt"
    return log_filename

def image_to_pdf(log_filename):
    html_path = "logs/"+log_filename.replace(".txt", ".html")
    pdf_path = "logs/"+log_filename.replace(".txt", ".pdf")
    with open("logs/"+log_filename, 'r', encoding='utf-8') as file:
        filedata = file.read()

    filedata = filedata.replace('\n', '<br>\n')

    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(filedata)


def generic_test(dst_function="weighted_feature_edit_distance", lang='english',
                 gen_sentence=True, gen_image=False, max_matches=2, log_filename=generate_file_name()):


    # log_to_file(f'<h1>start test of {lang.upper()} with {dst_function}, \n'\
    #             f'generate sentence = {gen_sentence}, generate image = {gen_image}\n'
    #             f'file {log_filename}</h1>\n', log_filename)

    dst_function = get_distance_function(dst_function)
    src_words_arr, translations_arr = get_words_for_test(lang)

    matches, src_phonim_arr, src_soundex_arr = matcher.calc_matches(src_words_arr, dst_function, lang=lang)

    for src_word, src_phonim, src_soundex, matches, translation in \
                    zip(src_words_arr, src_phonim_arr, src_soundex_arr, matches, translations_arr):

        page_start = """<p style="page-break-after: always;">&nbsp;</p>"""
        page_end   = """<p style="page-break-before: always;">&nbsp;</p>"""
        
        log_to_file("Word in {} : {}| English Translation : {}".format(lang , src_word, translation) , log_filename)
        # log_to_file(f"<h2>word |||  {src_word}   ||| IPA {src_phonim}  |||  soundex {src_soundex}</h2>", log_filename)
        log_to_file("Words that sound similar in english (best matches):" +
                    matches.to_html().replace('\n', '')+"\n", log_filename)
        print(matches)
        log_to_file(page_start , log_filename)
        if gen_sentence:
            sounds_like_arr = matches.head(max_matches).index.values
            for idx , sounds_like in enumerate(sounds_like_arr):
                sentence = gpt3.generate_sentance(sounds_like, translation)
                
                log_to_file("The word {} in {} which have a meaning of {}, sounds like {} in speaking (candidate #{}) \n".format(src_word , lang , translation , sounds_like , str(idx)) , log_filename)
                log_to_file("A GPT3 generated sentence with the combination of the two words <b>{}</b> and <b>{}</b> is <b>{}</b>".format(translation , sounds_like , sentence) , log_filename)
                # log_to_file(f'<h3>{lang}:{src_word},'
                #             f'means:{translation},'
                #             f'sounds like:{sounds_like}. </h3> \n'
                #             f'sentence:<h3>{sentence}</h3>', log_filename)

                if gen_image:
                    images_path_arr = images.generate_image(sentence,max_num=1)
                    
                    for image_path in images_path_arr:
                        log_to_file("A genereated image of the sentence <b>{}</b> from google images : ".format(sentence), log_filename)
                        # log_to_file("generated images in path:\n"+image_path, log_filename)
                        log_to_file(f'<img src="{image_path}" width="300" height="300">', log_filename)
                        # log_to_file(f'<hr size="8" width="90%" color="black">  ', log_filename)   
                    log_to_file(page_end , log_filename)  

    image_to_pdf(log_filename)


def run_few_languages_test(languages=["english", "russian", "french", "spanish", "esperanto", "german"],
                           gen_sentence=True, gen_image=False):
    log_filename = generate_file_name()

    for l in languages:
        generic_test(lang=l, gen_sentence=gen_sentence,
                     gen_image=gen_image, log_filename=log_filename)


if __name__ == '__main__':
    run_few_languages_test(["hebrew", "arabic", "german", "french", "spanish", "korean", "russian", "esperanto", "english"],
                           gen_sentence=True, gen_image=True)
    exit()
    print("\n\n\nfeature_edit_distance\n\n\n")
    generic_test(dst_function="feature_edit_distance", lang='russian')
    generic_test(dst_function="feature_edit_distance", lang='french')

    print("\n\n\nfast_levenshtein_distance\n\n\n")
    generic_test(dst_function="fast_levenshtein_distance", lang='russian')
    generic_test(dst_function="fast_levenshtein_distance", lang='french')

    print("\n\n\nhamming_feature_edit_distance\n\n\n")
    generic_test(dst_function="hamming_feature_edit_distance", lang='russian')
    generic_test(dst_function="hamming_feature_edit_distance", lang='french')

