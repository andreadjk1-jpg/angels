"""Regressioni delle effemeridi, delle derivazioni III.27 e dei pulsanti offline.

Eseguire: python -X utf8 -m unittest -v test_orthography test_lunar
I riferimenti astronomici sono istanti UTC indipendenti pubblicati da USNO.
"""
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

from hebrew_orthography import hebrew_gematria, transliterate_hebrew
from lunar_names import ALPHABET, MOON_COLUMN, lunar_hierarchy
from test_orthography import BASE, EDGE


# https://aa.usno.navy.mil/api/moon/phases/year?year=2024
# Dati US Naval Observatory (UTC al minuto), consultati il 25 ottobre 2026.
USNO_PHASES = [
    ['2024-01-04T03:30:00Z', 270], ['2024-01-11T11:57:00Z', 0],
    ['2024-03-25T07:00:00Z', 180], ['2024-04-02T03:15:00Z', 270],
    ['2024-04-08T18:21:00Z', 0], ['2024-04-15T19:13:00Z', 90],
    ['2024-07-05T22:57:00Z', 0], ['2024-09-18T02:34:00Z', 180],
]

BROWSER_CHECKS = r'''
<script>
window.addEventListener('DOMContentLoaded', () => {
  const report = {passed:false};
  const check = (condition, message) => {if (!condition) throw new Error(message);};
  const rejects = (fn, message) => {let failed=false; try {fn();} catch (_) {failed=true;} check(failed, message);};
  const close = (a,b,tolerance=1e-8) => Math.abs(a-b)<tolerance;
  const panels = () => [...document.querySelectorAll('[data-lunar-panel]')];
  const names = panel => panel.querySelectorAll('[data-lunar-action="trace"]');
  const click = (panel,action) => panel.querySelector(`[data-lunar-action="${action}"]`).click();
  const change = (input,value) => {input.value=value; input.dispatchEvent(new Event('change',{bubbles:true}));};
  const verifyPanel = panel => check(names(panel).length === 9, 'Missing nine names: ' + panel.dataset.lunarPanel);
  const atlas = typeof DATA !== 'undefined';
  function verifyTrace(panel, hebrew, value) {
    const order=Number(panel.dataset.lunarPanel);
    const sphere=atlas ? null : SPHERES_DATA.find(s=>getActiveTableForSphere(s).order===order);
    const svg=document.getElementById(atlas ? `ksvg-${order}` : `svg-sigil-${sphere.id}`);
    const points=svg.querySelector('polyline').getAttribute('points').trim().split(/\s+/);
    check(points.length===hebrew.length, 'Wrong traced point count: ' + order);
    if (atlas) {
      const status=document.getElementById(`kstatus-${order}`).textContent;
      check(status.includes(hebrew) && status.includes(String(value)), 'Trace status not updated: ' + order);
    } else {
      const active=activeSigilBySphere[sphere.id];
      check(active.hebrew===hebrew && active.expectedGematria===value, 'Wrong active lunar name: ' + order);
    }
  }
  try {
    check(document.querySelectorAll('#lunar-engine').length===1, 'Missing or duplicate lunar engine');
    check(typeof Astronomy.MoonPhase==='function', 'Offline astronomy dependency unavailable');
    for (const [local,time,offset,utc] of [
      ['2024-04-08','20:21',2,'2024-04-08T18:21:00.000Z'],
      ['2024-04-08','11:21',-7,'2024-04-08T18:21:00.000Z'],
      ['2024-04-08','23:51',5.5,'2024-04-08T18:21:00.000Z'],
      ['2024-04-09','08:21',14,'2024-04-08T18:21:00.000Z'],
      ['0001-01-01','00:00',0,'0001-01-01T00:00:00.000Z'],
      ['2000-02-29','00:00',0,'2000-02-29T00:00:00.000Z']]) {
      check(LunarEngine.instant(local,time,offset).toISOString()===utc, 'UTC conversion: ' + local + ' ' + offset);
    }
    for (const args of [['1900-02-29','00:00',0],['1500-02-29','00:00',0],['2024-04-31','00:00',0],
      ['2024-13-01','00:00',0],['2024-01-01','24:00',0],['2024-01-01','12:60',0],['2024-01-01','12:00',15]]) {
      rejects(()=>LunarEngine.instant(...args), 'Invalid date accepted: ' + args.join(' '));
    }
    for (let i=0;i<28;i++) {
      const start=LunarEngine.spec.mansions[i].start;
      check(LunarEngine.mansionAt(start).num===i+1, 'Exact mansion boundary: ' + (i+1));
      check(LunarEngine.mansionAt(start+1e-8).num===i+1, 'After mansion boundary: ' + (i+1));
      check(LunarEngine.mansionAt(start-1e-8).num===(i===0?28:i), 'Before mansion boundary: ' + (i+1));
    }
    check(LunarEngine.mansionAt(360).num===1 && LunarEngine.mansionAt(-360).num===1, '360 degree wrap');
    rejects(()=>LunarEngine.mansionAt(NaN),'NaN longitude accepted');
    const phaseErrors=[];
    for (const [utc,angle] of USNO_PHASES) {
      const state=LunarEngine.stateAt(new Date(utc));
      const error=Math.abs(LunarEngine.norm(state.phaseAngle-angle+180)-180);
      check(error<0.03, 'USNO phase disagreement: ' + utc + ': ' + error);
      check(state.moonLongitude>=0 && state.moonLongitude<360 && Math.abs(state.moonLatitude)<6, 'Moon coordinates out of range');
      check(state.distanceKm>350000 && state.distanceKm<410000 && state.illumination>=0 && state.illumination<=1, 'Physical quantities out of range');
      phaseErrors.push(error);
    }
    report.maxPhaseErrorDegrees=Math.max(...phaseErrors);
    const moment=new Date('2024-04-08T18:21:00Z');
    const tropical=LunarEngine.stateAt(moment), sidereal=LunarEngine.stateAt(moment,{shift:-24});
    check(close(LunarEngine.norm(tropical.moonLongitude-24),sidereal.moonLongitude), 'Sidereal correction not applied');
    check(close(tropical.phaseAngle,sidereal.phaseAngle) && close(tropical.illumination,sidereal.illumination), 'Coordinate choice changed physical phase');
    rejects(()=>LunarEngine.stateAt(moment,{shift:NaN}),'NaN zodiac correction accepted');
    for (const mansion of CATALOG.mansions) {
      check(JSON.stringify(LunarEngine.hierarchy(mansion.hebrew))===JSON.stringify(mansion.generated), 'Python/browser derivation differs: ' + mansion.num);
    }
    const elim=LunarEngine.hierarchy('אלים');
    check(elim[0].hebrew==='זצדגאל' && elim[0].gematria===135, 'Elim derivation');
    check(elim[1].hebrew==='הפושזצאל' && elim[1].gematria===519, 'Full-name iteration or printed Tsadi variant');
    check(LunarEngine.hierarchy('אלים','יה')[0].gematria===119, 'Yah suffix');

    if (atlas) {
      document.getElementById('lunarDate').value='2024-04-08';
      document.getElementById('lunarTime').value='20:21';
      document.getElementById('lunarUtcOffset').value='2';
      document.getElementById('lunarFrame').value='tropical';
      updateAtlasLunar();
      for (const [mode,count] of [['all',19],['higher',12],['classic',7]]) {
        setFilterMode(mode); check(panels().length===count,'Atlas lunar panel count: '+mode); panels().forEach(verifyPanel);
      }
      setFilterMode('all');
    } else {
      document.getElementById('calcDate').value='2024-04-08';
      document.getElementById('calcTime').value='20:21';
      document.getElementById('calcUtcOffset').value='2';
      document.getElementById('calcZodiacClock').value='moon_tropical';
      document.getElementById('calcName').value='Michael';
      runAgrippaCalculator();
      check(activeCalcSphereId==='luna', 'Lunar mode selected another planet');
      for (const [mode,count] of [['desc',12],['kamea',7]]) {
        setSphereOrder(mode); check(panels().length===count,'Calculator lunar panel count: '+mode); panels().forEach(verifyPanel);
      }
      setSphereOrder('desc');
    }
    check(LunarUI.getState().utc==='2024-04-08T18:21:00.000Z','UI selected wrong instant');
    check(document.querySelector('[data-lunar-phase]').textContent.includes('Luna nuova'),'UI phase incorrect');
    for (const panel of panels()) {
      verifyPanel(panel);
      panel.open=true;
      change(panel.querySelector('[data-lunar-mansion-choice]'),'5');
      click(panel,'traditional'); verifyTrace(panel,'גבריאל',246);
      click(panel,'elim'); names(panel)[0].click(); verifyTrace(panel,'זצדגאל',135);
      change(panel.querySelector('[data-lunar-suffix]'),'יה');
      names(panel)[0].click(); verifyTrace(panel,'זצדגיה',119);
    }
    const panel=panels()[0];
    change(panel.querySelector('[data-lunar-seed]'),'Michael');
    check(panel.querySelector('[data-lunar-seed-note]').textContent.includes('מיכאל'), 'Known Latin seed misspelled');
    for (const current of panels()) {
      current.querySelector('[data-lunar-seed]').value='';
      current.querySelector('[data-lunar-mansion-choice]').value='auto';
    }
    document.getElementById(atlas?'lunarDate':'calcDate').value='';
    if (atlas) updateAtlasLunar(); else runAgrippaCalculator();
    check(LunarUI.getState()===null && !document.querySelector('[data-lunar-phase]'),'Invalid date left stale phase');
    check(panels().every(p=>names(p).length===0),'Invalid date left automatic derived names');
    change(panel.querySelector('[data-lunar-mansion-choice]'),'28');
    verifyPanel(panel);
    report.tablesTraced=panels().length;
    report.passed=true;
  } catch (error) {report.error=error.stack || String(error);}
  const result=document.createElement('pre'); result.id='verification-result';
  result.textContent=JSON.stringify(report); document.body.append(result);
});
</script>
'''


class LunarTests(unittest.TestCase):
    def test_historical_column_and_iteration(self):
        self.assertEqual(len(ALPHABET), 22)
        self.assertEqual(len(MOON_COLUMN), 22)
        self.assertTrue(set(MOON_COLUMN) <= set(ALPHABET))
        names = lunar_hierarchy('אלים')
        self.assertEqual((names[0]['root_heb'], names[0]['hebrew'], names[0]['gematria']), ('זצדג', 'זצדגאל', 135))
        self.assertEqual((names[1]['hebrew'], names[1]['gematria']), ('הפושזצאל', 519))
        self.assertEqual(names, lunar_hierarchy('אלימ'))
        self.assertEqual(lunar_hierarchy('אלים', 'יה')[0]['gematria'], 119)
        for seed, suffix, depth in [('', 'אל', 9), ('abc', 'אל', 9), ('אל', 'x', 9),
                                    ('אל', 'אל', 0), ('אל', 'אל', 10), ('אל', 'אל', True)]:
            with self.assertRaises(ValueError):
                lunar_hierarchy(seed, suffix, depth)

    def test_exported_catalog(self):
        catalog = json.loads((BASE / 'lunar_angels_generated.json').read_text(encoding='utf-8'))
        self.assertEqual([m['num'] for m in catalog['mansions']], list(range(1, 29)))
        self.assertEqual(sum(len(m['generated']) for m in catalog['mansions']), 252)
        previous_end = 0
        for mansion in catalog['mansions']:
            self.assertEqual(mansion['start'], previous_end)
            previous_end = mansion['end']
            self.assertEqual(mansion['generated'], lunar_hierarchy(mansion['hebrew']))
            for item in mansion['generated']:
                self.assertEqual(item['gematria'], hebrew_gematria(item['hebrew']))
                self.assertEqual(item['latin'], transliterate_hebrew(item['hebrew']))
        self.assertEqual(previous_end, 360)

    def test_offline_vendor_integrity(self):
        source = (BASE / 'vendor/astronomy.browser.min.js').read_bytes()
        manifest = json.loads((BASE / 'vendor/astronomy-source.json').read_text(encoding='utf-8'))
        self.assertEqual(hashlib.sha256(source).hexdigest(), manifest['sha256'])
        self.assertEqual(len(source), manifest['bytes'])
        self.assertIn(b'MIT License', source[:2500])
        for name in ('angels_12_heavens.html', 'index.html', 'agrippa_calculator.html'):
            page = (BASE / name).read_text(encoding='utf-8')
            self.assertIn(source.decode('utf-8'), page)
            self.assertNotRegex(page, r'<script[^>]+src=["\']https?://')

    @unittest.skipUnless(EDGE.is_file(), 'Edge non installato: eseguire i controlli HTML in un browser.')
    def test_offline_pages_and_usno_phases(self):
        catalog = (BASE / 'lunar_angels_generated.json').read_text(encoding='utf-8')
        payload = '<script>const USNO_PHASES=' + json.dumps(USNO_PHASES) + '; const CATALOG=' + catalog + ';</script>' + BROWSER_CHECKS
        check_dir = Path(tempfile.mkdtemp(prefix='agrippa_luna_')).resolve()
        reports = {}
        for name in ('angels_12_heavens.html', 'index.html', 'agrippa_calculator.html'):
            with self.subTest(page=name):
                fixture = check_dir / name
                fixture.write_text((BASE / name).read_text(encoding='utf-8').replace('</body>', payload + '\n</body>'), encoding='utf-8')
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
                reports[name] = report
                self.assertTrue(report['passed'], str(report) + '\nArtifacts: ' + str(check_dir))
        (BASE / '.verification/lunar-last.json').write_text(json.dumps(reports, indent=2), encoding='utf-8')


if __name__ == '__main__':
    unittest.main(verbosity=2)
