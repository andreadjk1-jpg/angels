"""Alfabeto e convenzioni condivisi fra generatori Python e pagine HTML."""

HEBREW_ALPHABET = {
    'א': {'name': 'Aleph', 'val': 1, 'roman': 'ʾ'},
    'ב': {'name': 'Beth', 'val': 2, 'roman': 'b'},
    'ג': {'name': 'Gimel', 'val': 3, 'roman': 'g'},
    'ד': {'name': 'Daleth', 'val': 4, 'roman': 'd'},
    'ה': {'name': 'He', 'val': 5, 'roman': 'h'},
    'ו': {'name': 'Vav', 'val': 6, 'roman': 'v'},
    'ז': {'name': 'Zayin', 'val': 7, 'roman': 'z'},
    'ח': {'name': 'Cheth', 'val': 8, 'roman': 'ḥ'},
    'ט': {'name': 'Teth', 'val': 9, 'roman': 'ṭ'},
    'י': {'name': 'Yod', 'val': 10, 'roman': 'y'},
    'כ': {'name': 'Kaph', 'val': 20, 'roman': 'k'},
    'ך': {'name': 'Kaph finale', 'val': 20, 'valFinal': 500, 'roman': 'k'},
    'ל': {'name': 'Lamed', 'val': 30, 'roman': 'l'},
    'מ': {'name': 'Mem', 'val': 40, 'roman': 'm'},
    'ם': {'name': 'Mem finale', 'val': 40, 'valFinal': 600, 'roman': 'm'},
    'נ': {'name': 'Nun', 'val': 50, 'roman': 'n'},
    'ן': {'name': 'Nun finale', 'val': 50, 'valFinal': 700, 'roman': 'n'},
    'ס': {'name': 'Samekh', 'val': 60, 'roman': 's'},
    'ע': {'name': 'Ayin', 'val': 70, 'roman': 'ʿ'},
    'פ': {'name': 'Pe', 'val': 80, 'roman': 'p'},
    'ף': {'name': 'Pe finale', 'val': 80, 'valFinal': 800, 'roman': 'p'},
    'צ': {'name': 'Tsadi', 'val': 90, 'roman': 'ṣ'},
    'ץ': {'name': 'Tsadi finale', 'val': 90, 'valFinal': 900, 'roman': 'ṣ'},
    'ק': {'name': 'Qoph', 'val': 100, 'roman': 'q'},
    'ר': {'name': 'Resh', 'val': 200, 'roman': 'r'},
    'ש': {'name': 'Shin', 'val': 300, 'roman': 'š'},
    'ת': {'name': 'Tav', 'val': 400, 'roman': 't'},
}

# I/J e U/V sono resi con le lettere moderne distinte. Le quattro forme
# aggiuntive della tabella di Agrippa sono disponibili anche come token espliciti.
LATIN_VALUES = dict(zip('abcdefghiklmnopqrstuxyz',
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50,
                        60, 70, 80, 90, 100, 200, 300, 400, 500]))
LATIN_VALUES.update(j=600, v=700, w=900)
LATIN_SPECIAL = {'I': 600, 'V': 700, 'HI': 800, 'HV': 900}


def hebrew_gematria(text, extended_finals=False):
    return sum(letter.get('valFinal', letter['val']) if extended_finals else letter['val']
               for char in text if (letter := HEBREW_ALPHABET.get(char)))


def number_to_hebrew(number):
    """Numerali additivi, senza lettere finali estese; zero ha grafia vuota."""
    if isinstance(number, bool) or not isinstance(number, int) or number < 0:
        raise ValueError('Il numerale richiede un intero maggiore o uguale a zero.')
    hundreds, remainder = divmod(number, 400)
    result = 'ת' * hundreds
    count, remainder = divmod(remainder, 100)
    result += ['', 'ק', 'ר', 'ש'][count]
    if remainder == 15:
        return result + 'טו'
    if remainder == 16:
        return result + 'טז'
    tens, units = divmod(remainder, 10)
    return result + ['', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ'][tens] + ['', 'א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט'][units]


def transliterate_hebrew(text):
    """Trascrive tutte le consonanti; il punto separa lettere, senza vocali inventate."""
    return ' / '.join('·'.join(HEBREW_ALPHABET[c]['roman'] for c in word if c in HEBREW_ALPHABET)
                      for word in text.split())


def browser_spec(known_names):
    return {'letters': HEBREW_ALPHABET, 'latinValues': LATIN_VALUES,
            'latinSpecial': LATIN_SPECIAL, 'knownNames': known_names}
