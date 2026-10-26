# Agrippa Cosmo (אגריפה קוסמו)
### Motore Computazionale Deterministico per la Cosmologia di Cornelio Agrippa e l'Angelologia Cabalistica

Un archivio procedurale statico, autosufficiente e verificato al 100% che mappa e calcola matematicamente le gerarchie angeliche, le matrici numeriche dei pianeti, lo *Shem HaMephorash*, il Nome di 42 Lettere (*Ana Bekoach*) e le 28 Mansioni Lunari (*Manāzil al-Qamar*) con estensione comparativa in arabo (*Abjad*).

---

## 🌟 Caratteristiche Principali

* **Catalogo Unificato Zero-Dependency:** Oltre **2.105 grafie uniche ebraiche** e **4.002 occorrenze** ripartite in 10 Sfere Celesti + 2 Estensioni Geometriche, consultabili interamente offline in [`complete_angel_catalog.html`](complete_angel_catalog.html) (nessun framework, nessun server richiesto).
* **Le 12 Sfere e le Matrici Planetarie ($3\times3 \dots 21\times21$):**
  * Da Saturno ($3\times3$) e Giove ($4\times4$) fino alle estensioni matematico-geometriche del progetto: la **Porta di Tav** ($20\times20$) e il **Sigillo di Verità / Emeth** ($21\times21$).
  * Calcolo esatto e deterministico di tutte le costanti magiche ($M_n$), dei perimetri ($P_n$) e delle somme totali di cella ($S_n$).
* **Generatore del Nome a 42 Lettere (*Ana Bekoach*):**
  * Oltre **2.736 record operativi calcolati** tracciando i 7 versetti liturgici sulle celle dei quadrati planetari.
* **Le 28 Mansioni Lunari (*Manāzil al-Qamar*):**
  * 28 mansioni $\times$ 9 ordini gerarchici celesti calcolati attraverso la colonna segreta della Luna di Agrippa (*De Occulta Philosophia*, III.27).
* **Estensione Comparativa Semitica (Abjad & Arabo):**
  * Modulo [`arabic_orthography.py`](arabic_orthography.py) con calcolatore per l'**Abjad classico (Ḥisāb al-Jummal)** a 28 lettere.
  * Studio comparativo completo in [`islamic_hebrew_angels_atlas.md`](islamic_hebrew_angels_atlas.md) con le concordanze fonetiche e gematriche tra ebraico e arabo (inclusa l'identità $101 = 101$ per Michele / Mīkāl).
* **Affidabilità e Test Suite:**
  * **19 test unitari passati su 19 (100% pass rate)** a garanzia di zero regressioni, link integri e coerenza gematrica.

---

## 🏛️ Architettura delle 12 Sfere Celesti

| Sfera | Denominazione Cosmica | Arcangelo Governatore | Tavola / Ordine | Occorrenze nel Catalogo |
| :---: | :--- | :--- | :---: | :---: |
| **1** | *Primum Mobile / Kether* | **Metatron** (מטטרון = 314) | $10\times10$ | **202** |
| **2** | *Stelle Fisse e Zodiaco / Chokmah* | **Raziel** (רזיאל = 248) | $11\times11$ | **204** |
| **3** | *Saturno / Binah* | **Zaphkiel & Cassiel** (311) | $3\times3$ & $12\times12$ | **371** |
| **4** | *Giove / Chesed* | **Zadkiel & Sachiel** (235/121) | $4\times4$ & $13\times13$ | **372** |
| **5** | *Marte / Geburah* | **Camael** (כמאל = 91) | $5\times5$ & $14\times14$ | **378** |
| **6** | *Sole / Tiphereth* | **Raphael** (רפאל = 311) | $6\times6$ & $15\times15$ | **381** |
| **7** | *Venere / Netzach* | **Haniel & Anael** (96/151) | $7\times7$ & $16\times16$ | **387** |
| **8** | *Mercurio / Hod* | **Michael** (מיכאל = 101) | $8\times8$ & $17\times17$ | **372** |
| **9** | *Luna / Yesod* | **Gabriel** (גבריאל = 246) | $9\times9$ & $18\times18$ | **669** |
| **10** | *Mondo degli Elementi / Malkuth* | **Sandalphon** (סנדלפון = 280) | $19\times19$ | **227** |
| **Ext I** | *Porta di Tav* | **Barbiel & Uriel** | $20\times20$ | **218** |
| **Ext II**| *Sigillo di Verità (Emeth)* | **Advachiel & Metatron** | $21\times21$ | **221** |

---

## 🚀 Guida Rapida (Quickstart)

### Prerequisiti
* Python 3.8 o superiore (nessun pacchetto pip esterno necessario, standard library pura).
* Un qualsiasi browser web moderno per visualizzare i cataloghi statici.

### Esecuzione dei Test
Per verificare l'integrità del catalogo e di tutte le formule:
```bash
python -m unittest discover -s . -p "test_*.py"
```

### Rigenerazione del Catalogo Completo
Se vengono modificate le sorgenti delle tavole o delle ortografie:
```bash
python -X utf8 build_complete_catalog.py
```

### Consultazione Offline
Apri semplicemente il file [`complete_angel_catalog.html`](complete_angel_catalog.html) o [`index.html`](index.html) con un doppio clic o dal browser.

---

## 📂 Struttura della Repository

```
agrippa_cosmo/
├── complete_angel_catalog.html  # Catalogo monolitico visualizzabile (3.1 MB)
├── complete_angel_catalog.json  # Database completo e deduplicato (2.8 MB)
├── index.html                     # Calcolatore interattivo delle sfere e tavole
├── build_complete_catalog.py     # Script builder del catalogo unificato
├── hebrew_orthography.py          # Modulo gematria e traslitterazione ebraica
├── arabic_orthography.py          # Modulo Abjad e comparazione semitica
├── sphere_zodiac.py               # Modulo audit astronomico IAU vs 12 camere
├── lunar_names.py                 # Generatore gerarchie lunari (Agrippa III.27)
├── generate_shem42_angels.py      # Generatore matriciale Ana Bekoach
├── islamic_hebrew_angels_atlas.md # Atlante comparativo Ebraico / Arabo
├── lunar_generated_angels.md      # Tavola integrale delle 28 mansioni
├── test_complete_catalog.py      # Test suite catalogo
├── test_divine_names.py           # Test suite nomi divini
├── test_lunar.py                  # Test suite gerarchia lunare
├── test_orthography.py            # Test suite ortografia e gematria
└── test_shem42_generator.py       # Test suite generatore 42 lettere
```

---

## 📜 Fonti Storiche e Riferimenti Accademici

1. **Heinrich Cornelius Agrippa von Nettesheim**, *De Occulta Philosophia Libri Tres* (Colonia, 1533).
2. **Pseudo-al-Majrīṭī**, *Ġāyat al-Ḥakīm* (*Picatrix*, ed. Pingree, Warburg Institute).
3. **Ahmad al-Būnī**, *Shams al-Maʿārif al-Kubrā* (Il Cairo).
4. **Mistica della Merkavah**, *Sefer Hekhalot* (3 Enoch) e *Sefer Raziel HaMalakh*.
5. **International Astronomical Union (IAU)**, *Constellation Boundaries and Zodiac Audit*.

---

## ⚖️ Licenza
Distribuito con licenza Open Source MIT / Creative Commons per fini di ricerca, studio e Digital Humanities.
