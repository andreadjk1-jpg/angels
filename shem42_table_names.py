"""Nome di 42 lettere: lettura numerica delle diciannove tavole del progetto.

La riduzione riprende reduceToCell dell'atlante. La lettura dei numerali e
l'aggiunta del suffisso sono una convenzione del progetto, distinta dalla
sostituzione della tavola planetaria di Agrippa III.27.
"""
from divine_names import shem42_spec
from generate_table_angels import generate_magic_square
from hebrew_orthography import HEBREW_ALPHABET, hebrew_gematria, number_to_hebrew, transliterate_hebrew

FINAL_TO_NORMAL = str.maketrans('ךםןףץ', 'כמנפצ')
RULE = ('Lettera ebraica → valore ordinario → cella della tavola, riducendo per decine '
        'finché il valore rientra in N² → numerale ebraico della cella. '
        'Si concatenano i numerali in ordine e si aggiunge אל oppure יה.')
ITERATION = 'Ogni grado successivo ripete la stessa lettura sul nome completo precedente, suffisso incluso.'


def table_spec():
    return {'tables': [{'order': n, 'cells': n*n, 'matrix': generate_magic_square(n)} for n in range(3,22)],
            'rule': RULE, 'iterationRule': ITERATION,
            'methodStatus': 'Lettura numerica delle celle: convenzione del progetto applicata alle sue diciannove tavole.',
            'sources': ['https://www.esotericarchives.com/agrippa/agripp2b.htm#chap22',
                        'https://www.esotericarchives.com/agrippa/agripp3c.htm#chap30'],
            'scopeNote': 'Le sette kamee 3×3–9×9 sono classiche; le tavole 10×10–21×21 sono estensioni del progetto.'}


def normalize(seed):
    return ''.join(ch for ch in str(seed).translate(FINAL_TO_NORMAL) if ch in HEBREW_ALPHABET)


def reduce_to_cell(value, max_cell):
    if isinstance(value,bool) or not isinstance(value,int) or value < 1:
        raise ValueError('Il valore della lettera deve essere un intero positivo.')
    if isinstance(max_cell,bool) or not isinstance(max_cell,int) or max_cell < 1:
        raise ValueError('La capacità della tavola deve essere un intero positivo.')
    while value > max_cell:
        if value % 10 == 0:
            value //= 10
        else:
            root = value // 10
            value = root if 0 < root <= max_cell else (value-1) % max_cell+1
    return value


def table_hierarchy(seed, order=9, suffix='אל', depth=1):
    if isinstance(order,bool) or not isinstance(order,int) or not 3 <= order <= 21:
        raise ValueError('Scegliere una tavola da 3×3 a 21×21.')
    if suffix not in ('אל','יה'):
        raise ValueError('Scegliere il suffisso אל oppure יה.')
    if isinstance(depth,bool) or not isinstance(depth,int) or not 1 <= depth <= 9:
        raise ValueError('Scegliere da uno a nove gradi.')
    current = normalize(seed)
    if not current:
        raise ValueError('Il nome di partenza deve contenere lettere ebraiche.')
    matrix = generate_magic_square(order)
    coords = {cell:(r,c) for r,row in enumerate(matrix) for c,cell in enumerate(row)}
    records = []
    for level in range(1,depth+1):
        steps = []
        for ch in current:
            value = HEBREW_ALPHABET[ch]['val']
            cell = reduce_to_cell(value,order*order)
            row,col = coords[cell]
            steps.append({'letter':ch,'value':value,'cell':cell,'row':row,'col':col,'numeral':number_to_hebrew(cell)})
        root = ''.join(step['numeral'] for step in steps)
        hebrew = root+suffix
        records.append({'level':level,'seed':current,'root_heb':root,'hebrew':hebrew,
                        'latin':transliterate_hebrew(hebrew),'gematria':hebrew_gematria(hebrew),
                        'root_value':sum(step['cell'] for step in steps),'steps':steps})
        current = hebrew
    return records


def generate_records(seeds=None, orders=None, suffixes=('אל','יה'), depth=9):
    divine = shem42_spec()
    seeds = [divine['full'],*divine['groups']] if seeds is None else seeds
    orders = list(range(3,22)) if orders is None else orders
    result = []
    for seed in seeds:
        for order in orders:
            for suffix in suffixes:
                suffix_id = 'el' if suffix == 'אל' else 'yah'
                for name in table_hierarchy(seed['hebrew'],order,suffix,depth):
                    result.append({'id':f's42-{seed["id"]}-table-{order}-{suffix_id}-{name["level"]}',
                                   'seed_id':seed['id'],'seed_label':seed['label'],'source_hebrew':seed['hebrew'],
                                   'table_order':order,'suffix':suffix,**name})
    return result
