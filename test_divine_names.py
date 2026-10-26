"""Nome di 42 lettere: acrostico, grafie, gematria e collegamenti alle tavole."""
import html
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

from divine_names import shem42_spec
from hebrew_orthography import hebrew_gematria, transliterate_hebrew
from lunar_names import lunar_hierarchy
from test_orthography import BASE, EDGE

BROWSER_CHECKS = r'''
<script>
window.addEventListener('DOMContentLoaded', () => {
  const report={passed:false};
  const check=(condition,message)=>{if(!condition) throw new Error(message);};
  const atlas=typeof DATA!=='undefined';
  const panels=()=>[...document.querySelectorAll('[data-divine42-panel]')];
  const entries=[EXPECTED.full,...EXPECTED.groups];
  const letters=text=>[...text].filter(ch=>Orthography.letters[ch]);
  function verifyTrace(panel,item) {
    const order=Number(panel.dataset.divine42Panel);
    const sphere=atlas?null:SPHERES_DATA.find(s=>getActiveTableForSphere(s).order===order);
    const svg=document.getElementById(atlas?`ksvg-${order}`:`svg-sigil-${sphere.id}`);
    const points=svg.querySelector('polyline').getAttribute('points').trim().split(/\s+/);
    check(points.length===item.letters,'Wrong number of traced letters: '+order+' '+item.id);
    if(atlas) {
      const status=document.getElementById(`kstatus-${order}`).textContent;
      check(status.includes(item.hebrew) && status.includes(String(item.gematria)), 'Wrong trace status: '+order+' '+item.id);
    } else {
      const active=activeSigilBySphere[sphere.id];
      check(active.hebrew===item.hebrew && active.expectedGematria===item.gematria,'Wrong selected name: '+order+' '+item.id);
    }
  }
  try {
    check(document.querySelectorAll('#divine-names-engine').length===1,'Missing or duplicate divine engine');
    check(document.querySelectorAll('#divineNames42').length===1,'Missing or duplicate overview');
    check(letters(document.querySelector('[data-divine42-full]').textContent).length===42,'Visible full name length');
    check(document.querySelector('[data-divine42-total]').textContent==='3701','Visible total gematria');
    check(document.querySelectorAll('#divineNames42 tbody tr').length===7,'Visible seven groups');
    for(const item of entries) {
      check(letters(item.hebrew).length===item.letters,'Stored letter count: '+item.id);
      check(Orthography.gematria(item.hebrew)===item.gematria,'Browser gematria: '+item.id);
      check(Orthography.transliterateHebrew(item.hebrew)===item.latin,'Browser transliteration: '+item.id);
    }
    for(const alias of ['Shem 42','Shem Mem Bet','Nome di 42 lettere']) {
      const converted=Orthography.convertName(alias);
      check(converted.kind==='known' && converted.hebrew===letters(EXPECTED.full.hebrew).join(''),'Unrecognized full-name alias: '+alias);
    }
    const modes=atlas?[['all',19],['higher',12],['classic',7]]:[['desc',12],['kamea',7]];
    let traced=0;
    for(const [mode,count] of modes) {
      if(atlas) setFilterMode(mode); else setSphereOrder(mode);
      check(panels().length===count,'Missing table panels: '+mode);
      for(const panel of panels()) {
        panel.open=true;
        check(panel.querySelectorAll('[data-divine42-action="trace"]').length===8,'Missing name/group controls');
        for(const item of entries) {
          panel.querySelector(`[data-divine42-action="trace"][data-divine42-id="${item.id}"]`).click();
          verifyTrace(panel,item); traced++;
        }
      }
    }
    const panel=panels()[0];
    const order=panel.dataset.divine42Panel;
    for(const item of entries) {
      panel.querySelector(`[data-divine42-action="lunar-seed"][data-divine42-id="${item.id}"]`).click();
      const lunarPanel=document.querySelector(`[data-lunar-panel="${order}"]`);
      check(lunarPanel.open && lunarPanel.querySelector('[data-lunar-seed]').value===item.hebrew,'Wrong lunar seed selected: '+item.id);
      const names=lunarPanel.querySelectorAll('[data-lunar-action="trace"]');
      check(names.length===9,'Lunar generation failed: '+item.id);
      const expected=LUNAR_FIRST[item.id];
      check(names[0].textContent.includes(expected.hebrew) && names[0].textContent.includes(String(expected.gematria)), 'Wrong first lunar derivation: '+item.id);
    }
    LunarUI.showError('Istante non selezionato');
    panel.querySelector('[data-divine42-action="trace"][data-divine42-id="full"]').click();
    verifyTrace(panel,EXPECTED.full);
    if(!atlas) {
      document.getElementById('calcName').value='Shem 42';
      document.getElementById('calcHebrewOverride').value='';
      runAgrippaCalculator();
      check(document.getElementById('calculatorOutput').textContent.includes('3701'),'Full name unavailable in calculator');
    }
    report.traced=traced;
    report.passed=true;
  } catch(error) {report.error=error.stack||String(error);}
  const result=document.createElement('pre'); result.id='verification-result';
  result.textContent=JSON.stringify(report); document.body.append(result);
});
</script>
'''


class DivineNamesTests(unittest.TestCase):
    def test_seven_groups_and_ordinary_gematria(self):
        spec=shem42_spec()
        expected=[('אבגיתץ',506),('קרעשטן',729),('נגדיכש',387),('בטרצתג',704),
                  ('חקבטנע',239),('יגלפזק',230),('שקוצית',906)]
        self.assertEqual([(item['hebrew'],item['gematria']) for item in spec['groups']],expected)
        self.assertEqual(spec['full']['letters'],42)
        self.assertEqual(spec['full']['gematria'],3701)
        self.assertEqual(spec['full']['hebrew'],' '.join(hebrew for hebrew,_ in expected))
        for item in [spec['full'],*spec['groups']]:
            self.assertEqual(item['gematria'],hebrew_gematria(item['hebrew']))
            self.assertEqual(item['latin'],transliterate_hebrew(item['hebrew']))
        self.assertEqual(json.loads((BASE/'shem42_divine_names.json').read_text(encoding='utf-8')),spec)
        self.assertIn('3701',(BASE/'shem42_letter_name.md').read_text(encoding='utf-8'))

    @unittest.skipUnless(EDGE.is_file(),'Edge non installato: eseguire i controlli HTML in un browser.')
    def test_offline_tracing_and_lunar_seed_buttons(self):
        spec=shem42_spec()
        lunar={item['id']:lunar_hierarchy(item['hebrew'])[0] for item in [spec['full'],*spec['groups']]}
        payload='<script>const EXPECTED='+json.dumps(spec,ensure_ascii=False)+'; const LUNAR_FIRST='+json.dumps(lunar,ensure_ascii=False)+';</script>'+BROWSER_CHECKS
        check_dir=Path(tempfile.mkdtemp(prefix='agrippa_nome42_')).resolve()
        reports={}
        for name in ('angels_12_heavens.html','index.html','agrippa_calculator.html'):
            with self.subTest(page=name):
                fixture=check_dir/name
                fixture.write_text((BASE/name).read_text(encoding='utf-8').replace('</body>',payload+'\n</body>'),encoding='utf-8')
                command=[str(EDGE),'--headless=new','--no-sandbox','--in-process-gpu','--disable-gpu',
                         '--disable-software-rasterizer','--disable-extensions','--disable-background-networking',
                         '--no-first-run','--no-default-browser-check','--disable-sync',
                         '--user-data-dir='+str(check_dir/(name+'-profile')),
                         '--virtual-time-budget=4000','--dump-dom',fixture.as_uri()]
                result=subprocess.run(command,capture_output=True,encoding='utf-8',errors='replace',
                                      timeout=45,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
                (check_dir/(name+'-rendered.html')).write_text(result.stdout,encoding='utf-8')
                match=re.search(r'<pre id="verification-result">(.*?)</pre>',result.stdout,re.S)
                self.assertIsNotNone(match,result.stderr[-1500:]+'\nArtifacts: '+str(check_dir))
                report=json.loads(html.unescape(match[1])); reports[name]=report
                self.assertTrue(report['passed'],str(report)+'\nArtifacts: '+str(check_dir))
        (BASE/'.verification/divine42-last.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')


if __name__=='__main__':
    unittest.main(verbosity=2)
