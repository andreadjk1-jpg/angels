# -*- coding: utf-8 -*-
r"""
GENERA I NOMI STRUTTURALI DELLE 19 TAVOLE (3×3 → 9×9 CLASSICHE E 10×10 → 21×21 ESTESE).
Le sette tavole planetarie sono descritte da Agrippa, libro II, cap. 22.
Le tavole estese, i nomi generati e le associazioni mod 12 sono convenzioni del progetto.
"""

import json
import os
from hebrew_orthography import HEBREW_ALPHABET, hebrew_gematria, number_to_hebrew, transliterate_hebrew

HEB_LETTERS = {ch: info['val'] for ch, info in HEBREW_ALPHABET.items()}
C_MAP = {ch: info['roman'] for ch, info in HEBREW_ALPHABET.items()}

CLASSIC_MATRICES = {
    3: [[4, 9, 2], [3, 5, 7], [8, 1, 6]],
    4: [[4, 14, 15, 1], [9, 7, 6, 12], [5, 11, 10, 8], [16, 2, 3, 13]],
    5: [[11, 24, 7, 20, 3], [4, 12, 25, 8, 16], [17, 5, 13, 21, 9], [10, 18, 1, 14, 22], [23, 6, 19, 2, 15]],
    6: [
        [6, 32, 3, 34, 35, 1],
        [7, 11, 27, 28, 8, 30],
        [19, 14, 16, 15, 23, 24],
        [18, 20, 22, 21, 17, 13],
        [25, 29, 10, 9, 26, 12],
        [36, 5, 33, 4, 2, 31]
    ],
    7: [
        [22, 47, 16, 41, 10, 35, 4],
        [5, 23, 48, 17, 42, 11, 29],
        [30, 6, 24, 49, 18, 36, 12],
        [13, 31, 7, 25, 43, 19, 37],
        [38, 14, 32, 1, 26, 44, 20],
        [21, 39, 8, 33, 2, 27, 45],
        [46, 15, 40, 9, 34, 3, 28]
    ],
    8: [
        [8, 58, 59, 5, 4, 62, 63, 1],
        [49, 15, 14, 52, 53, 11, 10, 56],
        [41, 23, 22, 44, 45, 19, 18, 48],
        [32, 34, 35, 29, 28, 38, 39, 25],
        [40, 26, 27, 37, 36, 30, 31, 33],
        [17, 47, 46, 20, 21, 43, 42, 24],
        [9, 55, 54, 12, 13, 51, 50, 16],
        [64, 2, 3, 61, 60, 6, 7, 57]
    ],
    9: [
        [37, 78, 29, 70, 21, 62, 13, 54, 5],
        [6, 38, 79, 30, 71, 22, 63, 14, 46],
        [47, 7, 39, 80, 31, 72, 23, 55, 15],
        [16, 48, 8, 40, 81, 32, 64, 24, 56],
        [57, 17, 49, 9, 41, 73, 33, 65, 25],
        [26, 58, 18, 50, 1, 42, 74, 34, 66],
        [67, 27, 59, 10, 51, 2, 43, 75, 35],
        [36, 68, 19, 60, 11, 52, 3, 44, 76],
        [77, 28, 69, 20, 61, 12, 53, 4, 45]
    ]
}

def gematria(s):
    return hebrew_gematria(s)

def int_to_hebrew(n):
    return number_to_hebrew(n)

def hebrew_to_latin_euphonic(root, suffix='el'):
    # Nome mantenuto per compatibilità con gli import; la trascrizione ora è completa.
    heb_suffix = {'el': 'אל', 'iah': 'יה', 'yah': 'יה'}[suffix]
    return transliterate_hebrew(root + heb_suffix)

def make_angel_from_root(heb_root, suffix='אל', lat_suffix='el'):
    heb_name = f"{heb_root}{suffix}"
    gem = gematria(heb_name)
    lat_name = transliterate_hebrew(heb_name)
    cam12 = ((gem - 1) % 12) + 1
    return {
        'hebrew': heb_name,
        'latin': lat_name,
        'root_heb': heb_root,
        'gematria': gem,
        'chamber12': cam12
    }

def make_angel_from_value(value, suffix='אל', lat_suffix='el'):
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError('La radice numerica di un nome richiede un intero positivo.')
    heb_root = int_to_hebrew(value)
    return make_angel_from_root(heb_root, suffix, lat_suffix)

def make_angel_with_exact_gematria(target_val, suffix='אל', lat_suffix='el'):
    if isinstance(target_val, bool) or not isinstance(target_val, int) or target_val <= 0:
        raise ValueError('Il valore richiesto deve essere un intero positivo.')
    s_val = gematria(suffix)
    if target_val >= s_val:
        rem = target_val - s_val
        heb_root = int_to_hebrew(rem)
    else:
        heb_root = int_to_hebrew(target_val)
    ang = make_angel_from_root(heb_root, suffix, lat_suffix)
    ang['target_val'] = target_val
    ang['target_matches_gematria'] = ang['gematria'] == target_val
    return ang

def generate_odd_magic_square(n):
    grid = [[0]*n for _ in range(n)]
    r, c = 0, n // 2
    for num in range(1, n * n + 1):
        grid[r][c] = num
        nr = (r - 1 + n) % n
        nc = (c + 1) % n
        if grid[nr][nc] != 0:
            r = (r + 1) % n
        else:
            r, c = nr, nc
    return grid

def generate_doubly_even_magic_square(n):
    grid = [[0]*n for _ in range(n)]
    max_plus_one = n * n + 1
    num = 1
    for r in range(n):
        for c in range(n):
            in_diag = (r % 4 == c % 4) or ((r % 4) + (c % 4) == 3)
            grid[r][c] = (max_plus_one - num) if in_diag else num
            num += 1
    return grid

def generate_singly_even_magic_square(n):
    m = n / 2
    m = int(m)
    sub = generate_odd_magic_square(m)
    grid = [[0]*n for _ in range(n)]
    m2 = m * m
    for r in range(m):
        for c in range(m):
            grid[r][c] = sub[r][c]
            grid[r + m][c + m] = sub[r][c] + m2
            grid[r][c + m] = sub[r][c] + 2 * m2
            grid[r + m][c] = sub[r][c] + 3 * m2
    k = (m - 1) // 2
    for r in range(m):
        for c in range(k):
            col = c + 1 if r == k else c
            grid[r][col], grid[r + m][col] = grid[r + m][col], grid[r][col]
    for r in range(m):
        for c in range(n - k + 1, n):
            grid[r][c], grid[r + m][c] = grid[r + m][c], grid[r][c]
    return grid

def generate_magic_square(n):
    if n in CLASSIC_MATRICES:
        return CLASSIC_MATRICES[n]
    if n % 2 == 1:
        return generate_odd_magic_square(n)
    if n % 4 == 0:
        return generate_doubly_even_magic_square(n)
    return generate_singly_even_magic_square(n)

ZODIAC_NAMES = [
    '1. Ariete (♈)', '2. Toro (♉)', '3. Gemelli (♊)', '4. Cancro (♋)',
    '5. Leone (♌)', '6. Vergine (♍)', '7. Bilancia (♎)', '8. Scorpione (♏)',
    '9. Sagittario (♐)', '10. Capricorno (♑)', '11. Acquario (♒)', '12. Pesci (♓)'
]

TABLE_TITLES = {
    3: 'Tabula Saturni Classica 3×3 (Sfera III · Binah)',
    4: 'Tabula Iovis Classica 4×4 (Sfera IV · Chesed)',
    5: 'Tabula Martis Classica 5×5 (Sfera V · Geburah)',
    6: 'Tabula Solis Classica 6×6 (Sfera VI · Tiphereth)',
    7: 'Tabula Veneris Classica 7×7 (Sfera VII · Netzach)',
    8: 'Tabula Mercurii Classica 8×8 (Sfera VIII · Hod)',
    9: 'Tabula Lunae Classica 9×9 (Sfera IX · Yesod)',
    10: 'Tavola estesa 10×10 — Associazione di progetto: Primum Mobile / Kether',
    11: 'Tavola estesa 11×11 — Associazione di progetto: stelle fisse / Chokmah',
    12: 'Tavola estesa 12×12 — Associazione di progetto: Saturno / Binah',
    13: 'Tavola estesa 13×13 — Associazione di progetto: Giove / Chesed',
    14: 'Tavola estesa 14×14 — Associazione di progetto: Marte / Geburah',
    15: 'Tavola estesa 15×15 — Associazione di progetto: Sole / Tiphereth',
    16: 'Tavola estesa 16×16 — Associazione di progetto: Venere / Netzach',
    17: 'Tavola estesa 17×17 — Associazione di progetto: Mercurio / Hod',
    18: 'Tavola estesa 18×18 — Associazione di progetto: Luna / Yesod',
    19: 'Tavola estesa 19×19 — Associazione di progetto: elementi / Malkuth',
    20: 'Estensione I del progetto — Tavola 20×20: Porta di Tav ת=400 & ETH את=401',
    21: 'Estensione II del progetto — Tavola 21×21: Sigillo della Verità EMETH אמת=441'
}

def extract_table_angels(n):
    grid = generate_magic_square(n)
    cells = n * n
    P = cells + 1
    M = (n * (n * n + 1)) // 2
    S = (n * n * (n * n + 1)) // 2

    chamber = ((n - 1) % 12) + 1
    zodiac_sign = ZODIAC_NAMES[chamber - 1]

    data = {
        'order': n,
        'title': TABLE_TITLES.get(n, f'Tavola {n}×{n}'),
        'cells': cells,
        'chamber12': chamber,
        'zodiac_sign': zodiac_sign,
        'P_polar': P,
        'M_magic': M,
        'S_total': S,
        'constants': {},
        'cardinals': {},
        'diagonals': {},
        'center': {},
        'rows': [],
        'columns': [],
        'margins': {}
    }

    # 1. Costanti Aritmetiche Universali
    data['constants']['order'] = {**make_angel_with_exact_gematria(n, 'אל', 'el'), 'role': f"Angelo del Lato N={n}", 'number': n}
    data['constants']['cells'] = {**make_angel_with_exact_gematria(cells, 'אל', 'el'), 'role': f"Angelo del Quadrato N²={cells}", 'number': cells}
    data['constants']['polar'] = {**make_angel_with_exact_gematria(P, 'אל', 'el'), 'role': f"Angelo della Simmetria Polare P={P}", 'number': P}
    data['constants']['magic'] = {**make_angel_with_exact_gematria(M, 'אל', 'el'), 'role': f"Intelligenza Sovrana delle Linee M={M}", 'number': M}
    data['constants']['total'] = {**make_angel_with_exact_gematria(S, 'אל', 'el'), 'role': f"Spirito Supremo Cosmico S={S}", 'number': S}

    # 2. I 4 Cardini (NW, NE, SW, SE) + Corona 4 Angoli
    nw, ne, sw, se = grid[0][0], grid[0][n-1], grid[n-1][0], grid[n-1][n-1]
    data['cardinals']['NW'] = {**make_angel_from_value(nw), 'direction': 'Nord-Ovest (NW)', 'cell': nw, 'coords': [0, 0]}
    data['cardinals']['NE'] = {**make_angel_from_value(ne), 'direction': 'Nord-Est (NE)', 'cell': ne, 'coords': [0, n-1]}
    data['cardinals']['SW'] = {**make_angel_from_value(sw), 'direction': 'Sud-Ovest (SW)', 'cell': sw, 'coords': [n-1, 0]}
    data['cardinals']['SE'] = {**make_angel_from_value(se), 'direction': 'Sud-Est (SE)', 'cell': se, 'coords': [n-1, n-1]}
    data['cardinals']['Ring_4_Corners'] = {
        **make_angel_with_exact_gematria(2 * P),
        'role': f"Corona dei 4 Angoli (Somma = 2P = {2*P})",
        'cells': [nw, ne, sw, se],
        'sum': 2 * P
    }

    # 3. Le 2 Grandi Diagonali
    desc_root = int_to_hebrew(nw) + int_to_hebrew(se)
    asc_root = int_to_hebrew(ne) + int_to_hebrew(sw)
    data['diagonals']['descending'] = {
        **make_angel_from_root(desc_root, 'אל', 'el'),
        'role': f"Diagonale Solare Discendente \\ (M={M})",
        'start_cell': nw, 'end_cell': se, 'sum': M
    }
    data['diagonals']['ascending'] = {
        **make_angel_from_root(asc_root, 'יה', 'iah'),
        'role': f"Diagonale Lunare Ascendente / (M={M})",
        'start_cell': ne, 'end_cell': sw, 'sum': M
    }

    # 4. Centro / Cuore
    if n % 2 == 1:
        c_val = grid[n // 2][n // 2]
        data['center']['type'] = 'single'
        data['center']['angel'] = {
            **make_angel_from_value(c_val),
            'role': f"Asse Centrale (Cella {c_val} = Cor Mundi)",
            'cell': c_val, 'coords': [n // 2, n // 2]
        }
    else:
        m = n // 2
        core_coords = [[m-1, m-1], [m-1, m], [m, m-1], [m, m]]
        core_cells = [grid[r][c] for r, c in core_coords]
        core_sum = sum(core_cells)
        data['center']['type'] = 'quaternary'
        data['center']['angel'] = {
            **make_angel_with_exact_gematria(core_sum),
            'role': f"Nucleo Centrale Tetradico (4 Celle: {core_cells}, Somma = {core_sum})",
            'cells': core_cells, 'sum': core_sum
        }

    # 5. Gli N Angeli delle N Righe
    for r in range(n):
        row = grid[r]
        r_start, r_end = row[0], row[-1]
        r_root = int_to_hebrew(r_start) + int_to_hebrew(r_end)
        ang_row = make_angel_from_root(r_root, 'אל', 'el')
        ang_row.update({'row_num': r + 1, 'start_cell': r_start, 'end_cell': r_end, 'sum': M})
        data['rows'].append(ang_row)

    # 6. Gli N Angeli delle N Colonne
    for c in range(n):
        col = [grid[r][c] for r in range(n)]
        c_top, c_bot = col[0], col[-1]
        c_root = int_to_hebrew(c_top) + int_to_hebrew(c_bot)
        ang_col = make_angel_from_root(c_root, 'אל', 'el')
        ang_col.update({'col_num': c + 1, 'top_cell': c_top, 'bot_cell': c_bot, 'sum': M})
        data['columns'].append(ang_col)

    # 7. I 4 Margini
    top_edge, bot_edge = grid[0], grid[n-1]
    left_edge, right_edge = [grid[r][0] for r in range(n)], [grid[r][n-1] for r in range(n)]
    data['margins']['North'] = {**make_angel_from_value(sum(top_edge) % P or P), 'role': 'Margine Nord', 'sum': sum(top_edge)}
    data['margins']['South'] = {**make_angel_from_value(sum(bot_edge) % P or P), 'role': 'Margine Sud', 'sum': sum(bot_edge)}
    data['margins']['West']  = {**make_angel_from_value(sum(left_edge) % P or P), 'role': 'Margine Ovest', 'sum': sum(left_edge)}
    data['margins']['East']  = {**make_angel_from_value(sum(right_edge) % P or P), 'role': 'Margine Est', 'sum': sum(right_edge)}

    return data

def generate_all():
    results = {}
    md_lines = [
        "# Atlante Completo degli Angeli Strutturali di Tutte le 19 Tavole Magiche (3×3 → 21×21)",
        "",
        "Le **sette tavole planetarie classiche (3×3 → 9×9)** sono descritte da Agrippa (*De Occulta Philosophia*, libro II, cap. 22). Le **dodici tavole estese (10×10 → 21×21)**, i nomi strutturali generati e gli abbinamenti alle camere sono sviluppi numerici del progetto.",
        "",
        "La scala del dieci (libro II, cap. 13) ordina le sfere da Primum Mobile a elementi; la scala del dodici (cap. 14) riguarda i segni zodiacali. Porta di Tav e Sigillo della Verità sono due estensioni simboliche del progetto.",
        "",
        "**Convenzione numerica:** Camera = ((N − 1) mod 12) + 1, con N lato della tavola e Camera 1 associata all'Ariete. I segni riportati sono abbinamenti numerici della tavola.",
        "",
        "**Traslitterazione completa:** ogni consonante è separata da `·`; `ʾ` = Aleph, `ʿ` = Ayin, `ḥ` = Cheth, `ṭ` = Teth, `ṣ` = Tsadi, `š` = Shin. Le vocali dei nomi generati non sono ricostruite. Il parametro numerico e la gematria del nome con suffisso sono indicati separatamente; per valori inferiori al suffisso la gematria esatta non è ottenibile.",
        ""
    ]
    total_angels = 0

    for order in range(3, 22):
        res = extract_table_angels(order)
        results[f"table_{order}"] = res
        count_this = 5 + 5 + 2 + 1 + order + order + 4
        total_angels += count_this

        md_lines.append(f"## {res['title']}")
        md_lines.append(f"- **Parametri**: $N={order}$, $N^2={res['cells']}$, $P={res['P_polar']}$, $M={res['M_magic']}$, $S={res['S_total']}$ · **Camera 12**: Camera {res['chamber12']} ({res['zodiac_sign']}) · **Angeli Strutturali**: {count_this}")
        c = res['cardinals']
        md_lines.append(f"- **4 Cardini & Corona**: NW `{c['NW']['cell']}` **{c['NW']['latin']}** (`{c['NW']['hebrew']}`) · NE `{c['NE']['cell']}` **{c['NE']['latin']}** (`{c['NE']['hebrew']}`) · SW `{c['SW']['cell']}` **{c['SW']['latin']}** (`{c['SW']['hebrew']}`) · SE `{c['SE']['cell']}` **{c['SE']['latin']}** (`{c['SE']['hebrew']}`) · Corona ($2P={c['Ring_4_Corners']['sum']}$): **{c['Ring_4_Corners']['latin']}** (`{c['Ring_4_Corners']['hebrew']}`)")
        d = res['diagonals']
        ctr = res['center']['angel']
        md_lines.append(f"- **2 Diagonali & Cuore**: Solare $\\setminus$ **{d['descending']['latin']}** (`{d['descending']['hebrew']}`) · Lunare $/$ **{d['ascending']['latin']}** (`{d['ascending']['hebrew']}`) · Cuore: **{ctr['latin']}** (`{ctr['hebrew']}`)")
        mrg = res['margins']
        cst = res['constants']
        md_lines.append(f"- **4 Margini**: Nord **{mrg['North']['latin']}** (`{mrg['North']['hebrew']}`) · Sud **{mrg['South']['latin']}** (`{mrg['South']['hebrew']}`) · Ovest **{mrg['West']['latin']}** (`{mrg['West']['hebrew']}`) · Est **{mrg['East']['latin']}** (`{mrg['East']['hebrew']}`)")
        md_lines.append(f"- **5 Costanti**: $N$ **{cst['order']['latin']}** (`{cst['order']['hebrew']}`) · $N^2$ **{cst['cells']['latin']}** (`{cst['cells']['hebrew']}`) · $P$ **{cst['polar']['latin']}** (`{cst['polar']['hebrew']}`) · $M$ **{cst['magic']['latin']}** (`{cst['magic']['hebrew']}`) · $S$ **{cst['total']['latin']}** (`{cst['total']['hebrew']}`)")
        rows_str = " · ".join([f"R{r['row_num']}({r['start_cell']}↔{r['end_cell']}): **{r['latin']}** (`{r['hebrew']}`)" for r in res['rows']])
        cols_str = " · ".join([f"C{col['col_num']}({col['top_cell']}↕{col['bot_cell']}): **{col['latin']}** (`{col['hebrew']}`)" for col in res['columns']])
        md_lines.append(f"- **I {order} Angeli delle Righe**: {rows_str}")
        md_lines.append(f"- **I {order} Pilastri delle Colonne**: {cols_str}")
        md_lines.append("")

    md_lines.append(f"---")
    md_lines.append(f"**TOTALE COMPLESSIVO DEGLI ANGELI STRUTTURALI GENERATI SULLE 19 TAVOLE (3×3 → 21×21): {total_angels} ANGELI**")

    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, 'table_angels_generated.json')
    md_path = os.path.join(base_dir, 'all_tables_angels_atlas.md')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_lines))
    print(f"Generati {total_angels} angeli su 19 tavole (3x3 -> 21x21) in {json_path} e {md_path}")

if __name__ == '__main__':
    generate_all()
