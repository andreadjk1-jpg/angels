"""Modulo per l'ortografia araba e il calcolo dell'Abjad (Hisab al-Jummal).

Questo modulo fornisce le corrispondenze fonetiche e numeriche dell'alfabeto arabo
a 28 lettere, sia secondo lo standard orientale (Mashriqi) sia per l'analisi
dell'onomastica angelica islamica e delle 28 Mansioni Lunari (Manazil al-Qamar).
"""
import re
import unicodedata

# Alfabeto Abjad classico orientale (28 lettere) con valori numerici tradizionali
ABJAD_EASTERN = {
    # Unità 1-9 (Abjad - Hawwaz - Hutti)
    'ا': 1, 'أ': 1, 'إ': 1, 'آ': 1, 'ء': 1,
    'ب': 2,
    'ج': 3,
    'د': 4,
    'ه': 5, 'ة': 5,  # Ta Marbuta conta come 5 in pausa o 400 come Ta; per standard gematrico comune vale 5 o 400
    'و': 6, 'ؤ': 6,
    'ز': 7,
    'ح': 8,
    'ط': 9,
    # Decine 10-90 (Kalaman - Sa'fas)
    'ي': 10, 'ى': 10, 'ئ': 10,  # Ya / Alif Maqsura / Hamza su Ya
    'ك': 20,
    'ل': 30,
    'م': 40,
    'ن': 50,
    'س': 60,
    'ع': 70,
    'ف': 80,
    'ص': 90,
    # Centinaia 100-900 (Qarashat - Thakhadh - Dazagh)
    'ق': 100,
    'ر': 200,
    'ش': 300,
    'ت': 400,
    'ث': 500,
    'خ': 600,
    'ذ': 700,
    'ض': 800,
    'ظ': 900,
    # Millesimo
    'غ': 1000
}

# Traslitterazione standard accademica (DMG / Arabica)
ARABIC_TRANSLIT = {
    'ا': 'ā', 'أ': 'ʾa', 'إ': 'ʾi', 'آ': 'ʾā', 'ء': 'ʾ',
    'ب': 'b', 'ت': 't', 'ث': 'th', 'ج': 'j', 'ح': 'ḥ', 'خ': 'kh',
    'د': 'd', 'ذ': 'dh', 'ر': 'r', 'ز': 'z', 'س': 's', 'ش': 'sh',
    'ص': 'ṣ', 'ض': 'ḍ', 'ط': 'ṭ', 'ظ': 'ẓ', 'ع': 'ʿ', 'غ': 'gh',
    'ف': 'f', 'ق': 'q', 'ك': 'k', 'ل': 'l', 'م': 'm', 'ن': 'n',
    'ه': 'h', 'ة': 'h', 'و': 'w', 'ي': 'y', 'ى': 'ā', 'ئ': 'ʾy', 'ؤ': 'ʾw'
}

# Diacritici arabi (Tashkīl) da ignorare nel computo
TASHKEEL_REGEX = re.compile(r'[\u0617-\u061A\u064B-\u0652]')


def clean_arabic_text(text: str) -> str:
    """Rimuove harakat, tashkeel e caratteri non alfabetici arabi."""
    if not text:
        return ""
    text = TASHKEEL_REGEX.sub('', text)
    # Rimuove tatweel / kashida (_)
    text = text.replace('\u0640', '')
    return text.strip()


def abjad_gematria(text: str, ta_marbuta_as_400: bool = False) -> int:
    """Calcola il valore Abjad (Hisab al-Jummal) di una stringa araba.
    
    Se ta_marbuta_as_400 è True, 'ة' vale 400 (come 'ت'), altrimenti 5 (come 'ه').
    Nella maggior parte dei testi magico-talismanici (al-Buni), la Ta Marbuta vale 400.
    """
    clean = clean_arabic_text(text)
    total = 0
    for ch in clean:
        if ch == 'ة':
            total += 400 if ta_marbuta_as_400 else 5
        elif ch in ABJAD_EASTERN:
            total += ABJAD_EASTERN[ch]
    return total


def transliterate_arabic(text: str) -> str:
    """Fornisce una trascrizione fonetica leggibile dei caratteri consonantici."""
    clean = clean_arabic_text(text)
    parts = []
    for ch in clean:
        if ch in ARABIC_TRANSLIT:
            parts.append(ARABIC_TRANSLIT[ch])
        elif ch.isspace():
            parts.append(' ')
    return ''.join(parts)


# I Grandi Arcangeli Coranici e Tradizionali con varianti grafiche
ISLAMIC_ARCHANGELS = [
    {
        "id": "jibril",
        "name_ar": "جبريل",
        "translit": "Jibrīl",
        "abjad": abjad_gematria("جبريل"),
        "hebrew_equiv": "גבריאל",
        "hebrew_gem": 246,
        "role": "Angelo della Rivelazione e dello Spirito Santo (Rūḥ al-Qudus)",
        "quran_refs": ["2:97", "2:98", "66:4"]
    },
    {
        "id": "mikal",
        "name_ar": "ميكال",  # Forma coranica esatta in Sura 2:98
        "translit": "Mīkāl (Coranica)",
        "abjad": abjad_gematria("ميكال"),
        "hebrew_equiv": "מיכאל",
        "hebrew_gem": 101,
        "role": "Angelo del Sostentamento e delle Forze Naturali",
        "quran_refs": ["2:98"]
    },
    {
        "id": "mikail",
        "name_ar": "ميكائيل",  # Forma tradizionale estesa
        "translit": "Mīkā'īl (Tradizionale)",
        "abjad": abjad_gematria("ميكائيل"),
        "hebrew_equiv": "מיכאל",
        "hebrew_gem": 101,
        "role": "Angelo del Sostentamento (grafia letteraria)",
        "quran_refs": []
    },
    {
        "id": "israfil",
        "name_ar": "إسرافيل",
        "translit": "Isrāfīl",
        "abjad": abjad_gematria("إسرافيل"),
        "hebrew_equiv": "שרפיאל / רפאל",
        "hebrew_gem": 591,
        "role": "Angelo della Tromba del Giudizio (al-Ṣūr)",
        "quran_refs": ["Hadith canonici / esegesi Sura 39:68"]
    },
    {
        "id": "azrail",
        "name_ar": "عزرائيل",
        "translit": "ʿAzrā'īl",
        "abjad": abjad_gematria("عزرائيل"),
        "hebrew_equiv": "עזריאל",
        "hebrew_gem": 318,
        "role": "Angelo della Morte (Malak al-Mawt)",
        "quran_refs": ["Sura 32:11 cita 'Malak al-Mawt'"]
    }
]

# Altri angeli coranici specifici
QURANIC_ANGELS = [
    {
        "name_ar": "مالك",
        "translit": "Mālik",
        "abjad": abjad_gematria("مالك"),
        "role": "Guardiano del Fuoco Infernale (Jahannam)",
        "quran_ref": "43:77"
    },
    {
        "name_ar": "رضوان",
        "translit": "Riḍwān",
        "abjad": abjad_gematria("رضوان"),
        "role": "Custode dei Giardini del Paradiso (Jannah)",
        "quran_ref": "Tradizione Hadith"
    },
    {
        "name_ar": "هاروت",
        "translit": "Hārūt",
        "abjad": abjad_gematria("هاروت"),
        "role": "Angelo inviato a Babilonia",
        "quran_ref": "2:102"
    },
    {
        "name_ar": "ماروت",
        "translit": "Mārūt",
        "abjad": abjad_gematria("ماروت"),
        "role": "Angelo inviato a Babilonia",
        "quran_ref": "2:102"
    },
    {
        "name_ar": "منكر",
        "translit": "Munkar",
        "abjad": abjad_gematria("منكر"),
        "role": "Esaminatore dell'anima nel sepolcro",
        "quran_ref": "Tradizione escatologica"
    },
    {
        "name_ar": "نكير",
        "translit": "Nakīr",
        "abjad": abjad_gematria("نكير"),
        "role": "Esaminatore dell'anima nel sepolcro",
        "quran_ref": "Tradizione escatologica"
    }
]

# Le 28 Mansioni Lunari (Manāzil al-Qamar) con corrispondenza ad Agrippa
MANAZIL_LUNARI = [
    {"num": 1, "name_ar": "الناطح", "translit": "Al-Nāṭiḥ", "meaning": "Il cozzo (Corni dell'Ariete)", "agrippa_lat": "Alnath", "angel_agrippa": "Geniel", "angel_heb": "גניאל", "abjad": abjad_gematria("الناطح")},
    {"num": 2, "name_ar": "البطين", "translit": "Al-Buṭayn", "meaning": "Il piccolo ventre", "agrippa_lat": "Albotham", "angel_agrippa": "Enediel", "angel_heb": "אנדיאל", "abjad": abjad_gematria("البطين")},
    {"num": 3, "name_ar": "الثريا", "translit": "Al-Thurayyā", "meaning": "Le Pleiadi / La moltitudine", "agrippa_lat": "Acla / Athoraye", "angel_agrippa": "Anixiel", "angel_heb": "אניקסיאל", "abjad": abjad_gematria("الثريا")},
    {"num": 4, "name_ar": "الدبران", "translit": "Al-Dabarān", "meaning": "L'inseguitore (Aldebaran)", "agrippa_lat": "Aldebaran", "angel_agrippa": "Aziel", "angel_heb": "עזיאל", "abjad": abjad_gematria("الدبران")},
    {"num": 5, "name_ar": "الهقعة", "translit": "Al-Haqʿah", "meaning": "Il ciuffo bianco (in Orione)", "agrippa_lat": "Alchatay", "angel_agrippa": "Gabriel", "angel_heb": "גבריאל", "abjad": abjad_gematria("الهقعة")},
    {"num": 6, "name_ar": "الهنعة", "translit": "Al-Hanʿah", "meaning": "Il marchio / La cicatrice", "agrippa_lat": "Athanna", "angel_agrippa": "Dirachiel", "angel_heb": "דירכיאל", "abjad": abjad_gematria("الهنعة")},
    {"num": 7, "name_ar": "الذراع", "translit": "Al-Dhirāʿ", "meaning": "Il braccio (dei Gemelli)", "agrippa_lat": "Aldirah", "angel_agrippa": "Scheliel", "angel_heb": "שליאל", "abjad": abjad_gematria("الذراع")},
    {"num": 8, "name_ar": "النثرة", "translit": "Al-Nathrah", "meaning": "Il respiro / La criniera (nel Cancro)", "agrippa_lat": "Annathra", "angel_agrippa": "Amnediel", "angel_heb": "אמנדיאל", "abjad": abjad_gematria("النثرة")},
    {"num": 9, "name_ar": "الطرف", "translit": "Al-Ṭarf", "meaning": "Lo sguardo / Gli occhi del Leone", "agrippa_lat": "Attarf", "angel_agrippa": "Barbiel", "angel_heb": "ברביאל", "abjad": abjad_gematria("الطرف")},
    {"num": 10, "name_ar": "الجبهة", "translit": "Al-Jabhah", "meaning": "La fronte (del Leone)", "agrippa_lat": "Algebha", "angel_agrippa": "Ardefiel", "angel_heb": "ארדפיאל", "abjad": abjad_gematria("الجبهة")},
    {"num": 11, "name_ar": "الزبرة", "translit": "Al-Zubrah", "meaning": "Il dorso del Leone", "agrippa_lat": "Azobra", "angel_agrippa": "Neciel", "angel_heb": "נקיאל", "abjad": abjad_gematria("الزبرة")},
    {"num": 12, "name_ar": "الصرفة", "translit": "Al-Ṣarfah", "meaning": "Il volgersi del tempo (Denebola)", "agrippa_lat": "Asarfa", "angel_agrippa": "Abdizuel", "angel_heb": "עבדיזואל", "abjad": abjad_gematria("الصرفة")},
    {"num": 13, "name_ar": "العواء", "translit": "Al-ʿAwwāʾ", "meaning": "Il cane abbaiante (nella Vergine)", "agrippa_lat": "Achrue / Alhaue", "angel_agrippa": "Jazeriel", "angel_heb": "יזריאל", "abjad": abjad_gematria("العواء")},
    {"num": 14, "name_ar": "السماك", "translit": "Al-Simāk", "meaning": "L'elevato (Spica)", "agrippa_lat": "Simak / Azimeth", "angel_agrippa": "Ergediel", "angel_heb": "ארגדיאל", "abjad": abjad_gematria("السماك")},
    {"num": 15, "name_ar": "الغفر", "translit": "Al-Ghafr", "meaning": "Il velo / Il rifugio", "agrippa_lat": "Algafra", "angel_agrippa": "Atliel", "angel_heb": "אתליאל", "abjad": abjad_gematria("الغفر")},
    {"num": 16, "name_ar": "الزبانا", "translit": "Al-Zubānā", "meaning": "Le chele (della Bilancia)", "agrippa_lat": "Azubene", "angel_agrippa": "Azeruel", "angel_heb": "עזרואל", "abjad": abjad_gematria("الزبانا")},
    {"num": 17, "name_ar": "الإكليل", "translit": "Al-Iklīl", "meaning": "La corona (dello Scorpione)", "agrippa_lat": "Alchil", "angel_agrippa": "Adriel", "angel_heb": "אדריאל", "abjad": abjad_gematria("الإكليل")},
    {"num": 18, "name_ar": "القلب", "translit": "Al-Qalb", "meaning": "Il cuore (Antares)", "agrippa_lat": "Alchas", "angel_agrippa": "Egibiel", "angel_heb": "אגיביאל", "abjad": abjad_gematria("القلب")},
    {"num": 19, "name_ar": "الشولة", "translit": "Al-Shawlah", "meaning": "Il pungiglione (dello Scorpione)", "agrippa_lat": "Allatha", "angel_agrippa": "Amutiel", "angel_heb": "אמותיאל", "abjad": abjad_gematria("الشولة")},
    {"num": 20, "name_ar": "النعائم", "translit": "Al-Naʿāʾim", "meaning": "Gli struzzi (nel Sagittario)", "agrippa_lat": "Abnahaya", "angel_agrippa": "Kyriel", "angel_heb": "קיריאל", "abjad": abjad_gematria("النعائم")},
    {"num": 21, "name_ar": "البلدة", "translit": "Al-Baldah", "meaning": "La città / Lo spazio vuoto", "agrippa_lat": "Abeda", "angel_agrippa": "Bethnael", "angel_heb": "בתנאל", "abjad": abjad_gematria("البلدة")},
    {"num": 22, "name_ar": "سعد الذابح", "translit": "Saʿd al-Dhābiḥ", "meaning": "La fortuna del sacrificatore", "agrippa_lat": "Sadahacha", "angel_agrippa": "Geliel", "angel_heb": "גליאל", "abjad": abjad_gematria("سعد الذابح")},
    {"num": 23, "name_ar": "سعد بلع", "translit": "Saʿd Bulaʿ", "meaning": "La fortuna dell'inghiottitore", "agrippa_lat": "Zabadola", "angel_agrippa": "Requiel", "angel_heb": "רקיאל", "abjad": abjad_gematria("سعد بلع")},
    {"num": 24, "name_ar": "سعد السعود", "translit": "Saʿd al-Suʿūd", "meaning": "La fortuna delle fortune", "agrippa_lat": "Sadabath", "angel_agrippa": "Abrinael", "angel_heb": "אברינאל", "abjad": abjad_gematria("سعد السعود")},
    {"num": 25, "name_ar": "سعد الأخبية", "translit": "Saʿd al-Akhbiyah", "meaning": "La fortuna delle tende", "agrippa_lat": "Sadalabra", "angel_agrippa": "Aziel II", "angel_heb": "עזריאל", "abjad": abjad_gematria("سعد الأخبية")},
    {"num": 26, "name_ar": "الفرغ المقدم", "translit": "Al-Fargh al-Muqaddam", "meaning": "Il beccuccio anteriore del vaso", "agrippa_lat": "Alpharg", "angel_agrippa": "Tagriel", "angel_heb": "תגריאל", "abjad": abjad_gematria("الفرغ المقدم")},
    {"num": 27, "name_ar": "الفرغ المؤخر", "translit": "Al-Fargh al-Mu'akhkhar", "meaning": "Il beccuccio posteriore del vaso", "agrippa_lat": "Alcharya", "angel_agrippa": "Atheniel", "angel_heb": "אתניאל", "abjad": abjad_gematria("الفرغ المؤخر")},
    {"num": 28, "name_ar": "بطن الحوت", "translit": "Baṭn al-Ḥūt", "meaning": "Il ventre del pesce / della balena", "agrippa_lat": "Batnolhait / Albotham", "angel_agrippa": "Amnixiel", "angel_heb": "אמניקסיאל", "abjad": abjad_gematria("بطن الحوت")}
]

if __name__ == '__main__':
    print("=== TEST CALCOLATORE ABJAD ===")
    for a in ISLAMIC_ARCHANGELS:
        print(f"{a['translit']} ({a['name_ar']}) -> Abjad: {a['abjad']} | Equiv Ebr: {a['hebrew_equiv']} ({a['hebrew_gem']})")
    print(f"\nTotale Mansioni caricate: {len(MANAZIL_LUNARI)}")
