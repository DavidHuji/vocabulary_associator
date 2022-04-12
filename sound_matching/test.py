import matcher, gpt3, images
from pathlib import Path
import datetime
# import weasyprint

def english_test_with_translation():
    orig = ["kiwi","something", "tear", "informed", "chair", "sky", "cat", "sun"]
    return orig, orig


def korean_test_with_translation():
    orig = ["오늘", "지금", "년"]
    trans = ["Today", "Now", "Year"]
    return orig, trans

def french_test_with_translation():
    orig = ["baguette","avoir", "pas", "pouvoir", "son", "dire", "devoir", "avant", "deux", "bien",
            "fois", "nouveau", "vouloir", "moins", "temps", "savoir", "raison", "monde",
            "jour", "monsieur"]
    trans = ["bread","have", "not", "can", "sound", "say", "should", "before", "two", "well",
             "times", "new", "want", "less", "time", "know", "reason", "world",
             "day", "sir"]
    return orig, trans

def hebrew_test_with_translation():
    orig = ["שקד", "שלג", "במקום", "גלויה", "גרון", "זהב", "כתיבה", "עיר", "סוס"]
    trans = ["almond","snow", "instead", "postcard", "throat", "gold", "writing", "city", "hourse"]
    return orig, trans

def russian_test_with_translation():
    orig = ["мужчина", "порез", "уксус", "дерево", "Александр"]
    trans = ["male", "cut", "viniger", "tree", "alexander"]
    return orig, trans

def spanish_test_with_translation():
    orig = ["abane", "malo", "mujer", "hombre", "ciudad", "partir", "feliz"]
    trans =["abandon", "bad", "woman", "man", "city", "depart", "happy"]
    return orig, trans

def german_test_with_translation():
    orig = ["werden", "zwei", "zwischen", "sagte", "Netzwerk", "zurecht", "geschieht"]
    trans = ["become", "two", "between", "said", "network", "rightly", "happens"]
    return orig, trans

def esperanto_test_with_translation():
    orig = ["viro", "doni", "knabo", "kapo", "lernejo", "arbo"]
    trans = ["man", "give", "boy", "head", "school", "tree"]
    return orig, trans

def get_words_for_test(lang='english'):
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

    # weasyprint.HTML(html_path).write_pdf(pdf_path)


def generic_test(dst_function="weighted_feature_edit_distance", lang='english',
                 gen_sentence=True, gen_image=False, max_matches=3, log_filename=generate_file_name()):

    log_to_file(f'<h1>start test of {lang.upper()} with {dst_function}, \n'\
                f'generate sentence = {gen_sentence}, generate image = {gen_image}\n'
                f'file {log_filename}</h1>\n', log_filename)

    dst_function = get_distance_function(dst_function)
    src_words_arr, translations_arr = get_words_for_test(lang)

    matches, src_phonim_arr, src_soundex_arr = matcher.calc_matches(src_words_arr, dst_function, lang=lang)

    for src_word, src_phonim, src_soundex, matches, translation in \
                    zip(src_words_arr, src_phonim_arr, src_soundex_arr, matches, translations_arr):
        log_to_file(f"<h2>word |||  {src_word}   ||| IPA {src_phonim}  |||  soundex {src_soundex}</h2>", log_filename)
        log_to_file("Words that sound similar in english (best matches):" +
                    matches.to_html().replace('\n', '')+"\n", log_filename)
        print(matches)

        if gen_sentence:
            sounds_like_arr = matches.head(max_matches).index.values
            for sounds_like in sounds_like_arr:

                sentence = gpt3.generate_sentance(sounds_like, translation)

                log_to_file(f'<h3>{lang}:{src_word},'
                            f'means:{translation},'
                            f'sounds like:{sounds_like}. </h3> \n'
                            f'sentence:<h3>{sentence}</h3>', log_filename)

                if gen_image:
                    images_path_arr = images.generate_image(sentence,max_num=1)
                    for image_path in images_path_arr:
                        log_to_file("Image", log_filename)
                        log_to_file("generated images in path:\n"+image_path, log_filename)
                        log_to_file(f'<img src="{image_path}" style="max-width:30%">', log_filename)

    image_to_pdf(log_filename)

def run_few_languages_test(languages=["english", "russian", "french", "spanish", "esperanto", "german"],
                           gen_sentence=True, gen_image=False):
    log_filename = generate_file_name()

    for l in languages:
        generic_test(lang=l, gen_sentence=gen_sentence,
                     gen_image=gen_image, log_filename=log_filename)


if __name__ == '__main__':
    run_few_languages_test(["korean", "hebrew", "english", "french", "russian", "spanish", "esperanto", "german"],
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

