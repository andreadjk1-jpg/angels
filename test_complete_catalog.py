"""Copertura delle sorgenti, gruppi per sfera e catalogo statico senza disegni."""
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest
import copy

from build_complete_catalog import collect_catalog,js_literal,name_key
from hebrew_orthography import hebrew_gematria
from sphere_zodiac import audit_spheres
from test_orthography import BASE,EDGE,structural_entries


class TextCollector(HTMLParser):
    def __init__(self):super().__init__();self.text=[];self.skip=0;self.entries=[];self.ids=[];self.links=[];self.sections=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag=='a' and attrs.get('href','').startswith('#'):self.links.append(attrs['href'][1:])
        if tag=='section':self.sections.append(attrs.get('id'))
        if tag=='article' and attrs.get('class')=='entry':self.entries.append((attrs,self.sections[-1]))
        if tag in ('style','script'):self.skip+=1
    def handle_endtag(self,tag):
        if tag=='section':self.sections.pop()
        if tag in ('style','script'):self.skip-=1
    def handle_data(self,data):
        if not self.skip:self.text.append(data)


class CompleteCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads((BASE/'complete_angel_catalog.json').read_text(encoding='utf-8'))
        cls.page=(BASE/'complete_angel_catalog.html').read_text(encoding='utf-8')
        cls.by_key={entry['key']:entry for entry in cls.manifest['entries']}

    def test_js_literal_reader(self):
        value=js_literal(r'''const SAMPLE=[{name:'Da\'ath: // testo', Hebrew:'דעת',yes:true, no:false, empty:null, numbers:[1,2,],}, /* commento */]; alert('ignored');''','SAMPLE')
        self.assertEqual(value,[{'name':"Da'ath: // testo",'Hebrew':'דעת','yes':True,'no':False,'empty':None,'numbers':[1,2]}])
        with self.assertRaises(ValueError):js_literal('const SAMPLE=[execute()];','SAMPLE')

    def test_all_catalog_sources_and_identity(self):
        self.assertEqual(self.manifest,collect_catalog())
        self.assertEqual(len(self.by_key),2105)
        for filename,digest in self.manifest['sources'].items():
            self.assertEqual(hashlib.sha256((BASE/filename).read_bytes()).hexdigest(),digest)
        for filename in ('table_angels_generated.json','lunar_angels_generated.json','shem42_generated_angels.json'):
            data=json.loads((BASE/filename).read_text(encoding='utf-8'))
            for entry in structural_entries(data):self.assertIn(name_key(entry['hebrew']),self.by_key)
        ids=set()
        for entry in self.manifest['entries']:
            self.assertNotIn(entry['id'],ids);ids.add(entry['id'])
            self.assertEqual(entry['gematria'],hebrew_gematria(entry['hebrew']))
            self.assertEqual(entry['key'],name_key(entry['hebrew']))
            self.assertTrue(all(name_key(spelling)==entry['key'] for spelling in entry['spellings']))
            self.assertTrue(entry['occurrences']);self.assertTrue(entry['tableOrders'])
        for hebrew in ('מיכאל','מטטרון','גבריאל','דעת','ארך','אבגיתץ','קרעשטן'):
            self.assertIn(hebrew,self.by_key)
        self.assertNotEqual(self.by_key['מיכאל']['id'],self.by_key['מטטרון']['id'])
        self.assertEqual(self.manifest['counts']['families']['structural'],779)
        self.assertEqual(self.manifest['counts']['families']['lunar'],252)
        self.assertEqual(self.manifest['counts']['families']['shem42'],2736)
        self.assertEqual(self.manifest['counts']['families']['shem72'],72)

    def test_sphere_grouping_and_text_only_document(self):
        self.assertNotRegex(self.page,r'<(?:script|iframe|img|svg|canvas|object|embed)\b')
        self.assertNotRegex(self.page,r'<link[^>]+href=')
        self.assertNotRegex(self.page,r'\bon[a-z]+\s*=')
        parser=TextCollector();parser.feed(self.page)
        self.assertNotRegex(''.join(parser.text),r'[A-Za-z]')
        self.assertIn('<html lang="he" dir="rtl">',self.page)
        self.assertEqual(len(parser.entries),4002)
        self.assertEqual(len(parser.ids),len(set(parser.ids)))
        self.assertTrue(set(parser.links)<=set(parser.ids))
        actual=set()
        for attrs,section in parser.entries:
            self.assertEqual(attrs['data-group'],section)
            pair=(attrs['data-name'],section)
            self.assertNotIn(pair,actual);actual.add(pair)
        expected={(entry['key'],group_id) for entry in self.manifest['entries'] for group_id in entry['groupIds']}
        self.assertEqual(actual,expected)
        self.assertEqual({key for key,_ in actual},set(self.by_key))
        groups=self.manifest['sphereGroups']
        self.assertEqual(len(groups),12)
        self.assertEqual(sum(group['kind']=='sphere' for group in groups),10)
        self.assertEqual(sum(group['kind']=='extension' for group in groups),2)
        self.assertEqual(sum(group['nameCount'] for group in groups),4002)
        for entry in self.manifest['entries']:
            expected_groups={group['id'] for group in groups if set(group['tableOrders'])&set(entry['tableOrders'])}
            self.assertEqual(set(entry['groupIds']),expected_groups)

    def test_zodiac_audit_and_rejected_wrong_mappings(self):
        metadata=js_literal((BASE/'index.html').read_text(encoding='utf-8'),'ORTHOGRAPHY_SPHERES')
        audit=audit_spheres(metadata)
        self.assertEqual(json.loads((BASE/'verify_spheres_zodiac.json').read_text(encoding='utf-8')),self.manifest['zodiacAudit'])
        self.assertTrue(audit['traditionalTableAssignmentVerified'])
        self.assertTrue(audit['projectChamberFormulaVerified'])
        self.assertFalse(audit['fixedSphereToAstronomicalSignCorrespondence'])
        self.assertFalse(audit['planetaryPositionsComputed'])
        self.assertEqual(audit['groups'][1]['astronomicalStatus'],'whole-zodiac')
        self.assertEqual(sum(group['astronomicalStatus']=='moving-body' for group in audit['groups']),7)
        self.assertTrue(all(group['fixedAstronomicalSign'] is None for group in audit['groups']))
        self.assertEqual(len(audit['solarEclipticConstellations']),13)
        self.assertIn('Ophiuchus',audit['solarEclipticConstellations'])
        self.assertEqual({order for group in audit['groups'] for order in group['tableOrders']},set(range(3,22)))
        for index,field,value in [(2,'classicOrder',4),(8,'chamber12',9),(11,'isExtension',False),(0,'sign','10. Leone')]:
            wrong=copy.deepcopy(metadata);wrong[index][field]=value
            with self.assertRaises(ValueError):audit_spheres(wrong)

    @unittest.skipUnless(EDGE.is_file(),'Edge non installato.')
    def test_actual_archive_and_catalog_in_browser(self):
        folder=Path(tempfile.mkdtemp(prefix='agrippa_catalogo_')).resolve()
        report_path=BASE/'.verification/catalogue-last.json'
        archive_script=r'''<script>window.addEventListener('DOMContentLoaded',()=>{
          const report={passed:false};
          try {
            const names=[];
            for(const sphere of SPHERES_DATA) {
              for(const field of ['divineHebrew','archangelHebrew','intelligenceHebrew','spiritHebrew']) if(sphere[field]) names.push(sphere[field]);
              for(const entity of sphere.entities||[]) names.push(entity.hebrew);
              for(const [field,value] of Object.entries(sphere.latinInfo||{})) if(field.endsWith('Heb')) names.push(value);
            }
            names.push(...SHEM_72_ANGELS.map(item=>Array.isArray(item)?item[1]:item.hebrew),...MANSIONS_28_LUNA.map(item=>item.heb));
            const missing=names.filter(name=>!EXPECTED_KEYS.includes([...name].filter(ch=>Orthography.letters[ch]).join('')));
            if(missing.length) throw new Error('Missing runtime names: '+JSON.stringify(missing));
            report.passed=true;report.runtimeNames=names.length;
          }catch(error){report.error=error.stack||String(error);}
          const out=document.createElement('pre');out.id='verification-result';out.textContent=JSON.stringify(report);document.body.append(out);
        });</script>'''
        layout_script=r'''<script>window.addEventListener('DOMContentLoaded',()=>{
          const report={passed:false};
          try {
            const entries=[...document.querySelectorAll('article.entry')];
            if(entries.length!==4002) throw new Error('Missing grouped entries');
            if(new Set(entries.map(entry=>entry.dataset.name)).size!==2105) throw new Error('Lost distinct names');
            if(document.querySelectorAll('.sphere-section[data-kind="sphere"]').length!==10||document.querySelectorAll('.sphere-section[data-kind="extension"]').length!==2) throw new Error('Wrong sphere grouping');
            if(document.querySelector('svg,canvas,img')) throw new Error('Catalog still contains drawings');
            for(const entry of entries) {
              const bounds=entry.getBoundingClientRect(),name=entry.querySelector('h3').getBoundingClientRect();
              if(bounds.left<0||bounds.right>innerWidth+1||name.right>bounds.right+1||name.left<bounds.left-1) throw new Error('Entry overflow: '+entry.id);
              if(entry.closest('.sphere-section').id!==entry.dataset.group) throw new Error('Wrong parent sphere: '+entry.id);
            }
            if(document.documentElement.scrollWidth>innerWidth+1) throw new Error('Page overflows viewport');
            const audit=document.getElementById('zodiac-audit');audit.open=true;
            if(audit.getBoundingClientRect().height<100) throw new Error('Audit does not open');
            const anchor=document.querySelector('.sphere-nav a');anchor.click();
            if(decodeURIComponent(location.hash)!==anchor.getAttribute('href')) throw new Error('Sphere link failed');
            report.passed=true;report.entries=entries.length;report.distinctNames=2105;report.drawings=document.querySelectorAll('svg,canvas,img').length;
          }catch(error){report.error=error.stack||String(error);}
          const out=document.createElement('pre');out.id='verification-result';out.textContent=JSON.stringify(report);document.body.append(out);
        });</script>'''
        reports={}
        for label,source,payload in [
            ('archive',(BASE/'index.html').read_text(encoding='utf-8'),'<script>const EXPECTED_KEYS='+json.dumps(sorted(self.by_key),ensure_ascii=False)+'</script>'+archive_script),
            ('catalogue',self.page,layout_script)]:
            fixture=folder/(label+'.html');fixture.write_text(source.replace('</body>',payload+'\n</body>'),encoding='utf-8')
            command=[str(EDGE),'--headless=new','--no-sandbox','--in-process-gpu','--disable-gpu','--disable-software-rasterizer',
                     '--disable-extensions','--disable-background-networking','--no-first-run','--no-default-browser-check','--disable-sync',
                     '--user-data-dir='+str(folder/(label+'-profile')),'--window-size=390,900','--virtual-time-budget=4000','--dump-dom',fixture.as_uri()]
            result=subprocess.run(command,capture_output=True,encoding='utf-8',errors='replace',timeout=45,
                                  creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            (folder/(label+'-rendered.html')).write_text(result.stdout,encoding='utf-8')
            match=re.search(r'<pre id="verification-result">(.*?)</pre>',result.stdout,re.S)
            self.assertIsNotNone(match,result.stderr[-1500:]+'\nArtifacts: '+str(folder))
            report=json.loads(html.unescape(match[1]));reports[label]=report
            self.assertTrue(report['passed'],str(report)+'\nArtifacts: '+str(folder))
        report_path.write_text(json.dumps(reports,indent=2),encoding='utf-8')


if __name__=='__main__':unittest.main(verbosity=2)
