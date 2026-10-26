"""Verifica regressioni di grafie, numerali, nomi e pagine offline.

Eseguire: python -m unittest -v test_orthography
I controlli delle pagine usano Edge se installato; non richiedono rete o pacchetti.
"""
import html
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

import generate_table_angels as generator
from hebrew_orthography import hebrew_gematria, number_to_hebrew, transliterate_hebrew

BASE = Path(__file__).resolve().parent
EDGE = Path(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')


def structural_entries(value):
    if isinstance(value, dict):
        if all(key in value for key in ('latin', 'hebrew', 'gematria')):
            yield value
        for child in value.values():
            yield from structural_entries(child)
    elif isinstance(value, list):
        for child in value:
            yield from structural_entries(child)


BROWSER_CHECKS = r'''
<script>
window.addEventListener('DOMContentLoaded', () => {
  const report = {passed:false};
  const check = (condition, message) => {if (!condition) throw new Error(message);};
  const allHandlers = () => {
    for (const element of document.querySelectorAll('[onclick]')) {
      try { new Function('event', element.getAttribute('onclick')); }
      catch (error) { throw new Error('Invalid button: ' + element.getAttribute('onclick') + ': ' + error.message); }
    }
  };
  try {
    const expectedNames = [['Michael','מיכאל',101],['Mikhael','מיכאל',101],['Metatron','מטטרון',314],['Gabriel','גבריאל',246],['Agiel','אגיאל',45],['Tiriel','טיריאל',260]];
    for (const [name, hebrew, value] of expectedNames) {
      const converted = Orthography.convertName(name);
      check(converted.hebrew === hebrew, name + ': wrong spelling: ' + converted.hebrew + ' (' + converted.kind + ')');
      check(Orthography.gematria(converted.hebrew) === value, name + ': wrong value');
    }
    for (const [input, value] of [['sh',300],['tz',90],['ch',8],['ph',80],['s·h',65],['t·h',405],['ṭ·t',409]]) {
      check(Orthography.gematria(Orthography.convertName(input).hebrew) === value, 'Digraph: ' + input);
    }
    check(Orthography.convertName('Michael (מיכאל)').hebrew === 'מיכאל', 'Duplicated bilingual input');
    check(Orthography.convertName('מִיכָאֵל').hebrew === 'מיכאל', 'Pointed Hebrew input');
    check(Orthography.gematria('ךםןףץ') === 280, 'Ordinary final values');
    check(Orthography.gematria('ךםןףץ', true) === 3500, 'Extended final values');
    check(Orthography.latinGematria('I J U V W [I] [V] [HI] [HV]') === 5409, 'Latin alphabet distinctions');
    check(Orthography.latinGematria('HI') === 17 && Orthography.latinGematria('[HI]') === 800, 'Aspirate token');
    check(Orthography.latinGematria('Jupiter') === 1054, 'Consonantal J');
    for (const [value, expected] of [[0,''],[15,'טו'],[16,'טז'],[415,'תטו'],[416,'תטז'],[441,'תמא'],[900,'תתק']]) {
      check(Orthography.numberToHebrew(value) === expected, 'Numeral ' + value);
    }
    let rejected = false;
    try {Orthography.numberToHebrew(0.5);} catch (_) {rejected=true;}
    check(rejected, 'Fraction accepted as Hebrew numeral');
    check(document.querySelectorAll('#orthography-guide').length === 1, 'Missing or repeated guide');
    check(document.querySelectorAll('#orthography-engine').length === 1, 'Repeated shared engine');

    if (typeof DATA !== 'undefined') {
      let entries = 0;
      function walk(value) {
        if (!value || typeof value !== 'object') return;
        if ('latin' in value && 'hebrew' in value && 'gematria' in value) {
          check(value.latin === Orthography.transliterateHebrew(value.hebrew), 'Incomplete stored transliteration');
          check(Orthography.convertName(value.latin).hebrew === value.hebrew, 'Transliteration does not round trip');
          check(Orthography.gematria(value.hebrew) === value.gematria, 'Stored gematria mismatch');
          entries++;
        }
        for (const child of Object.values(value)) walk(child);
      }
      walk(DATA.tables);
      check(entries === 779, 'Wrong structural count');
      for (const [mode, tables] of [['all',19],['higher',12],['classic',7],['chamber',19]]) {
        setFilterMode(mode);
        check(document.querySelectorAll('.kamea-stage').length === tables, 'Table filter: ' + mode);
        check(document.querySelectorAll('.sigil-svg polyline').length === tables, 'Sigils: ' + mode);
        check(document.querySelectorAll('button[onclick*="Angelo Totale S="]').length === tables, 'Missing total constant: ' + mode);
        allHandlers();
      }
      setFilterMode('all');
      const total21 = [...document.querySelectorAll('button[onclick*="Angelo Totale S="]')].find(button=>button.getAttribute('onclick').startsWith('traceAngelOnTable(21,'));
      total21.click();
      check(document.getElementById('kstatus-21').textContent.includes('97461'), 'Longest name does not trace');
      const bounds=total21.getBoundingClientRect();
      check(bounds.right<=innerWidth+1 && bounds.left>=0, 'Longest name overflows the viewport');
      const search = document.getElementById('searchBox');
      search.value = 'zzzz_unmatched';
      search.dispatchEvent(new Event('input', {bubbles:true}));
      check(document.querySelectorAll('.two-col-tables tbody tr').length === 0, 'Search filter');
      search.value=''; search.dispatchEvent(new Event('input', {bubbles:true}));
      check(document.querySelectorAll('.two-col-tables tbody tr').length === 456, 'Search reset');
      report.structuralEntries = entries;
    } else {
      check(document.querySelectorAll('#cosmicDiagramSvg circle').length === 10, 'Cosmological diagram includes extensions');
      const wrongValues = SPHERES_DATA.flatMap(s => (s.entities || []).filter(e => e.expectedGematria && e.expectedGematria !== Orthography.gematria(e.hebrew)).map(e => e.name));
      check(!wrongValues.length, 'Incorrect entity values: ' + wrongValues.join(', '));
      for (const sphere of SPHERES_DATA) {
        for (const field of ['intelligence','spirit']) {
          if (sphere[field + 'Hebrew']) check(Orthography.gematria(sphere[field + 'Hebrew']) === sphere[field + 'Val'], 'Incorrect full-name value: ' + sphere.id);
        }
      }
      check(SPHERES_DATA.find(s=>s.id==='luna').intelligenceTableNumber===3321, 'Lunar table number changed');
      const input = document.getElementById('calcName');
      const override = document.getElementById('calcHebrewOverride');
      for (const [name, hebrew, value] of expectedNames) {
        input.value=name; override.value=''; runAgrippaCalculator();
        check(currentCalcTraces.some(e=>e.hebrew===hebrew && e.name.includes(name)), 'Calculator name trace: ' + name);
        check(document.getElementById('calculatorOutput').textContent.includes('= ' + value), 'Calculator explanation: ' + name);
      }
      input.value='Jupiter'; override.value='מיכאל'; runAgrippaCalculator();
      check(currentCalcTraces.some(e=>e.hebrew==='מיכאל' && e.name.includes('Jupiter')), 'Hebrew spelling override');
      check(document.getElementById('calculatorOutput').textContent.includes('J(600)'), 'Latin breakdown');
      input.value='[HI]'; runAgrippaCalculator();
      check(document.getElementById('calculatorOutput').textContent.includes('[HI](800)'), 'Latin special-token breakdown');
      override.value=''; input.value='Michael'; runAgrippaCalculator();
      const custom=document.getElementById('custom-input-kether');
      custom.value='Metatron'; traceCustomName('kether');
      check(activeSigilBySphere.kether.hebrew==='מטטרון', 'Custom-name sigil');
      check(Orthography.gematria(activeSigilBySphere.kether.hebrew)===314, 'Custom-name value');
      for (const s of SPHERES_DATA) {
        const record=extractTableStructuralAngelsJS(s.higherMatrix);
        for (const row of record.rows) {
          check(row.name.startsWith(Orthography.transliterateHebrew(row.heb)), 'Truncated dynamic structural name');
        }
      }
      const totalButton=[...document.querySelectorAll('button')].find(button=>button.textContent.includes('Totale S=97461'));
      check(totalButton, 'Missing longest structural name');
      totalButton.click();
      const totalBounds=totalButton.getBoundingClientRect();
      check(totalBounds.left>=0 && totalBounds.right<=innerWidth+1, 'Calculator longest name overflows after tracing');
      for (const mode of ['desc','asc','kamea','higher','sum','reduction']) {setSphereOrder(mode); allHandlers();}
      setSphereOrder('desc');
      allHandlers();
      report.calculator='passed';
    }
    report.passed=true;
  } catch (error) {report.error=error.stack || String(error);}
  const result=document.createElement('pre'); result.id='verification-result';
  result.textContent=JSON.stringify(report); document.body.append(result);
});
</script>
'''


class OrthographyTests(unittest.TestCase):
    def test_known_hebrew_values_and_finals(self):
        for name, value in [('מיכאל', 101), ('מטטרון', 314), ('גבריאל', 246), ('ךםןףץ', 280)]:
            self.assertEqual(hebrew_gematria(name), value)
        self.assertEqual(hebrew_gematria('ךםןףץ', extended_finals=True), 3500)

    def test_numeral_spelling(self):
        for n, expected in [(0, ''), (15, 'טו'), (16, 'טז'), (415, 'תטו'), (416, 'תטז'), (441, 'תמא'), (900, 'תתק')]:
            self.assertEqual(number_to_hebrew(n), expected)
        for n in range(1001):
            self.assertEqual(hebrew_gematria(number_to_hebrew(n)), n)
        for n in (-1, 0.5, True):
            with self.assertRaises(ValueError):
                number_to_hebrew(n)

    def test_zero_is_not_an_angel_root(self):
        for fn in (generator.make_angel_from_value, generator.make_angel_with_exact_gematria):
            with self.assertRaises(ValueError):
                fn(0)
        el = generator.make_angel_with_exact_gematria(31)
        self.assertEqual(el['hebrew'], 'אל')
        self.assertTrue(el['target_matches_gematria'])
        self.assertFalse(generator.make_angel_with_exact_gematria(3)['target_matches_gematria'])

    def test_complete_generated_names_and_magic_squares(self):
        tables = json.loads((BASE / 'table_angels_generated.json').read_text(encoding='utf-8'))
        entries = list(structural_entries(tables))
        self.assertEqual(len(entries), 779)
        labels = {}
        for item in entries:
            self.assertEqual(item['latin'], transliterate_hebrew(item['hebrew']))
            self.assertEqual(len(item['latin'].split('·')), len(item['hebrew']))
            self.assertEqual(item['gematria'], hebrew_gematria(item['hebrew']))
            self.assertEqual(labels.setdefault(item['latin'], item['hebrew']), item['hebrew'])
        for n in range(3, 22):
            grid = generator.generate_magic_square(n)
            total = n * (n * n + 1) // 2
            self.assertEqual(sorted(v for row in grid for v in row), list(range(1, n * n + 1)))
            self.assertTrue(all(sum(row) == total for row in grid))
            self.assertTrue(all(sum(grid[r][c] for r in range(n)) == total for c in range(n)))
            self.assertEqual(sum(grid[i][i] for i in range(n)), total)
            self.assertEqual(sum(grid[i][n - 1 - i] for i in range(n)), total)

    @unittest.skipUnless(EDGE.is_file(), 'Edge non installato: eseguire i controlli HTML in un browser.')
    def test_offline_pages_in_edge(self):
        check_dir = Path(tempfile.mkdtemp(prefix='agrippa_lettere_')).resolve()
        for name in ('angels_12_heavens.html', 'index.html', 'agrippa_calculator.html'):
            with self.subTest(page=name):
                source = (BASE / name).read_text(encoding='utf-8')
                fixture = check_dir / name
                fixture.write_text(source.replace('</body>', BROWSER_CHECKS + '\n</body>'), encoding='utf-8')
                command = [str(EDGE), '--headless=new', '--no-sandbox', '--in-process-gpu', '--disable-gpu',
                           '--disable-software-rasterizer', '--disable-extensions', '--disable-background-networking',
                           '--no-first-run', '--no-default-browser-check', '--disable-sync',
                           '--user-data-dir=' + str(check_dir / (name + '-profile')),
                           '--virtual-time-budget=4000', '--dump-dom', fixture.as_uri()]
                result = subprocess.run(command, capture_output=True, encoding='utf-8', errors='replace',
                                        timeout=45, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
                (check_dir / (name + '-rendered.html')).write_text(result.stdout, encoding='utf-8')
                match = re.search(r'<pre id="verification-result">(.*?)</pre>', result.stdout, re.S)
                self.assertIsNotNone(match, result.stderr[-1500:] + '\nArtifacts: ' + str(check_dir))
                report = json.loads(html.unescape(match[1]))
                self.assertTrue(report['passed'], str(report) + '\nArtifacts: ' + str(check_dir))


if __name__ == '__main__':
    unittest.main(verbosity=2)
