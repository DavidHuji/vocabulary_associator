from itertools import zip_longest

def convert_sound(sound):
    if sound in "pbɸβfvθðwɓʋ":
        return "V"
    elif sound in "tdʈɖcɟɗ":
        return "D"
    elif sound in "ɟkgqɠʛɡ":
        return "K"
    elif sound in "szʃʒʂɕʑʍ":
        return "S"
    elif sound in "lɭʟɫ":
        return "L"
    elif sound in "rʀⱱɾɽʕʕɹɻʁ":
        return "R"
    elif sound in "nɳɲŋɴ":
        return "N"
    elif sound in "mɱ":
        return "M"
    elif sound in "ħhɦxɣχɰç":
        return "H"
    elif sound in "ʎjʝ":
        return "Y"
    elif sound in "iyɨʉɯuɪʏʊeøɘɵɤoəɛœɜɞʌɔæɐaɶɑɒɔ̃ɔ̃ɝ":
        return "A"
    elif sound in "ˈˌ":
        return "."
    #elif sound in "ʲː̟͡ ̞̹̹̹̹̹̹̹̹̹̹":
    #    return ""
    else:
        return "?"

def convert(word):
    sndx = ''.join([convert_sound(x) for x in word])
    # remove duplicating chars that are next to each other
    fixed = "".join([i for i, j in zip_longest(sndx, sndx[1:]) if i!=j])
    # remove vowels
    fixed = fixed.replace("A","")
    # Remove symbols that break the sound
    fixed = fixed.replace(".", "")
    # Remove unknown symbols
    fixed = fixed.replace("?", "")
    if len(fixed) == 0:
        fixed = "A"
    return fixed

if __name__ == '__main__':
    print(convert("ˈɪnfoʊ"))
    print(convert("nuvo"))

