# -*- coding: utf-8 -*-
"""
Costruisce l'atlante delle dieci sfere e delle due estensioni del progetto:
  C:\\Users\\asdf\\agrippa_cosmo\\angels_12_heavens.html
e aggiorna index.html e agrippa_calculator.html con il collegamento diretto.
"""

import json
import os
import re
from collections import Counter
from generate_table_angels import generate_all, extract_table_angels, generate_magic_square
from hebrew_orthography import HEBREW_ALPHABET, browser_spec
from lunar_names import export_lunar_catalog
from divine_names import export_shem42, known_divine_names, shem42_overview
from generate_shem42_angels import build_shem42_generator
from build_complete_catalog import build_complete_catalog

SPHERES_META = [
    {
        "sphereNum": 1, "higherOrder": 10, "classicOrder": None, "chamber12": 10,
        "sign": "10. Capricorno (♑)", "signAngel": "Hanael", "signAngelHeb": "הנאל", "signAngelGem": 86,
        "permYHVH": "היהו", "month": "Tevet", "tribe": "Zabulon",
        "heavenName": "Cielo I — Primum Mobile (Sphaera Prima · Kether)",
        "divineName": "Eheieh (אהיה = 21 · «Qui Sum / Essentia»)", "divineHeb": "אהיה",
        "sephirah": "1. Kether (כתר = 620 — Corona Suprema)",
        "choir": "Haioth ha-Kadosh (חיות הקדש — Animalia Sancta / Serafini)",
        "archangel": "Metatron (מטטרון = 314 — Princeps Facierum)",
        "intName": "Daathel / Scientiel (דעתאל = 505 = M₁₀)", "intHeb": "דעתאל", "intGem": 505,
        "spirName": "Michael / Oculel (מיכאל = 101 = P₁₀)", "spirHeb": "מיכאל", "spirGem": 101,
        "color": "#f5d76e", "signature12": "[10 - 4 - 1 - 10]",
        "shemRange": (55, 60), "mansions": [(22, "Sadahacha", "Geliel", "גליאל"), (23, "Zabadola", "Requiel", "רקיאל"), (24, "Sadabath", "Abrinael", "אברינאל")]
    },
    {
        "sphereNum": 2, "higherOrder": 11, "classicOrder": None, "chamber12": 11,
        "sign": "11. Acquario (♒)", "signAngel": "Cambiel", "signAngelHeb": "כמביאל", "signAngelGem": 103,
        "permYHVH": "היוה", "month": "Shevat", "tribe": "Ruben",
        "heavenName": "Cielo II — Coelum Stellatum / Signifer (Zodiaco · Chokmah)",
        "divineName": "Yah (יה = 15) / YHVH (יהוה = 26)", "divineHeb": "יהוה",
        "sephirah": "2. Chokmah (חכמה = 73 — Sapienza Primordiale)",
        "choir": "Ophanim (אופנים — Rotae Coelestes / Cherubini)",
        "archangel": "Raziel (רזיאל = 248 — Secretum Dei)",
        "intName": "Semesiel / Solariel (שמשאל = 671 = M₁₁)", "intHeb": "שמשאל", "intGem": 671,
        "spirName": "Sachiel / Iustitiel (סכיאל = 121 = 11²)", "spirHeb": "סכיאל", "spirGem": 121,
        "color": "#a569bd", "signature12": "[11 - 1 - 11 - 1]",
        "shemRange": (61, 66), "mansions": [(25, "Sadalabra", "Aziel", "עזיאל"), (26, "Alpharg", "Tagriel", "תגריאל")]
    },
    {
        "sphereNum": 3, "higherOrder": 12, "classicOrder": 3, "chamber12": 12,
        "sign": "12. Pesci (♓)", "signAngel": "Barchiel", "signAngelHeb": "ברכיאל", "signAngelGem": 263,
        "permYHVH": "ההוי", "month": "Adar", "tribe": "Simeone",
        "heavenName": "Cielo III — Sphaera Saturni (Saturno ♄ · Binah)",
        "divineName": "YHVH Elohim (יהוה אלהים) · Yah (יה = 15)", "divineHeb": "יה",
        "sephirah": "3. Binah (בינה — Intelligenza / Madre Superna)",
        "choir": "Aralim (אראלים — Throni / Angeli Fortes)",
        "archangel": "Zaphkiel (צפקיאל = 311) & Cassiel (קפציאל = 311)",
        "intName": "Kedemel-Magnum (קדם = 144 = 12²) · Classica: Agiel (אגיאל = 45)", "intHeb": "קדם", "intGem": 144,
        "spirName": "Thathlatiel (תתלטאל = 870 = M₁₂) · Classica: Zazel (זזאל = 45)", "spirHeb": "תתלטאל", "spirGem": 870,
        "color": "#95a5a6", "signature12": "[12 - 12 - 6 - 12]",
        "shemRange": (67, 72), "mansions": [(27, "Alcharya", "Atheniel", "אתניאל"), (28, "Albotham", "Amnixiel", "אמניקסיאל")]
    },
    {
        "sphereNum": 4, "higherOrder": 13, "classicOrder": 4, "chamber12": 1,
        "sign": "1. Ariete (♈)", "signAngel": "Malchidael", "signAngelHeb": "מלכידאל", "signAngelGem": 135,
        "permYHVH": "יהוה", "month": "Nisan", "tribe": "Gad",
        "heavenName": "Cielo IV — Sphaera Iovis (Giove ♃ · Chesed)",
        "divineName": "El (אל = 31) · El Ab (אל אב = 34) · Echad (אחד = 13)", "divineHeb": "אלאב",
        "sephirah": "4. Chesed (חסד — Misericordia)",
        "choir": "Chasmalim (חשמלים — Dominationes / Lucidi)",
        "archangel": "Zadkiel (צדקיאל = 235) & Sachiel (סכיאל = 121)",
        "intName": "Tzemachel / Germiniel (צמחאל = 169 = 13²) · Classica: Iophiel (יופיל = 136)", "intHeb": "צמחאל", "intGem": 169,
        "spirName": "Unitiel / Amoriel (אחד = 13 = N₁₃) · Classica: Hismael (הסמאל = 136)", "spirHeb": "אחד", "spirGem": 13,
        "color": "#5dade2", "signature12": "★ [1 - 1 - 1 - 1] (Pilastro Puro)",
        "shemRange": (1, 6), "mansions": [(1, "Alnath", "Geniel", "גניאל"), (2, "Albotham", "Enediel", "אנדיאל"), (3, "Achaomazon", "Anixiel", "אניקסיאל")]
    },
    {
        "sphereNum": 5, "higherOrder": 14, "classicOrder": 5, "chamber12": 2,
        "sign": "2. Toro (♉)", "signAngel": "Asmodel", "signAngelHeb": "אסמודאל", "signAngelGem": 142,
        "permYHVH": "יההו", "month": "Iyar", "tribe": "Efraim",
        "heavenName": "Cielo V — Sphaera Martis (Marte ♂ · Geburah)",
        "divineName": "Elohim Gibor (אלהים גבור) · Adonai (אדני = 65)", "divineHeb": "אדני",
        "sephirah": "5. Geburah (גבורה — Potenza / Severità)",
        "choir": "Seraphim (שרפים — Potestates / Virtutes Ardentes)",
        "archangel": "Camael (כמאל = 91 — Auxilium / Rigor Dei)",
        "intName": "Etzahel / Consiliel (עצהאל = 196 = 14²) · Classica: Graphiel (גראפיאל = 325)", "intHeb": "עצהאל", "intGem": 196,
        "spirName": "Manuiel / Davidel (דוד = 14 = N₁₄) · Classica: Barzabel (ברצבאל = 325)", "spirHeb": "דוד", "spirGem": 14,
        "color": "#e74c3c", "signature12": "[2 - 4 - 11 - 10]",
        "shemRange": (7, 12), "mansions": [(4, "Aldebaram", "Azariel", "עזריאל"), (5, "Alchatay", "Gabriel", "גבריאל")]
    },
    {
        "sphereNum": 6, "higherOrder": 15, "classicOrder": 6, "chamber12": 3,
        "sign": "3. Gemelli (♊)", "signAngel": "Ambriel", "signAngelHeb": "אמבריאל", "signAngelGem": 284,
        "permYHVH": "יוהה", "month": "Sivan", "tribe": "Manasse",
        "heavenName": "Cielo VI — Sphaera Solis (Sole ☉ · Tiphereth — Cor Coeli)",
        "divineName": "YHVH Eloah Va-Daath · Aleph (אלף = 111)", "divineHeb": "אלף",
        "sephirah": "6. Tiphereth (תפארת — Bellezza / Cuore del Cosmo)",
        "choir": "Malachim (מלאכים — Virtutes / Reges Angelici)",
        "archangel": "Raphael (רפאל = 311 — Medicina Dei)",
        "intName": "Tzadkiel-Solis / Iustitiel (צדקאל = 225 = 15²) · Classica: Nachiel (נכיאל = 111)", "intHeb": "צדקאל", "intGem": 225,
        "spirName": "Iahel / Lucifel (יה = 15 = N₁₅) · Classica: Sorath (סורת = 666)", "spirHeb": "יה", "spirGem": 15,
        "color": "#f39c12", "signature12": "[3 - 9 - 3 - 9]",
        "shemRange": (13, 18), "mansions": [(6, "Alhanna", "Dirachiel", "דירכיאל"), (7, "Aldimiach", "Scheliel", "שליאל")]
    },
    {
        "sphereNum": 7, "higherOrder": 16, "classicOrder": 7, "chamber12": 4,
        "sign": "4. Cancro (♋)", "signAngel": "Muriel", "signAngelHeb": "מוריאל", "signAngelGem": 287,
        "permYHVH": "הוהי", "month": "Tammuz", "tribe": "Issachar",
        "heavenName": "Cielo VII — Sphaera Veneris (Venere ♀ · Netzach)",
        "divineName": "YHVH Tzabaoth (יהוה צבאות) · Aha (אהא = 7)", "divineHeb": "אהא",
        "sephirah": "7. Netzach (נצח — Vittoria / Eternità)",
        "choir": "Elohim / Tarshishim (אלהים — Principatus)",
        "archangel": "Haniel (הניאל = 96) & Anael (ענאל = 151)",
        "intName": "Rakahel / Suaviel (רכהאל = 256 = 16²) · Classica: Hagiel (הגיאל = 49)", "intHeb": "רכהאל", "intGem": 256,
        "spirName": "Tzaphonel / Aquilonel (צפונאל = 257 = P₁₆) · Classica: Kedemel (קדמאל = 175)", "spirHeb": "צפונאל", "spirGem": 257,
        "color": "#2ecc71", "signature12": "★ [4 - 4 - 4 - 4] (Pilastro Puro)",
        "shemRange": (19, 24), "mansions": [(8, "Alnaza", "Amnediel", "אמנדיאל"), (9, "Archaam", "Barbiel", "ברביאל"), (10, "Algelioche", "Ardefiel", "ארדפיאל")]
    },
    {
        "sphereNum": 8, "higherOrder": 17, "classicOrder": 8, "chamber12": 5,
        "sign": "5. Leone (♌)", "signAngel": "Verchiel", "signAngelHeb": "ורכיאל", "signAngelGem": 267,
        "permYHVH": "הויה", "month": "Av", "tribe": "Giuda",
        "heavenName": "Cielo VIII — Sphaera Mercurii (Mercurio ☿ · Hod)",
        "divineName": "Elohim Tzabaoth (אלהים צבאות) · Din (דין = 64)", "divineHeb": "דין",
        "sephirah": "8. Hod (הוד — Gloria / Splendore)",
        "choir": "Bene Elohim (בני אלהים — Archangeli / Filii Dei)",
        "archangel": "Michael (מיכאל = 101) & Raphael (רפאל = 311)",
        "intName": "Ranachel / Eloquentiel (רנחאל = 289 = 17²) · Classica: Tiriel (טיריאל = 260)", "intHeb": "רנחאל", "intGem": 289,
        "spirName": "Boniel / Benigniel (טוב = 17 = N₁₇) · Classica: Taphthartharath (תפתרתרת = 2080)", "spirHeb": "טוב", "spirGem": 17,
        "color": "#48c9b0", "signature12": "[5 - 1 - 5 - 1]",
        "shemRange": (25, 30), "mansions": [(11, "Azobra", "Neciel", "נקיאל"), (12, "Alzarpha", "Abdizuel", "עבדיזואל")]
    },
    {
        "sphereNum": 9, "higherOrder": 18, "classicOrder": 9, "chamber12": 6,
        "sign": "6. Vergine (♍)", "signAngel": "Hamaliel", "signAngelHeb": "המליאל", "signAngelGem": 116,
        "permYHVH": "ההיו", "month": "Elul", "tribe": "Neftali",
        "heavenName": "Cielo IX — Sphaera Lunae (Luna ☽ · Yesod — Regina Coeli)",
        "divineName": "Shaddai El Chai (שדי אל חי) · Elim (אלים = 81) · Chai (חי = 18)", "divineHeb": "אלים",
        "sephirah": "9. Yesod (יסוד — Fondamento Vivente)",
        "choir": "Cherubim (כרובים — Angeli)",
        "archangel": "Gabriel (גבריאל = 246 — Fortitudo Dei)",
        "intName": "Ratzgiel / Fundamentiel (רצגאל = 324 = 18²) · Classica: Malkah be-Tarshishim (S associata = 3321; grafia dell’archivio = 2447)", "intHeb": "רצגאל", "intGem": 324,
        "spirName": "Graphiel-Lunae (גראפיאל = 325 = P₁₈) · Classica: Hasmodai (חשמודאי = 369)", "spirHeb": "גראפיאל", "spirGem": 325,
        "color": "#d7dbdd", "signature12": "[6 - 12 - 9 - 6]",
        "shemRange": (31, 36), "mansions": [(13, "Alhaire", "Jazeriel", "יזריאל"), (14, "Achureth", "Ergediel", "ארגדיאל")]
    },
    {
        "sphereNum": 10, "higherOrder": 19, "classicOrder": None, "chamber12": 7,
        "sign": "7. Bilancia (♎)", "signAngel": "Zuriel", "signAngelHeb": "זוריאל", "signAngelGem": 254,
        "permYHVH": "ויהה", "month": "Tishri", "tribe": "Assur / Asher",
        "heavenName": "Cielo X — Sphaera Elementorum (Mondo degli elementi · Malkuth)",
        "divineName": "Adonai ha-Aretz (אדני הארץ = 65 + 296 = 361 = 19²!)", "divineHeb": "אדניהארץ",
        "sephirah": "10. Malkuth (מלכות — Il Regno)",
        "choir": "Ishim (אישים = 361 = 19²! — Animae Beatae / Heroes)",
        "archangel": "Sandalphon (סנדלפון = 280) & Zuriel (זוריאל = 254)",
        "intName": "Adonai ha-Aretz (361) & Shalel / Paciel (שלאל = 361 = 19²)", "intHeb": "שלאל", "intGem": 361,
        "spirName": "Ishim (אישים = 361 = 19²) & Qenael (קנאל = 181 = Centro)", "spirHeb": "אישים", "spirGem": 361,
        "color": "#cd6155", "signature12": "[7 - 1 - 7 - 1]",
        "shemRange": (37, 42), "mansions": [(15, "Agrapha", "Atliel", "אתליאל"), (16, "Azubene", "Azeruel", "עזרואל"), (17, "Alchil", "Adriel", "אדריאל")]
    },
    {
        "sphereNum": 11, "higherOrder": 20, "classicOrder": None, "chamber12": 8, "isExtension": True,
        "sign": "8. Scorpione (♏)", "signAngel": "Barbiel", "signAngelHeb": "ברביאל", "signAngelGem": 245,
        "permYHVH": "והיה", "month": "Cheshvan", "tribe": "Dan",
        "heavenName": "Estensione I del progetto — Porta di Tav (ת = 400 · ETH את = 401 · Tavola 20×20)",
        "divineName": "ETH (את = 401 = P₂₀ · «Alpha et Omega / Principium et Finis»)", "divineHeb": "את",
        "sephirah": "Simbolismo del progetto: Plenitudo Literarum (22 lettere · Tav ת = 400 = 20²)",
        "choir": "Custodes Quattuor Centum Mundorum (ת = 400 = 20²)",
        "archangel": "Barbiel (ברביאל = 245) & Uriel (אוריאל = 248)",
        "intName": "Athiel / Principiel (אתאל = 432 · את = 401 = P₂₀)", "intHeb": "אתאל", "intGem": 432,
        "spirName": "Thaviel / Universiel (ת = 400 = 20²)", "spirHeb": "ת", "spirGem": 400,
        "color": "#00d2d3", "signature12": "[8 - 4 - 2 - 4]",
        "shemRange": (43, 48), "mansions": [(18, "Alchas", "Egibiel", "אגיביאל"), (19, "Allatha", "Amutiel", "אמותיאל")]
    },
    {
        "sphereNum": 12, "higherOrder": 21, "classicOrder": None, "chamber12": 9, "isExtension": True,
        "sign": "9. Sagittario (♐)", "signAngel": "Advachiel", "signAngelHeb": "אדוכיאל", "signAngelGem": 72,
        "permYHVH": "וההי", "month": "Kislev", "tribe": "Beniamino",
        "heavenName": "Estensione II del progetto — Sigillo della Verità (EMETH אמת = 441 · Tavola 21×21)",
        "divineName": "EMETH (אמת = 441 = 21² · «Sigillum Dei Veritatis») & EHEIEH (אהיה = 21 = Lato N)", "divineHeb": "אמת",
        "sephirah": "Simbolismo del progetto: Corona compiuta / Ouroboros (richiamo a Kether · N = 21 = אהיה)",
        "choir": "Chayoth & Ishim Riuniti (Pilastro Puro della 9ª Camera [9-9-9-9])",
        "archangel": "Advachiel (אדוכיאל = 72 = Shem HaMephorash!) & Metatron-Sandalphon",
        "intName": "Emethiel / Veritatiel (אמתאל = 472 · אמת = 441 = 21²)", "intHeb": "אמתאל", "intGem": 472,
        "spirName": "Eheiel / Coroniel (אהיה = 21 = Lato N₂₁)", "spirHeb": "אהיה", "spirGem": 21,
        "color": "#ff9ff3", "signature12": "★ [9 - 9 - 9 - 9] (Pilastro Puro)",
        "shemRange": (49, 54), "mansions": [(20, "Abnahaya (Trabs)", "Kyriel", "קיריאל"), (21, "Abeda", "Bethnael", "בתנאל")]
    }
]

SHEM_72 = [
  ('Vehuiah','והויה'),('Jeliel','יליאל'),('Sitael','סיטאל'),('Elemiah','עלמיה'),('Mahasiah','מהשיה'),('Lelahel','ללהאל'),('Achaiah','אכאיה'),('Cahetel','כהתאל'),
  ('Haziel','הזיאל'),('Aladiah','אלדיה'),('Lauviah','לאויה'),('Hahaiah','ההעיה'),('Iezalel','יזלאל'),('Mebahel','מבהאל'),('Hariel','הריאל'),('Hakamiah','הקמיה'),
  ('Lauviah II','לאויה'),('Caliel','כליאל'),('Leuviah','לוויה'),('Pahaliah','פהליה'),('Nelchael','נלכאל'),('Yeiayel','יייאל'),('Melahel','מלהאל'),('Haheuiah','חהויה'),
  ('Nith-Haiah','נתהיה'),('Haaiah','האאיה'),('Yeratel','ירתאל'),('Seheiah','שאהיה'),('Reiyel','רייאל'),('Omael','אומאל'),('Lecabel','לכבאל'),('Vasariah','ושריה'),
  ('Yehuiah','יחויה'),('Lehahiah','להחיה'),('Chavakiah','כוקיה'),('Menadel','מנדאל'),('Aniel','אניאל'),('Haamiah','חעמיה'),('Rehael','רהעאל'),('Ieiazel','ייזאל'),
  ('Hahahel','הההאל'),('Mikhael','מיכאל'),('Veuliah','ווליה'),('Yelahiah','ילהיה'),('Sealiah','סאליה'),('Ariel','עריאל'),('Asaliah','עשליה'),('Mihael','מיהאל'),
  ('Vehuel','והואל'),('Daniel','דניאל'),('Hahasiah','החשיה'),('Imamiah','עממיה'),('Nanael','ננאאל'),('Nithael','ניתאל'),('Mebahiah','מבהיה'),('Poyel','פויאל'),
  ('Nemamiah','נממיה'),('Yeialel','יילאל'),('Harahel','הרחאל'),('Mitzrael','מצראל'),('Umabel','אומבאל'),('Iah-Hel','יההאל'),('Anauel','ענואל'),('Mehiel','מחיאל'),
  ('Damabiah','דמביה'),('Manakel','מנקאל'),('Eyael','איעאל'),('Habuhiah','חבויה'),('Rochel','ראהאל'),('Jabamiah','יבמיה'),('Haiaiel','הייאל'),('Mumiah','מומיה')
]

def validate_spheres_meta():
    """Evita di rigenerare bandiere con lettere mancanti o duplicate."""
    expected_letters = Counter('יהוה')
    banners = [s['permYHVH'] for s in SPHERES_META]
    for sphere in SPHERES_META:
        if Counter(sphere['permYHVH']) != expected_letters:
            raise ValueError(f"Bandiera YHVH non valida: {sphere['heavenName']}")
    if len(banners) != 12 or len(set(banners)) != 12:
        raise ValueError('Le dodici camere devono avere dodici permutazioni YHVH distinte.')


def known_hebrew_names():
    names = {}
    ambiguous = set()

    def register(label, hebrew):
        for alias in label.split('/'):
            alias = alias.strip()
            if not alias or alias in ambiguous:
                continue
            if alias in names and names[alias] != hebrew:
                names.pop(alias)
                ambiguous.add(alias)
            else:
                names[alias] = hebrew

    for label, hebrew in SHEM_72:
        register(label, hebrew)
    for sphere in SPHERES_META:
        register(sphere['signAngel'], sphere['signAngelHeb'])
        register(sphere['intName'].split('(')[0], sphere['intHeb'])
        register(sphere['spirName'].split('(')[0], sphere['spirHeb'])
        for _, _, label, hebrew in sphere['mansions']:
            register(label, hebrew)
        for field in ('archangel', 'divineName', 'intName', 'spirName'):
            for label, hebrew in re.findall(r"([A-Za-z][A-Za-z0-9 /'-]*?)\s*\(([א-ת ]+)", sphere[field]):
                register(label, hebrew.strip())
    for label, hebrew in known_divine_names().items():
        register(label, hebrew)
    return names


def orthography_assets(base_dir):
    spec = browser_spec(known_hebrew_names())
    with open(os.path.join(base_dir, 'orthography.js'), encoding='utf-8') as source:
        engine = source.read()
    script = ('<script id="orthography-engine">\n' + engine + '\nconst Orthography = createOrthography('
              + json.dumps(spec, ensure_ascii=False).replace('<', '\\u003c') + ');\nconst ORTHOGRAPHY_SPHERES = '
              + json.dumps(SPHERES_META, ensure_ascii=False).replace('<', '\\u003c') + ';\n</script>\n')
    rows = ''.join(f"<tr><td class=\"hebrew\">{ch}</td><td>{info['name']}</td><td>{info['roman']}</td><td>{info['val']}</td><td>{info.get('valFinal', info['val'])}</td></tr>"
                   for ch, info in HEBREW_ALPHABET.items())
    guide = '''<!-- orthography-guide:start -->
<details id="orthography-guide" style="margin:12px 0; padding:12px; border:1px solid var(--cyan); border-radius:8px; overflow-wrap:anywhere;">
  <summary style="cursor:pointer; color:var(--cyan); font-weight:bold;">Lettere, traslitterazione e convenzioni numeriche</summary>
  <p>I nomi presenti nell'archivio usano la grafia ebraica associata. Per altri nomi latini la conversione è convenzionale: è possibile scrivere direttamente l'ebraico o specificarne la grafia nel calcolatore.</p>
  <p>I nomi strutturali generati mostrano tutte le consonanti, separate da <code>·</code>. <code>ʾ</code> = Aleph, <code>ʿ</code> = Ayin, <code>ḥ</code> = Cheth, <code>ṭ</code> = Teth, <code>ṣ</code> = Tsadi, <code>š</code> = Shin. Le vocali richiedono una grafia attestata. Le forme finali sono applicate a fine parola nella conversione latina.</p>
  <p><strong>Gematria ebraica:</strong> i calcoli e i sigilli usano i valori ordinari, anche per le lettere finali. La colonna «finali estese» documenta la variante 500–900. I numerali usano <code>טו</code> per 15 e <code>טז</code> per 16; zero ha grafia vuota. Il valore di una cella o di un parametro e la somma del nome con suffisso sono indicati separatamente.</p>
  <p><strong>Tabella latina di Agrippa, resa con lettere moderne distinte:</strong> A=1, B=2, C=3, D=4, E=5, F=6, G=7, H=8, I=9; K=10, L=20, M=30, N=40, O=50, P=60, Q=70, R=80, S=90; T=100, U=200, X=300, Y=400, Z=500; J=600, V=700, HI aspirata=800, HV aspirata=900. Nell'input <code>[I]</code>, <code>[V]</code>, <code>[HI]</code>, <code>[HV]</code> indicano esplicitamente le quattro forme aggiuntive. W è trattata come HV=900. Una sequenza HI senza parentesi vale H+I.</p>
  <p><a href="https://www.esotericarchives.com/agrippa/agripp2b.htm" target="_blank" rel="noopener noreferrer">Agrippa, libro II, cap. 19–20</a> · <a href="https://www.loc.gov/catdir/cpso/romanization/hebrew.pdf" target="_blank" rel="noopener noreferrer">Consonanti e vocali nella romanizzazione ebraica (Library of Congress)</a></p>
  <div style="overflow-x:auto;"><table style="width:100%; border-collapse:collapse;"><thead><tr><th>Ebraico</th><th>Lettera</th><th>Traslitterazione</th><th>Valore ordinario</th><th>Finali estese</th></tr></thead><tbody>''' + rows + '''</tbody></table></div>
</details>
<!-- orthography-guide:end -->'''
    return script, guide


def lunar_assets(base_dir):
    spec = export_lunar_catalog(SPHERES_META, base_dir)
    sources = []
    for filename in ('vendor/astronomy.browser.min.js', 'lunar_engine.js', 'lunar_ui.js'):
        with open(os.path.join(base_dir, filename), encoding='utf-8') as source:
            sources.append(source.read())
    script = '<script id="lunar-engine">\n' + '\n'.join(sources)
    script += '\nconst LunarEngine = createLunarEngine(Astronomy, Orthography, ' + json.dumps(spec, ensure_ascii=False).replace('<', '\\u003c') + ');\n'
    script += '''const LunarUI = createLunarUI(LunarEngine, Orthography);
DivineNamesUI.setLunarSeedHandler((order, hebrew) => {
  const panel = document.querySelector(`[data-lunar-panel="${order}"]`);
  if (!panel) return;
  panel.querySelector('[data-lunar-seed]').value = hebrew;
  panel.open = true;
  LunarUI.refreshPanels();
  panel.scrollIntoView({behavior:'smooth', block:'center'});
});
</script>
'''
    return script


def divine_name_assets(base_dir):
    spec = export_shem42(base_dir)
    with open(os.path.join(base_dir, 'divine_names_ui.js'), encoding='utf-8') as source:
        engine = source.read()
    script = '<script id="divine-names-engine">\n' + engine
    script += '\nconst DivineNamesUI = createDivineNamesUI(Orthography, ' + json.dumps(spec, ensure_ascii=False).replace('<', '\\u003c') + ');\n</script>\n'
    return script, shem42_overview(spec)


def embed_orthography(page, script, guide, lunar_script='', divine_script='', divine_overview=''):
    page = re.sub(r'<script id="(?:orthography-engine|lunar-engine|divine-names-engine)">.*?</script>\s*', '', page, flags=re.S)
    page = page.replace('<script>', script + divine_script + lunar_script + '<script>', 1)
    page = re.sub(r'<!-- orthography-guide:start -->.*?<!-- orthography-guide:end -->', lambda _: guide, page, flags=re.S)
    if '<!-- divine42-overview:start -->' in page:
        page = re.sub(r'<!-- divine42-overview:start -->.*?<!-- divine42-overview:end -->', lambda _: divine_overview, page, flags=re.S)
    elif divine_overview:
        page = page.replace('<!-- orthography-guide:start -->', divine_overview + '\n<!-- orthography-guide:start -->', 1)
    return page


def escape_inline_arguments(page):
    """Protegge apostrofi e virgolette dei nomi nei pulsanti generati."""
    def attribute(match):
        code = re.sub(r"'\$\{([^{}]+)\}'", lambda arg: arg[0] if arg[1].startswith('Orthography.inlineText(')
                      else "'${Orthography.inlineText(" + arg[1] + ")}'", match[1])
        return 'onclick="' + code + '"'
    return re.sub(r'onclick="([^"\n]*)"', attribute, page)


def build_html():
    validate_spheres_meta()
    base_dir = os.path.dirname(__file__)
    build_shem42_generator(base_dir)
    json_path = os.path.join(base_dir, 'table_angels_generated.json')
    generate_all()
    with open(json_path, 'r', encoding='utf-8') as f:
        tables_data = json.load(f)

    # Aggiunge le matrici alle tavole per il rendering JS del quadrato magico e del sigillo
    for order in range(3, 22):
        tables_data[f"table_{order}"]["matrix"] = generate_magic_square(order)
    orthography_script, orthography_guide = orthography_assets(base_dir)
    divine_script, divine_overview = divine_name_assets(base_dir)
    lunar_script = lunar_assets(base_dir)

    payload_json = json.dumps({
        "spheres": SPHERES_META,
        "tables": tables_data,
        "shem72": SHEM_72
    }, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Atlante angelico: 10 sfere e 2 estensioni (19 tavole 3×3 → 21×21)</title>
  <style>
    :root {{
      --bg-dark: #090a10;
      --bg-card: #121521;
      --bg-panel: #171b2b;
      --gold: #d4af37;
      --gold-bright: #f5d76e;
      --cyan: #00d2d3;
      --green: #2ecc71;
      --orange: #f39c12;
      --text-main: #eceff4;
      --text-muted: #9aa5b1;
      --border: rgba(212, 175, 55, 0.28);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      background: radial-gradient(circle at top, #15192b 0%, #090a10 70%);
      color: var(--text-main);
      line-height: 1.5;
      overflow-wrap: anywhere;
    }}
    header {{
      text-align: center;
      padding: 28px 20px 22px;
      border-bottom: 2px solid var(--border);
      background: linear-gradient(180deg, rgba(212,175,55,0.12) 0%, rgba(9,10,16,0.95) 100%);
    }}
    .subtitle {{
      color: var(--gold);
      text-transform: uppercase;
      letter-spacing: 2px;
      font-size: 0.82rem;
    }}
    h1 {{
      color: var(--gold-bright);
      font-size: 1.75rem;
      margin: 6px 0 8px;
    }}
    .container {{
      max-width: 1500px;
      margin: 0 auto;
      padding: 20px;
    }}
    .nav-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      justify-content: space-between;
      align-items: center;
      background: var(--bg-card);
      border: 1px solid var(--border);
      padding: 12px 16px;
      border-radius: 10px;
      margin-bottom: 18px;
      position: sticky;
      top: 8px;
      z-index: 50;
      box-shadow: 0 8px 24px rgba(0,0,0,0.65);
    }}
    button, .btn-link {{
      background: rgba(212, 175, 55, 0.12);
      color: var(--gold-bright);
      border: 1px solid var(--border);
      padding: 7px 13px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.84rem;
      text-decoration: none;
      transition: all 0.18s;
      max-width: 100%;
      overflow-wrap: anywhere;
    }}
    button:hover, .btn-link:hover, button.active {{
      background: rgba(212, 175, 55, 0.28);
      border-color: var(--gold-bright);
      color: #fff;
    }}
    input[type="search"] {{
      background: #0b0d16;
      color: var(--text-main);
      border: 1px solid var(--cyan);
      padding: 8px 14px;
      border-radius: 6px;
      min-width: 300px;
      font-size: 0.9rem;
    }}
    .hebrew {{
      font-family: 'Times New Roman', 'David', serif;
      font-size: 1.12em;
      direction: rtl;
      display: inline-block;
      color: var(--gold-bright);
    }}
    .badge {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 99px;
      font-size: 0.74rem;
      border: 1px solid var(--border);
      background: rgba(212,175,55,0.1);
      color: var(--gold-bright);
    }}
    .section-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 18px 20px;
      margin-bottom: 24px;
      box-shadow: 0 6px 20px rgba(0,0,0,0.45);
    }}
    .heaven-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      padding-bottom: 12px;
      margin-bottom: 14px;
      border-bottom: 1px solid var(--border);
    }}
    .heaven-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.25fr) minmax(0, 0.95fr);
      gap: 18px;
      align-items: start;
    }}
    @media (max-width: 1100px) {{
      .heaven-grid {{ grid-template-columns: minmax(0, 1fr); }}
    }}
    .info-box {{
      background: var(--bg-panel);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 8px;
      padding: 10px 14px;
      margin-bottom: 10px;
      font-size: 0.87rem;
    }}
    table.angels-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.81rem;
      margin-top: 6px;
    }}
    table.angels-table th, table.angels-table td {{
      border: 1px solid rgba(212,175,55,0.2);
      padding: 5px 8px;
      text-align: left;
      overflow-wrap: anywhere;
    }}
    table.angels-table th {{
      background: rgba(212,175,55,0.14);
      color: var(--gold-bright);
    }}
    table.angels-table tr:hover {{
      background: rgba(0,210,211,0.08);
    }}
    .kamea-wrap {{
      display: flex;
      flex-direction: column;
      align-items: center;
      background: #0c0e17;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px;
      min-width: 0;
      overflow-x: auto;
    }}
    .kamea-stage {{
      position: relative;
      border: 2px solid var(--gold);
      background: #08090f;
      margin: 8px 0;
      flex-shrink: 0;
      align-self: flex-start;
      margin-left: auto;
      margin-right: auto;
    }}
    .kamea-grid {{
      display: grid;
    }}
    .kamea-cell {{
      border: 1px solid rgba(212,175,55,0.18);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-size: 0.68rem;
      color: var(--text-main);
      user-select: none;
    }}
    .kamea-cell.active-cell {{
      background: rgba(0, 210, 211, 0.28);
      color: #fff;
      font-weight: bold;
    }}
    .sigil-svg {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
    }}
    .two-col-tables {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
      gap: 12px;
    }}
    @media (max-width: 800px) {{
      .two-col-tables {{ grid-template-columns: minmax(0, 1fr); }}
    }}
    .heaven-grid > *, .two-col-tables > * {{ min-width: 0; }}
  </style>
</head>
<body>

<header>
  <div class="subtitle">Agrippa · Dieci sfere e sette tavole planetarie · Estensioni numeriche del progetto</div>
  <h1>Atlante angelico delle 10 sfere e delle 2 estensioni</h1>
  <p style="max-width:980px; margin:0 auto; color:var(--text-muted); font-size:0.94rem;">
    Le <strong>10 sfere</strong> sono ordinate da Kether e Primum Mobile a Malkuth e mondo degli elementi.
    L'atlante comprende <strong>7 tavole classiche (3×3 → 9×9)</strong>, <strong>12 tavole estese del progetto (10×10 → 21×21)</strong>,
    <strong>779 voci strutturali generate</strong>, <strong>72 angeli dello Shem HaMephorash</strong> e <strong>28 angeli delle mansioni lunari</strong>.
  </p>
</header>

<div class="container">
  <div class="section-card" id="readingGuide">
    <h2 style="color:var(--gold-bright); margin-top:0; font-size:1.15rem;">Sfere, segni e tavole: come leggere l'atlante</h2>
    <p><strong>Ordine delle dieci sfere:</strong> Primum Mobile → stelle fisse / Zodiaco → Saturno → Giove → Marte → Sole → Venere → Mercurio → Luna → elementi.</p>
    <p><strong>Dodici segni:</strong> sono le suddivisioni dello Zodiaco. Qui la camera di ogni tavola segue la convenzione numerica del progetto:
      <code>Camera = ((N − 1) mod 12) + 1</code>, con N uguale al lato della tavola e Camera 1 associata all'Ariete.
      Gli abbinamenti ai segni, la distribuzione dello Shem e delle mansioni nelle schede e le firme numeriche seguono questa convenzione.</p>
    <p><strong>Estensioni del progetto:</strong> le tavole 10×10 → 21×21 e i relativi nomi strutturali sviluppano il modello numerico.
      Le schede Porta di Tav e Sigillo della Verità sono presentate separatamente come due estensioni simboliche.
      I nomi generati e le associazioni simboliche richiedono questa distinzione rispetto alle corrispondenze storiche.</p>
    <p style="margin-bottom:0; color:var(--text-muted);">Riferimento:
      <a class="btn-link" href="https://www.esotericarchives.com/agrippa/agripp2b.htm" target="_blank" rel="noopener noreferrer">Agrippa, libro II: cap. 13 (dieci sfere), 14 (dodici segni), 22 (sette tavole planetarie)</a>
    </p>
  </div>
  {orthography_guide}
  {divine_overview}
  <section class="section-card" id="lunarWorkbench">
    <h2 style="color:var(--cyan); margin-top:0;">☽ Calcolo lunare e nomi derivati sulle tavole</h2>
    <p>La mansione segue la posizione lunare nei 360° del riferimento scelto. La fase è calcolata dal rapporto Luna–Sole nello stesso istante UTC.
      Apri il pannello lunare di una tavola per generare e tracciare i nove gradi dalla colonna della Luna di Agrippa III.27.</p>
    <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:end;">
      <label>Data gregoriana<br/><input id="lunarDate" type="date" min="0001-01-01" max="3000-12-31" onchange="updateAtlasLunar()"/></label>
      <label>Ora locale<br/><input id="lunarTime" type="time" value="12:00" onchange="updateAtlasLunar()"/></label>
      <label>Scarto da UTC (ore, inclusa ora legale)<br/><input id="lunarUtcOffset" type="number" min="-14" max="14" step="0.25" value="0" style="width:130px;" onchange="updateAtlasLunar()"/></label>
      <label>Riferimento delle mansioni<br/><select id="lunarFrame" onchange="updateAtlasLunar()"><option value="tropical">Tropicale</option><option value="sidereal">Sidereo · ayanamsha dichiarata</option></select></label>
      <label>Ayanamsha siderea (°)<br/><input id="lunarAyanamsha" type="number" step="0.0001" placeholder="Vuoto: stima lineare" style="width:170px;" onchange="updateAtlasLunar()"/></label>
      <label>Suffisso dei nomi<br/><select id="lunarSuffix" onchange="updateAtlasLunar()"><option value="אל">El · אל</option><option value="יה">Yah · יה</option></select></label>
      <button type="button" onclick="setAtlasLunarNow()">Adesso, in UTC</button>
    </div>
    <div id="lunarStatePanel" aria-live="polite"></div>
    <p><a class="btn-link" href="lunar_generated_angels.md">Catalogo dei 252 nomi lunari derivati</a> · <a class="btn-link" href="lunar_angels_generated.json">Dati e passaggi in JSON</a></p>
  </section>
  <!-- Barra di Navigazione e Ricerca Istantanea -->
  <div class="nav-bar">
    <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
      <a class="btn-link" href="index.html">⬅ Torna al Calcolatore & Atlante Principale (index.html)</a>
      <a class="btn-link" href="complete_angel_catalog.html">Catalogo completo in ebraico, raggruppato per sfera →</a>
      <button id="btnModeAll" class="active" onclick="setFilterMode('all')">Tutte le 19 tavole (779 voci)</button>
      <button id="btnModeHigher" onclick="setFilterMode('higher')">12 tavole estese del progetto (10×10 → 21×21 · 576 voci)</button>
      <button id="btnModeClassic" onclick="setFilterMode('classic')">7 tavole classiche (3×3 → 9×9 · 203 voci)</button>
      <button id="btnSortChamber" onclick="setFilterMode('chamber')" style="border-color:var(--cyan); color:var(--cyan);">✡ Ordina per Camera (Camera 1 ♈ → Camera 12 ♓)</button>
    </div>
    <div>
      <input type="search" id="searchBox" placeholder="🔍 Cerca qualsiasi Angelo (Latino, Ebraico, Gematria, Cella, Segno)..." oninput="renderEncyclopedia()" />
    </div>
  </div>

  <!-- Dieci sfere tradizionali e due estensioni simboliche del progetto -->
  <div class="section-card">
    <h2 style="color:var(--gold-bright); margin-top:0; font-size:1.25rem;">
      🏛️ Tavola sinottica delle 10 sfere e delle 2 estensioni simboliche
    </h2>
    <div style="overflow-x:auto;">
      <table class="angels-table" id="synopticHeavensTable">
        <thead>
          <tr>
            <th>Sfera / Estensione</th>
            <th>Camera tavola estesa & Segno associato</th>
            <th>Tavola Estesa & Classica</th>
            <th>Firma 12 Camere</th>
            <th>Nome Divino & Bandiera YHVH</th>
            <th>Sephirah / Simbolismo & Coro</th>
            <th>Arcangelo & Principe del Segno</th>
            <th>Associazioni numeriche: Intelligenza & Spirito</th>
            <th>I 6 Angeli Shem HaMephorash</th>
            <th>Angeli Mansioni Lunari</th>
          </tr>
        </thead>
        <tbody id="synopticBody"></tbody>
      </table>
    </div>
  </div>

  <!-- Schede delle dieci sfere e delle due estensioni del progetto -->
  <div id="heavensContainer"></div>
</div>

{orthography_script}{divine_script}{lunar_script}<script>
const DATA = {payload_json};

const HEBREW_VALS = Object.fromEntries(Object.entries(Orthography.letters).map(([ch, info]) => [ch, info.val]));

let currentMode = 'all'; // 'all' | 'higher' | 'classic' | 'chamber'

function sphereLabel(s) {{
  return s.isExtension ? `Estensione ${{s.sphereNum - 10}} del progetto` : `Sfera ${{s.sphereNum}}`;
}}

function updateAtlasLunar() {{
  try {{
    const dateText = document.getElementById('lunarDate').value;
    const offset = Number(document.getElementById('lunarUtcOffset').value);
    const instant = LunarEngine.instant(dateText, document.getElementById('lunarTime').value, offset);
    const sidereal = document.getElementById('lunarFrame').value === 'sidereal';
    const explicit = document.getElementById('lunarAyanamsha').value.trim();
    const ayanamsha = explicit ? Number(explicit) : 23.853 + (Number(dateText.slice(0,4)) - 2000) * 0.01396;
    const frame = sidereal ? `Sidereo · ayanamsha ${{ayanamsha.toFixed(4)}}° (${{explicit ? 'manuale' : 'stima lineare'}})` : 'Tropicale';
    LunarUI.setState(LunarEngine.stateAt(instant, {{shift:sidereal ? -ayanamsha : 0, frame, offsetHours:offset, suffix:document.getElementById('lunarSuffix').value}}));
  }} catch (error) {{ LunarUI.showError(error.message || String(error)); }}
}}

function setAtlasLunarNow() {{
  const utc = new Date().toISOString();
  document.getElementById('lunarDate').value = utc.slice(0,10);
  document.getElementById('lunarTime').value = utc.slice(11,16);
  document.getElementById('lunarUtcOffset').value = '0';
  updateAtlasLunar();
}}

function setFilterMode(mode) {{
  currentMode = mode;
  ['btnModeAll','btnModeHigher','btnModeClassic','btnSortChamber'].forEach(id => {{
    const el = document.getElementById(id);
    if (el) el.classList.remove('active');
  }});
  if (mode === 'all') document.getElementById('btnModeAll').classList.add('active');
  if (mode === 'higher') document.getElementById('btnModeHigher').classList.add('active');
  if (mode === 'classic') document.getElementById('btnModeClassic').classList.add('active');
  if (mode === 'chamber') document.getElementById('btnSortChamber').classList.add('active');
  renderEncyclopedia();
}}

function renderSynopticTable() {{
  const tbody = document.getElementById('synopticBody');
  let list = [...DATA.spheres];
  if (currentMode === 'chamber') {{
    list.sort((a, b) => a.chamber12 - b.chamber12);
  }} else if (currentMode === 'classic') {{
    list = list.filter(s => s.classicOrder !== null);
  }}
  tbody.innerHTML = list.map(s => {{
    const [shStart, shEnd] = s.shemRange;
    const shemNames = DATA.shem72.slice(shStart - 1, shEnd).map((x, idx) => `#${{shStart+idx}} ${{x[0]}} (<span class="hebrew">${{x[1]}}</span>)`).join(', ');
    const mansNames = s.mansions.map(m => `${{m[0]}}ª ${{m[2]}} (<span class="hebrew">${{m[3]}}</span>)`).join(', ');
    const tSup = DATA.tables['table_' + s.higherOrder];
    const tCls = s.classicOrder ? DATA.tables['table_' + s.classicOrder] : null;
    return `
      <tr onclick="document.getElementById('heaven-card-${{s.sphereNum}}').scrollIntoView({{behavior:'smooth'}})" style="cursor:pointer;">
        <td><strong style="color:${{s.color}}">${{sphereLabel(s)}}</strong><br/><span style="font-size:0.74rem; color:var(--text-muted)">${{s.heavenName}}</span></td>
        <td><strong style="color:var(--cyan)">Camera ${{s.chamber12}}</strong><br/><strong>${{s.sign}}</strong></td>
        <td>
          <span class="badge">Estesa ${{s.higherOrder}}×${{s.higherOrder}} (M=${{tSup.M_magic}})</span>
          ${{tCls ? `<br/><span class="badge" style="margin-top:3px; opacity:0.85;">Classica ${{s.classicOrder}}×${{s.classicOrder}} (M=${{tCls.M_magic}})</span>` : ''}}
        </td>
        <td><code style="color:var(--green)">${{s.signature12}}</code></td>
        <td>${{s.divineName}}<br/>Bandiera: <span class="hebrew">${{s.permYHVH}}</span></td>
        <td>${{s.sephirah}}<br/><span style="color:var(--text-muted)">${{s.choir}}</span></td>
        <td>${{s.archangel}}<br/>Principe: <strong style="color:var(--cyan)">${{s.signAngel}} (<span class="hebrew">${{s.signAngelHeb}}</span> = ${{s.signAngelGem}})</strong></td>
        <td><strong style="color:var(--cyan)">${{s.intName}}</strong><br/><strong style="color:var(--orange)">${{s.spirName}}</strong></td>
        <td style="font-size:0.75rem;">${{shemNames}}</td>
        <td style="font-size:0.75rem;">${{mansNames}}</td>
      </tr>
    `;
  }}).join('');
}}

function reduceToCell(val, maxCell) {{
  let v = val;
  while (v > maxCell) {{
    if (v % 10 === 0) {{
      v = Math.floor(v / 10);
    }} else {{
      const root = Math.floor(v / 10);
      v = (root > 0 && root <= maxCell) ? root : (((v - 1) % maxCell) + 1);
    }}
  }}
  return v < 1 ? 1 : v;
}}

function findCoords(matrix, num) {{
  for (let r = 0; r < matrix.length; r++) {{
    for (let c = 0; c < matrix[r].length; c++) {{
      if (matrix[r][c] === num) return {{ r, c }};
    }}
  }}
  return {{ r: 0, c: 0 }};
}}

function traceAngelOnTable(tableOrder, role, latinName, hebrewStr, gematriaVal) {{
  const tData = DATA.tables['table_' + tableOrder];
  if (!tData) return;
  const n = tData.order;
  const maxCell = tData.cells;
  const cellSize = n >= 16 ? 24 : (n >= 11 ? 30 : 40);

  // Pulisci celle attive
  for (let i = 1; i <= maxCell; i++) {{
    const el = document.getElementById(`kcell-${{tableOrder}}-${{i}}`);
    if (el) el.classList.remove('active-cell');
  }}

  const steps = [];
  for (const ch of hebrewStr) {{
    const val = HEBREW_VALS[ch];
    if (!val) continue;
    const cellNum = reduceToCell(val, maxCell);
    const coords = findCoords(tData.matrix, cellNum);
    steps.push({{ ch, val, cellNum, r: coords.r, c: coords.c }});
    const el = document.getElementById(`kcell-${{tableOrder}}-${{cellNum}}`);
    if (el) el.classList.add('active-cell');
  }}

  const svg = document.getElementById(`ksvg-${{tableOrder}}`);
  if (svg && steps.length > 0) {{
    const pts = steps.map(st => ({{
      x: st.c * cellSize + cellSize / 2,
      y: st.r * cellSize + cellSize / 2
    }}));
    const poly = pts.map(p => `${{p.x}},${{p.y}}`).join(' ');
    const start = pts[0];
    const end = pts[pts.length - 1];
    svg.innerHTML = `
      <polyline points="${{poly}}" fill="none" stroke="#00d2d3" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" />
      <circle cx="${{start.x}}" cy="${{start.y}}" r="5" fill="none" stroke="#f5d76e" stroke-width="2.2" />
      <line x1="${{end.x - 5}}" y1="${{end.y - 5}}" x2="${{end.x + 5}}" y2="${{end.y + 5}}" stroke="#f39c12" stroke-width="2.4" />
    `;
  }}

  const statusEl = document.getElementById(`kstatus-${{tableOrder}}`);
  if (statusEl) {{
    const pathStr = steps.map(st => `${{st.ch}}(${{st.val}}→cella ${{st.cellNum}})`).join(' → ');
    statusEl.innerHTML = `
      <div style="color:var(--gold-bright); font-weight:bold;">Sigillo Attivo: ${{latinName}} (<span class="hebrew">${{hebrewStr}}</span> = ${{gematriaVal}})</div>
      <div style="color:var(--cyan); font-size:0.78rem;">Ruolo: ${{role}}</div>
      <div style="color:var(--text-muted); font-size:0.75rem; margin-top:2px;">Percorso Celle: ${{pathStr}}</div>
    `;
  }}
}}

function renderSingleTableSection(tData, sphereMeta, filterQuery) {{
  const n = tData.order;
  const cellSize = n >= 16 ? 24 : (n >= 11 ? 30 : 40);
  const c = tData.cardinals;
  const d = tData.diagonals;
  const ctr = tData.center.angel;
  const mrg = tData.margins;
  const cst = tData.constants;

  // Filtra righe e colonne se c'è una ricerca attiva
  const q = (filterQuery || '').trim().toLowerCase();
  const matchAng = (a, extraText) => {{
    if (!q) return true;
    const hay = `${{a.latin}} ${{a.hebrew}} ${{a.gematria}} ${{extraText || ''}}`.toLowerCase();
    return hay.includes(q);
  }};

  const rowsFiltered = tData.rows.filter(r => matchAng(r, `riga R${{r.row_num}} ${{r.start_cell}} ${{r.end_cell}}`));
  const colsFiltered = tData.columns.filter(col => matchAng(col, `colonna C${{col.col_num}} ${{col.top_cell}} ${{col.bot_cell}}`));

  const gridHtml = tData.matrix.map(row =>
    row.map(num => `<div class="kamea-cell" id="kcell-${{n}}-${{num}}" style="width:${{cellSize}}px; height:${{cellSize}}px;">${{num}}</div>`).join('')
  ).join('');

  return `
    <div style="margin-top:14px; padding-top:14px; border-top:1px dashed rgba(212,175,55,0.3);">
      <h3 style="color:var(--gold-bright); margin:0 0 10px;">
        📐 ${{tData.title}} — Parametri: N=${{n}}, N²=${{tData.cells}}, P=${{tData.P_polar}}, M=${{tData.M_magic}}, S=${{tData.S_total}}
      </h3>
      <p style="color:var(--text-muted); font-size:0.82rem;">
        ${{n >= 10 ? 'Tavola estesa del progetto' : 'Tavola planetaria classica'}} ·
        Camera numerica della tavola: ${{tData.chamber12}} · Segno associato per convenzione: ${{tData.zodiac_sign}}
      </p>

      <div class="heaven-grid">
        <div>
          <!-- Cardini, Diagonali, Cuore, Margini e Costanti -->
          <div class="info-box">
            <div style="color:var(--orange); font-weight:bold; margin-bottom:6px;">🧭 I 4 Cardini Angolari, Corona (2P=${{c.Ring_4_Corners.sum}}) & Cuore Centrale (Clicca per tracciare il Sigillo):</div>
            <div style="display:flex; flex-wrap:wrap; gap:6px;">
              <button onclick="traceAngelOnTable(${{n}}, 'Cardine NW (Cella ${{c.NW.cell}})', '${{c.NW.latin}}', '${{c.NW.hebrew}}', ${{c.NW.gematria}})">
                NW (Cella ${{c.NW.cell}}): <strong>${{c.NW.latin}}</strong> (<span class="hebrew">${{c.NW.hebrew}}</span> = ${{c.NW.gematria}})
              </button>
              <button onclick="traceAngelOnTable(${{n}}, 'Cardine NE (Cella ${{c.NE.cell}})', '${{c.NE.latin}}', '${{c.NE.hebrew}}', ${{c.NE.gematria}})">
                NE (Cella ${{c.NE.cell}}): <strong>${{c.NE.latin}}</strong> (<span class="hebrew">${{c.NE.hebrew}}</span> = ${{c.NE.gematria}})
              </button>
              <button onclick="traceAngelOnTable(${{n}}, 'Cardine SW (Cella ${{c.SW.cell}})', '${{c.SW.latin}}', '${{c.SW.hebrew}}', ${{c.SW.gematria}})">
                SW (Cella ${{c.SW.cell}}): <strong>${{c.SW.latin}}</strong> (<span class="hebrew">${{c.SW.hebrew}}</span> = ${{c.SW.gematria}})
              </button>
              <button onclick="traceAngelOnTable(${{n}}, 'Cardine SE (Cella ${{c.SE.cell}})', '${{c.SE.latin}}', '${{c.SE.hebrew}}', ${{c.SE.gematria}})">
                SE (Cella ${{c.SE.cell}}): <strong>${{c.SE.latin}}</strong> (<span class="hebrew">${{c.SE.hebrew}}</span> = ${{c.SE.gematria}})
              </button>
              <button onclick="traceAngelOnTable(${{n}}, 'Corona dei 4 Angoli (2P=${{c.Ring_4_Corners.sum}})', '${{c.Ring_4_Corners.latin}}', '${{c.Ring_4_Corners.hebrew}}', ${{c.Ring_4_Corners.gematria}})" style="border-color:var(--orange);">
                Corona 4A (2P=${{c.Ring_4_Corners.sum}}): <strong>${{c.Ring_4_Corners.latin}}</strong> (<span class="hebrew">${{c.Ring_4_Corners.hebrew}}</span>)
              </button>
              <button onclick="traceAngelOnTable(${{n}}, '${{ctr.role}}', '${{ctr.latin}}', '${{ctr.hebrew}}', ${{ctr.gematria}})" style="border-color:var(--cyan);">
                Cuore Centrale: <strong>${{ctr.latin}}</strong> (<span class="hebrew">${{ctr.hebrew}}</span> = ${{ctr.gematria}})
              </button>
            </div>
          </div>

          <div class="info-box">
            <div style="color:var(--gold-bright); font-weight:bold; margin-bottom:6px;">⚡ Le 2 Grandi Diagonali, i 4 Margini & le 5 Costanti Universali:</div>
            <div style="display:flex; flex-wrap:wrap; gap:6px;">
              <button onclick="traceAngelOnTable(${{n}}, 'Diagonale Solare Discendente (M=${{tData.M_magic}})', '${{d.descending.latin}}', '${{d.descending.hebrew}}', ${{d.descending.gematria}})">
                Diag. Solare \\ (${{d.descending.start_cell}}→${{d.descending.end_cell}}): <strong>${{d.descending.latin}}</strong> (<span class="hebrew">${{d.descending.hebrew}}</span> = ${{d.descending.gematria}})
              </button>
              <button onclick="traceAngelOnTable(${{n}}, 'Diagonale Lunare Ascendente (M=${{tData.M_magic}})', '${{d.ascending.latin}}', '${{d.ascending.hebrew}}', ${{d.ascending.gematria}})">
                Diag. Lunare / (${{d.ascending.start_cell}}→${{d.ascending.end_cell}}): <strong>${{d.ascending.latin}}</strong> (<span class="hebrew">${{d.ascending.hebrew}}</span> = ${{d.ascending.gematria}})
              </button>
              <button onclick="traceAngelOnTable(${{n}}, 'Margine Nord/Sud/Ovest/Est', '${{mrg.North.latin}}', '${{mrg.North.hebrew}}', ${{mrg.North.gematria}})">
                4 Margini (N/S/W/E): <strong>${{mrg.North.latin}}</strong> (<span class="hebrew">${{mrg.North.hebrew}}</span> = ${{mrg.North.gematria}})
              </button>
              <button onclick="traceAngelOnTable(${{n}}, 'Angelo Lato N=${{n}}', '${{cst.order.latin}}', '${{cst.order.hebrew}}', ${{cst.order.gematria}})">
                Lato N=${{n}}: <strong>${{cst.order.latin}}</strong> (<span class="hebrew">${{cst.order.hebrew}}</span>)
              </button>
              <button onclick="traceAngelOnTable(${{n}}, 'Angelo Quadrato N²=${{tData.cells}}', '${{cst.cells.latin}}', '${{cst.cells.hebrew}}', ${{cst.cells.gematria}})">
                Celle N²=${{tData.cells}}: <strong>${{cst.cells.latin}}</strong> (<span class="hebrew">${{cst.cells.hebrew}}</span>)
              </button>
              <button onclick="traceAngelOnTable(${{n}}, 'Angelo Simmetria P=${{tData.P_polar}}', '${{cst.polar.latin}}', '${{cst.polar.hebrew}}', ${{cst.polar.gematria}})">
                Simmetria P=${{tData.P_polar}}: <strong>${{cst.polar.latin}}</strong> (<span class="hebrew">${{cst.polar.hebrew}}</span>)
              </button>
              <button onclick="traceAngelOnTable(${{n}}, 'Angelo Costante Magica M=${{tData.M_magic}}', '${{cst.magic.latin}}', '${{cst.magic.hebrew}}', ${{cst.magic.gematria}})">
                Costante M=${{tData.M_magic}}: <strong>${{cst.magic.latin}}</strong> (<span class="hebrew">${{cst.magic.hebrew}}</span>)
              </button>
              <button onclick="traceAngelOnTable(${{n}}, 'Angelo Totale S=${{tData.S_total}}', '${{cst.total.latin}}', '${{cst.total.hebrew}}', ${{cst.total.gematria}})">
                Totale S=${{tData.S_total}}: <strong>${{cst.total.latin}}</strong> (<span class="hebrew">${{cst.total.hebrew}}</span> = ${{cst.total.gematria}})
              </button>
            </div>
          </div>

          <!-- Tabelle complete degli N Angeli delle Righe e degli N Pilastri delle Colonne -->
          <div class="two-col-tables">
            <div class="info-box" style="margin-bottom:0;">
              <div style="color:var(--cyan); font-weight:bold; margin-bottom:4px;">📜 Tutti gli ${{n}} Angeli delle ${{n}} Righe Orizzontali (Somma Riga = ${{tData.M_magic}}):</div>
              <table class="angels-table">
                <thead>
                  <tr><th>Riga</th><th>Celle</th><th>Traslitterazione completa</th><th>Ebraico</th><th>Gem.</th><th>Cam.12</th></tr>
                </thead>
                <tbody>
                  ${{rowsFiltered.map(r => `
                    <tr onclick="traceAngelOnTable(${{n}}, 'Angelo ${{r.row_num}}ª Riga (${{r.start_cell}}↔${{r.end_cell}})', '${{r.latin}}', '${{r.hebrew}}', ${{r.gematria}})" style="cursor:pointer;" title="Clicca per tracciare il Sigillo">
                      <td><strong>R${{r.row_num}}</strong></td>
                      <td>${{r.start_cell}} ↔ ${{r.end_cell}}</td>
                      <td><strong style="color:var(--gold-bright)">${{r.latin}}</strong></td>
                      <td><span class="hebrew">${{r.hebrew}}</span></td>
                      <td>${{r.gematria}}</td>
                      <td>Cam.${{r.chamber12}}</td>
                    </tr>
                  `).join('')}}
                </tbody>
              </table>
            </div>

            <div class="info-box" style="margin-bottom:0;">
              <div style="color:var(--green); font-weight:bold; margin-bottom:4px;">🏛️ Tutti gli ${{n}} Pilastri delle ${{n}} Colonne Verticali (Somma Col. = ${{tData.M_magic}}):</div>
              <table class="angels-table">
                <thead>
                  <tr><th>Col.</th><th>Vertici</th><th>Traslitterazione completa</th><th>Ebraico</th><th>Gem.</th><th>Cam.12</th></tr>
                </thead>
                <tbody>
                  ${{colsFiltered.map(col => `
                    <tr onclick="traceAngelOnTable(${{n}}, 'Pilastro ${{col.col_num}}ª Colonna (${{col.top_cell}}↕${{col.bot_cell}})', '${{col.latin}}', '${{col.hebrew}}', ${{col.gematria}})" style="cursor:pointer;" title="Clicca per tracciare il Sigillo">
                      <td><strong>C${{col.col_num}}</strong></td>
                      <td>${{col.top_cell}} ↕ ${{col.bot_cell}}</td>
                      <td><strong style="color:var(--gold-bright)">${{col.latin}}</strong></td>
                      <td><span class="hebrew">${{col.hebrew}}</span></td>
                      <td>${{col.gematria}}</td>
                      <td>Cam.${{col.chamber12}}</td>
                    </tr>
                  `).join('')}}
                </tbody>
              </table>
            </div>
          </div>
          ${{DivineNamesUI.panelHTML(n)}}
          ${{LunarUI.panelHTML(n)}}
        </div>

        <!-- Quadrato Magico N×N e Tracciatore SVG del Sigillo -->
        <div class="kamea-wrap">
          <div style="color:var(--gold-bright); font-weight:bold; font-size:0.9rem; text-align:center;">
            Quadrato Magico ${{n}}×${{n}} (${{tData.cells}} Celle · M = ${{tData.M_magic}})
          </div>
          <div class="kamea-stage" style="width:${{n * cellSize + 4}}px; height:${{n * cellSize + 4}}px;">
            <div class="kamea-grid" style="grid-template-columns: repeat(${{n}}, ${{cellSize}}px);">
              ${{gridHtml}}
            </div>
            <svg class="sigil-svg" id="ksvg-${{n}}" viewBox="0 0 ${{n * cellSize}} ${{n * cellSize}}"></svg>
          </div>
          <div id="kstatus-${{n}}" style="text-align:center; padding:6px 10px; background:rgba(255,255,255,0.04); border-radius:6px; width:100%;">
            <span style="color:var(--text-muted); font-size:0.8rem;">Clicca qualsiasi Angelo a sinistra per disegnarne il Sigillo sulla Tavola ${{n}}×${{n}}</span>
          </div>
        </div>
      </div>
    </div>
  `;
}}

function renderEncyclopedia() {{
  renderSynopticTable();
  const container = document.getElementById('heavensContainer');
  const q = (document.getElementById('searchBox').value || '').trim().toLowerCase();

  let spheresList = [...DATA.spheres];
  if (currentMode === 'chamber') {{
    spheresList.sort((a, b) => a.chamber12 - b.chamber12);
  }} else if (currentMode === 'classic') {{
    spheresList = spheresList.filter(s => s.classicOrder !== null);
  }}

  const htmlParts = [];
  spheresList.forEach(s => {{
    const traceOrder = currentMode === 'classic' ? s.classicOrder : s.higherOrder;
    const [shStart, shEnd] = s.shemRange;
    const shemButtons = DATA.shem72.slice(shStart - 1, shEnd).map((x, idx) => {{
      const num = shStart + idx;
      const gem = Array.from(x[1]).reduce((acc, ch) => acc + (HEBREW_VALS[ch] || 0), 0);
      return `<button onclick="traceAngelOnTable(${{traceOrder}}, 'Angelo Quinario #${{num}} Shem HaMephorash', '${{x[0]}}', '${{x[1]}}', ${{gem}})">#${{num}} <strong>${{x[0]}}</strong> (<span class="hebrew">${{x[1]}}</span> = ${{gem}})</button>`;
    }}).join('');

    const mansionButtons = s.mansions.map(m => {{
      const gem = Array.from(m[3]).reduce((acc, ch) => acc + (HEBREW_VALS[ch] || 0), 0);
      return `<button onclick="traceAngelOnTable(${{traceOrder}}, '${{m[0]}}ª Mansione Lunare (${{m[1]}})', '${{m[2]}}', '${{m[3]}}', ${{gem}})">☽ ${{m[0]}}ª ${{m[1]}}: <strong>${{m[2]}}</strong> (<span class="hebrew">${{m[3]}}</span> = ${{gem}})</button>`;
    }}).join('');

    let tablesHtml = '';
    if (currentMode !== 'classic') {{
      tablesHtml += renderSingleTableSection(DATA.tables['table_' + s.higherOrder], s, q);
    }}
    if (s.classicOrder && currentMode !== 'higher') {{
      tablesHtml += renderSingleTableSection(DATA.tables['table_' + s.classicOrder], s, q);
    }}

    if (s.sphereNum === 11 && currentMode !== 'chamber') {{
      htmlParts.push(`<div class="section-card" id="extensionsIntro" style="border-color:var(--orange);">
        <h2 style="color:var(--orange); margin-top:0;">Le due estensioni simboliche del progetto</h2>
        <p style="margin-bottom:0;">Porta di Tav e Sigillo della Verità raccolgono le associazioni delle tavole 20×20 e 21×21.
          Le dieci sfere della scala di Agrippa terminano con il mondo degli elementi, nella scheda precedente.</p>
      </div>`);
    }}

    htmlParts.push(`
      <div class="section-card" id="heaven-card-${{s.sphereNum}}" data-kind="${{s.isExtension ? 'extension' : 'sphere'}}" style="border-color:${{s.color}};">
        <div class="heaven-header">
          <div>
            <div style="color:${{s.color}}; font-size:0.8rem; font-weight:bold; text-transform:uppercase; letter-spacing:1px;">
              ${{sphereLabel(s)}} · FIRMA NUMERICA DELLA TAVOLA ESTESA ${{s.signature12}}
            </div>
            <h2 style="color:var(--gold-bright); margin:4px 0 0; font-size:1.35rem;">
              ${{s.heavenName}}
            </h2>
            <p style="margin:6px 0 0; font-size:0.85rem; color:var(--text-muted);">
              Abbinamento numerico della tavola estesa: Camera ${{s.chamber12}} · <span style="color:var(--cyan)">${{s.sign}}</span>
            </p>
          </div>
          <div style="display:flex; gap:6px; flex-wrap:wrap;">
            ${{s.isExtension ? '<span class="badge" style="border-color:var(--orange); color:var(--orange);">Estensione simbolica del progetto</span>' : ''}}
            <span class="badge" style="border-color:var(--cyan); color:var(--cyan);">Tavola estesa: ${{s.higherOrder}}×${{s.higherOrder}}</span>
            ${{s.classicOrder ? `<span class="badge">Tavola Classica: ${{s.classicOrder}}×${{s.classicOrder}}</span>` : ''}}
            <span class="badge">Mese: ${{s.month}} · Tribù: ${{s.tribe}}</span>
          </div>
        </div>

        <!-- Gerarchia Celestiale del Cielo -->
        <div class="info-box" style="border-color:rgba(0,210,211,0.3);">
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:8px;">
            <div>• <strong>Nome Divino & Bandiera della Camera:</strong> ${{s.divineName}} · YHVH: <span class="hebrew">${{s.permYHVH}}</span></div>
            <div>• <strong>${{s.isExtension ? 'Simbolismo & Coro del progetto' : 'Sephirah & Coro Angelico'}}:</strong> ${{s.sephirah}} · <em>${{s.choir}}</em></div>
            <div>• <strong>Arcangelo & Principe del Segno:</strong> ${{s.archangel}} ·
              <button onclick="traceAngelOnTable(${{traceOrder}}, 'Principe Camera ${{s.chamber12}} (${{s.sign}})', '${{s.signAngel}}', '${{s.signAngelHeb}}', ${{s.signAngelGem}})" style="padding:2px 8px; font-size:0.76rem; border-color:var(--cyan);">
                👼 ${{s.signAngel}} (<span class="hebrew">${{s.signAngelHeb}}</span> = ${{s.signAngelGem}})
              </button>
            </div>
            <div>• <strong>Associazioni numeriche del progetto (${{s.higherOrder}}×${{s.higherOrder}}):</strong>
              <button onclick="traceAngelOnTable(${{traceOrder}}, 'Intelligenza associata alla tavola estesa ${{s.higherOrder}}×${{s.higherOrder}}', '${{s.intName.split('(')[0].trim()}}', '${{s.intHeb}}', ${{s.intGem}})" style="padding:2px 8px; font-size:0.76rem;">
                ✨ <span class="hebrew">${{s.intHeb}}</span> (${{s.intGem}})
              </button>
              <button onclick="traceAngelOnTable(${{traceOrder}}, 'Spirito associato alla tavola estesa ${{s.higherOrder}}×${{s.higherOrder}}', '${{s.spirName.split('(')[0].trim()}}', '${{s.spirHeb}}', ${{s.spirGem}})" style="padding:2px 8px; font-size:0.76rem;">
                🔥 <span class="hebrew">${{s.spirHeb}}</span> (${{s.spirGem}})
              </button>
            </div>
          </div>
          <div style="margin-top:8px; padding-top:8px; border-top:1px solid rgba(255,255,255,0.08); display:flex; flex-wrap:wrap; gap:6px; align-items:center;">
            <strong style="color:var(--cyan);">I 6 Angeli dello Shem HaMephorash (Camera ${{s.chamber12}}):</strong> ${{shemButtons}}
          </div>
          <div style="margin-top:6px; display:flex; flex-wrap:wrap; gap:6px; align-items:center;">
            <strong style="color:var(--gold-bright);">Angeli delle Mansioni Lunari (Camera ${{s.chamber12}}):</strong> ${{mansionButtons}}
          </div>
        </div>

        ${{tablesHtml}}
      </div>
    `);
  }});

  container.innerHTML = htmlParts.join('');

  // Inizializza ogni tavola tracciando la sua Diagonale Solare Discendente
  Object.values(DATA.tables).forEach(t => {{
    const d = t.diagonals.descending;
    traceAngelOnTable(t.order, `Diagonale Solare Discendente (M=${{t.M_magic}})`, d.latin, d.hebrew, d.gematria);
  }});
  LunarUI.refreshPanels();
}}

window.addEventListener('DOMContentLoaded', () => {{
  LunarUI.setTraceHandler(traceAngelOnTable);
  DivineNamesUI.setTraceHandler(traceAngelOnTable);
  setAtlasLunarNow();
  renderEncyclopedia();
}});
</script>
</body>
</html>
"""

    out_html_path = os.path.join(base_dir, 'angels_12_heavens.html')
    html = escape_inline_arguments(html)
    with open(out_html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Creato con successo: {out_html_path} ({len(html)} bytes)")

    # Aggiorna il collegamento in ciascuna pagina senza sovrascrivere l'altra.
    old_label = "👼 Apri l'Enciclopedia HTML Completa di Tutti i 779 Angeli e dei 12 Cieli (angels_12_heavens.html) →"
    new_label = "👼 Apri l'Atlante angelico: 10 sfere e 2 estensioni (angels_12_heavens.html) →"
    for page_name in ('index.html', 'agrippa_calculator.html'):
        page_path = os.path.join(base_dir, page_name)
        with open(page_path, 'r', encoding='utf-8') as f:
            page_text = f.read()
        updated_text = escape_inline_arguments(embed_orthography(page_text, orthography_script, orthography_guide, lunar_script, divine_script, divine_overview)).replace(old_label, new_label)
        if 'angels_12_heavens.html' not in updated_text:
            updated_text = updated_text.replace(
                '</header>',
                '  <div style="margin-top:12px; text-align:center;">\n'
                f'    <a class="btn-link" href="angels_12_heavens.html">{new_label}</a>\n'
                '  </div>\n</header>',
                1
            )
        if updated_text != page_text:
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(updated_text)
    print("Aggiornati i collegamenti in index.html e agrippa_calculator.html.")
    build_complete_catalog(base_dir)

if __name__ == '__main__':
    build_html()
