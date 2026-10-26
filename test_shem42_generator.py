"""Regressioni del generatore del Nome di 42 lettere sulle tavole dell'utente."""
import html
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

from divine_names import shem42_spec
from generate_table_angels import generate_magic_square
from hebrew_orthography import hebrew_gematria,number_to_hebrew,transliterate_hebrew
from shem42_table_names import generate_records,normalize,reduce_to_cell,table_hierarchy
from test_orthography import BASE,EDGE

BROWSER_CHECKS=r'''
<script>
window.addEventListener('DOMContentLoaded',async()=>{
  const report={passed:false};
  const check=(value,message)=>{if(!value) throw new Error(message);};
  const $=id=>document.getElementById(id),change=(id,value)=>{$(id).value=value;$(id).dispatchEvent(new Event('change',{bubbles:true}));};
  try {
    check(typeof Astronomy==='undefined','Generator unexpectedly depends on ephemerides');
    check(Shem42Generator.getRecords().length===133,'Default seven groups on nineteen tables');
    check($('s42Rows').children.length===133,'Initial results not rendered');
    const expected=JSON.parse($('expected-records').textContent);
    const actual=Shem42Generator.completePayload();
    check(JSON.stringify(actual.records)===JSON.stringify(expected),'Python/browser complete corpus differs');
    check(actual.counts.derivations===2736&&actual.counts.distinctSpellings===1004,'Complete corpus counts');
    change('s42Seed','group-1');change('s42Table','3');
    let record=Shem42Generator.getRecords()[0];
    check(record.hebrew==='אבגאדטאל'&&record.gematria===51,'Wrong first-group reading on table 3');
    const button=$('s42Rows').querySelector('button');
    check(button.innerText.trim()===record.hebrew,'Hebrew-only result contains Latin');
    button.click();
    check(!$('s42Details').hidden,'Reading details did not open');
    check($('s42MatrixStage').querySelectorAll('[data-cell]').length===9,'Wrong matrix size');
    const points=$('s42MatrixStage').querySelector('polyline').getAttribute('points').split(' ');
    check(points.length===6,'Wrong number of reading points');
    const point=points[0].split(',').map(Number);
    check(Math.abs(point[0]-50)<1e-8&&Math.abs(point[1]-250/3)<1e-8,'First point not on cell 1');
    const cells=[...$('s42MatrixStage').querySelectorAll('.active')].map(cell=>Number(cell.dataset.cell));
    check([1,2,3,4,9].every(cell=>cells.includes(cell)),'Wrong highlighted cells');
    change('s42Seed','all');change('s42Table','all');change('s42Suffix','both');change('s42Depth','9');
    check(Shem42Generator.getRecords().length===2736,'All-table generation count');
    $('s42Unique').checked=true;$('s42Unique').dispatchEvent(new Event('change',{bubbles:true}));
    check(Shem42Generator.getVisible().length===1004&&$('s42Rows').children.length===1004,'Duplicate spelling filter');
    $('s42Search').value='zzzz_unmatched';$('s42Search').dispatchEvent(new Event('input',{bubbles:true}));
    check(!Shem42Generator.getVisible().length&&$('s42ExportJson').disabled,'Empty search did not disable export');
    $('s42Search').value='';$('s42Search').dispatchEvent(new Event('input',{bubbles:true}));
    const longest=Shem42Generator.getVisible().reduce((a,b)=>a.hebrew.length>b.hebrew.length?a:b);
    const longestButton=document.querySelector(`[data-open-record="${longest.id}"]`);
    const bounds=longestButton.getBoundingClientRect();
    check(bounds.left>=0&&bounds.right<=innerWidth+1,'Long name overflows viewport');
    longestButton.click();
    check(!$('s42Details').hidden,'Long name cannot show reading');
    const exported=Shem42Generator.plainHtml(),doc=new DOMParser().parseFromString(exported,'text/html');
    check(!doc.querySelector('script'),'Static Hebrew export includes scripts');
    check(doc.querySelectorAll('li').length===1004&&!/[A-Za-z]/.test(doc.body.textContent),'Static export is not Hebrew-only');
    const selected=Shem42Generator.selectionPayload();
    check(selected.records.length===2736&&selected.visibleRecordIds.length===1004,'Export lost duplicate paths');
    check(selected.visibleRecordIds.every(id=>selected.records.some(item=>item.id===id)),'Export has unresolved record references');
    let captured=null;
    URL.createObjectURL=blob=>{captured=blob;return 'blob:test';};URL.revokeObjectURL=()=>{};
    HTMLAnchorElement.prototype.click=function(){};
    $('s42ExportHtml').click();
    check((await captured.text())===exported,'HTML download button failed');
    $('s42ExportTxt').click();
    check((await captured.text()).trim().split('\n').length===1004,'TXT download button failed');
    $('s42ExportAll').click();
    check(JSON.parse(await captured.text()).records.length===2736,'Full JSON download failed');
    change('s42Depth','10');
    check(!$('s42Error').hidden&&!Shem42Generator.getRecords().length&&$('s42Details').hidden,'Invalid depth left stale output');
    change('s42Depth','1');
    check($('s42Error').hidden&&Shem42Generator.getRecords().length===304,'Recovery after invalid depth');
    report.derivations=actual.records.length;report.distinctSpellings=1004;report.passed=true;
  }catch(error){report.error=error.stack||String(error);}
  const result=document.createElement('pre');result.id='verification-result';result.textContent=JSON.stringify(report);document.body.append(result);
});
</script>
'''


class Shem42GeneratorTests(unittest.TestCase):
    def test_independent_cell_readings(self):
        for order,hebrew,value in [(3,'אבגאדטאל',51),(4,'אבגידטאל',60),(9,'אבגימטאל',96),
                                   (19,'אבגימצאל',177),(21,'אבגיתצאל',537)]:
            record=table_hierarchy('אבגיתץ',order)[0]
            self.assertEqual((record['hebrew'],record['gematria']),(hebrew,value))
        record=table_hierarchy('אבגיתץ',3)[0]
        self.assertEqual([(step['row'],step['col']) for step in record['steps']],[(2,1),(0,2),(1,0),(2,1),(0,0),(0,1)])
        self.assertEqual(table_hierarchy('אבגיתץ',3,'יה')[0]['gematria'],35)
        full=shem42_spec()['full']['hebrew']
        self.assertEqual(table_hierarchy(full,21)[0]['gematria'],3732)
        self.assertEqual(table_hierarchy(full,21,depth=2)[1]['gematria'],3763)
        for args in [('',9,'אל',1),('abc',9,'אל',1),('אל',2,'אל',1),('אל',22,'אל',1),
                     ('אל',9,'x',1),('אל',9,'אל',0),('אל',9,'אל',10),('אל',True,'אל',1)]:
            with self.assertRaises(ValueError):table_hierarchy(*args)
        for args in [(0,9),(True,9),(1,0),(1,-1)]:
            with self.assertRaises(ValueError):reduce_to_cell(*args)

    def test_complete_corpus_and_table_coordinates(self):
        catalog=json.loads((BASE/'shem42_generated_angels.json').read_text(encoding='utf-8'))
        records=catalog['records']
        self.assertEqual(records,generate_records())
        self.assertEqual(catalog['counts'],{'derivations':2736,'distinctSpellings':1004})
        self.assertEqual(len({record['id'] for record in records}),2736)
        self.assertEqual({record['table_order'] for record in records},set(range(3,22)))
        for record in records:
            matrix=generate_magic_square(record['table_order'])
            self.assertEqual(record['seed'],normalize(record['seed']))
            self.assertEqual(record['gematria'],hebrew_gematria(record['hebrew']))
            self.assertEqual(record['latin'],transliterate_hebrew(record['hebrew']))
            self.assertEqual(record['gematria'],record['root_value']+hebrew_gematria(record['suffix']))
            self.assertEqual(record['root_heb'],''.join(step['numeral'] for step in record['steps']))
            for step in record['steps']:
                self.assertEqual(matrix[step['row']][step['col']],step['cell'])
                self.assertEqual(step['numeral'],number_to_hebrew(step['cell']))
        page=(BASE/'shem42_angel_generator.html').read_text(encoding='utf-8')
        self.assertNotIn('<!-- GENERATOR_ENGINE -->',page)
        self.assertNotRegex(page,r'<script[^>]+src=')
        self.assertNotIn('createPlanetaryNamesEngine',page)
        for name in ('angels_12_heavens.html','index.html','agrippa_calculator.html'):
            self.assertIn('href="shem42_angel_generator.html"',(BASE/name).read_text(encoding='utf-8'))

    @unittest.skipUnless(EDGE.is_file(),'Edge non installato.')
    def test_offline_browser_and_exports(self):
        check_dir=Path(tempfile.mkdtemp(prefix='agrippa_gen42_')).resolve()
        catalog=json.loads((BASE/'shem42_generated_angels.json').read_text(encoding='utf-8'))
        payload='<script type="application/json" id="expected-records">'+json.dumps(catalog['records'],ensure_ascii=False)+'</script>'+BROWSER_CHECKS
        fixture=check_dir/'generator.html'
        fixture.write_text((BASE/'shem42_angel_generator.html').read_text(encoding='utf-8').replace('</body>',payload+'\n</body>'),encoding='utf-8')
        command=[str(EDGE),'--headless=new','--no-sandbox','--in-process-gpu','--disable-gpu',
                 '--disable-software-rasterizer','--disable-extensions','--disable-background-networking',
                 '--no-first-run','--no-default-browser-check','--disable-sync',
                 '--user-data-dir='+str(check_dir/'profile'),'--window-size=390,900',
                 '--virtual-time-budget=5000','--dump-dom',fixture.as_uri()]
        result=subprocess.run(command,capture_output=True,encoding='utf-8',errors='replace',timeout=60,
                              creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        (check_dir/'rendered.html').write_text(result.stdout,encoding='utf-8')
        match=re.search(r'<pre id="verification-result">(.*?)</pre>',result.stdout,re.S)
        self.assertIsNotNone(match,result.stderr[-1500:]+'\nArtifacts: '+str(check_dir))
        report=json.loads(html.unescape(match[1]))
        self.assertTrue(report['passed'],str(report)+'\nArtifacts: '+str(check_dir))
        (BASE/'.verification/generator42-last.json').write_text(json.dumps(report,indent=2),encoding='utf-8')


if __name__=='__main__':unittest.main(verbosity=2)
