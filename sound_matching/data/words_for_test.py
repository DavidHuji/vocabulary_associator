

# to hear that words use: https://translate.google.com/?sl=en&tl=ko&text=%22time%22%2C%20%20%22year%22%2C%20%20%22people%22%2C%20%20%22way%22%2C%20%20%22day%22%2C%20%20%22man%22%2C%20%20%22thing%22%2C%20%20%22woman%22%2C%20%20%22life%22%2C%20%20%22child%22%2C%20%20%22world%22%2C%20%20%22school%22%2C%20%20%22state%22%2C%20%20%22family%22%2C%20%20%22student%22%2C%20%20%22group%22%2C%20%20%22country%22%2C%20%20%22problem%22%2C%20%20%22hand%22%2C%20%20%22part%22%0A&op=translate
top_english_20_nouns = ["time",  "year",  "people",  "way",  "day",  "man",  "thing",  "woman",  "life",  "child",  "world",  "school",  "state",  "family",  "student",  "group",  "country",  "problem",  "hand",  "part"]
french_trans = ["temps", "année", "gens", "chemin", "jour", "homme", "chose", "femme", "vie", "enfant", "monde", "école", "état", "famille", "étudiant", "groupe", "pays", "problème", "main", "partie"]
spanish_trans = ["tiempo", "año", "gente", "camino", "día", "hombre", "cosa", "mujer", "vida", "niño", "mundo", "escuela", "estado", "familia", "estudiante", "grupo", "país", "problema", "mano", "parte"]
italian_trans = ["tempo", "anno", "persone", "via", "giorno", "uomo", "cosa", "donna", "vita", "bambino", "mondo", "scuola", "stato", "famiglia", "studente", "gruppo", "paese", "problema", "mano", "parte"]
german_trans = ["Zeit", "Jahr", "Menschen", "Weg", "Tag", "Mann", "Ding", "Frau", "Leben", "Kind", "Welt", "Schule", "Zustand", "Familie", "Schüler", "Gruppe", "Land", "Problem", "Hand", "Teil"]
esperanto_trans = ["tempo", "jaro", "homoj", "maniero", "tago", "viro", "aĵo", "virino", "vivo", "infano", "mondo", "lernejo", "ŝtato", "familio", "lernanto", "grupo", "lando", "problemo", "mano", "parto"]
hebrew_trans = ["זמן", "שנה", "אנשים", "דרך", "יום", "גבר", "דבר", "אישה", "חיים", "ילד", "עולם", "בית ספר", "מדינה", "משפחה", "סטודנט", "קבוצה", "ארץ", "בעיה", "יד", "חלק"]
korean_trans = ["시간", "년", "사람", "길", "일", "남자", "사물", "여자", "생활", "아이", "세계", "학교", "상태", "가족", "학생", "단체", "국가", "문제", "손", "부분"]
russian_trans = ["время", "год", "люди", "путь", "день", "мужчина", "вещь", "женщина", "жизнь", "ребенок", "мир", "школа", "государство", "семья", "ученик", "группа", "страна", "проблема", "рука", "часть"]
# arabic_trans = ["الوقت", "السنة", "الناس", "الطريق", "اليوم", "الرجل", "الشيء", "المرأة", "الحياة", "الطفل", "العالم" , "المدرسة" , "الولاية" , "العائلة" , "الطالب" , "المجموعة" , "البلد" , "المشكلة" , "اليد" , "الجزء"]
# arabic_trans = [سنة, ناس, طريق, يوم, رجل, شيء, مرأة, حياة, طفل, عالم, مدرسة, ولاية, عائلة, طالب, مجموعة, بلد, مشكلة, يد, جزء]
arabic_trans = ["وقت", "سنة", "ناس", "طريق", "يوم", "رجل", "شيء", "مرأة", "حياة", "طفل", "عالم", "مدرسة", "ولاية", "عائلة", "طالب", "مجموعة", "بلد", "مشكلة", "يد", "جزء"]



def get_top_20nouns(lang='english'):
    if lang == 'english':
        return top_english_20_nouns
    elif lang == 'hebrew':
        return hebrew_trans
    elif lang == 'french':
        return french_trans
    elif lang == 'spanish':
        return spanish_trans
    elif lang == 'italian':
        return italian_trans
    elif lang == 'german':
        return german_trans
    elif lang == 'esperanto':
        return esperanto_trans
    elif lang == 'korean':
        return korean_trans
    elif lang == 'russian':
        return russian_trans
    elif lang == "arabic":
        return arabic_trans


def get_top_20nouns_test(lang):
    return get_top_20nouns(lang=lang), get_top_20nouns('english')