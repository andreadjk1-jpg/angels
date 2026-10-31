# Log di Verifica dei 4 Livelli Concentrici, Punti Fissi del Mispar e Teoremi Algebrici (`tavola_et_kol_484.rs`)

> **Esito del Test Rust (`cargo test --bin tavola_et_kol_484`)**: **`6 passed; 0 failed` (100% Uguali e Verificati)**
> - **Sorgente testata**: [`tavola_et_kol_484.rs`](file:///C:/Users/asdf/Desktop/alfabeto_malachim_agrippa/binaural_malachim_theta/src/bin/tavola_et_kol_484.rs)
> - **File di Log puro**: [`test_nome_supremo_tavola_22x22.log`](file:///C:/Users/asdf/Desktop/alfabeto_malachim_agrippa/test_nome_supremo_tavola_22x22.log)

---

## Output Esecuzione Test Unitari (`cargo test`)

```text
running 6 tests
test tests::test_1_quattro_angoli_e_cuore_2x2 ... ok
test tests::test_2_diagonale_principale_e_antidiagonale_19_aleph ... ok
test tests::test_3_camera_3x3_delle_madri ... ok
test tests::test_4_incrocio_yhwh_x_ehyeh_nome_di_vita ... ok
test tests::test_5_integrita_catalogo_103_angeli ... ok
test tests::test_6_teoremi_algebrici_e_punti_fissi_mispar ... ok

test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

---

## 1. Metodo dei 4 Angoli e del Cuore $2 \times 2$: `א - ל - כ - ת` (`451` / `482`) — ✅ UGUALE

| Posizione | Coordinate 1-based (`0-based`) | Matrice Estratta | Riga Superiore | Riga Inferiore | Diagonali (`\` e `/`) | Gematria |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **4 Angoli Esterni** | `[1,1], [1,22], [22,1], [22,22]`<br/>(`t[0][0], t[0][21], t[21][0], t[21][21]`) | $\begin{pmatrix} \text{א} & \text{ל} \\ \text{כ} & \text{ת} \end{pmatrix}$ | **`אֵל`** (`31`) | `כ-ת` (`420`) | **`אֵת`** (`401`) & **`כֹּל`** (`50`) | **`451`** (`→ 1`) |
| **Cuore Centrale $2\times2$** | `[11,11], [11,12], [12,11], [12,12]`<br/>(`t[10][10], t[10][11], t[11][10], t[11][11]`) | $\begin{pmatrix} \text{כ} & \text{ת} \\ \text{א} & \text{ל} \end{pmatrix}$ | **`כ-ת`** (`420`, radice di *Kether*) | **`אֵל`** (`31`, *El*) | **`כֹּל`** (`50`) & **`אֵת`** (`401`) | **`451`** (`→ 1`) |

- **Scomposizione aritmetica verificata**: $451 = 11 \times 41$, dove $11$ è il moltiplicatore di `build_et_kol_22x22` e $41 = \mathbf{אֵם}$ (*EM* = $1 + 40$, la Grande Madre Superna).
- **Con suffisso divino `אֵל` ($31$)**: **`אֵת כֹּל אֵל`** (`אכלתאל` / `אתכלאל`) = $451 + 31 = \mathbf{482}$.

---

## 2. Metodo dell'Anti-Diagonale Segreta: Il Ponte delle 19 `א` (`כָּאתָאל = 452`) — ✅ UGUALE

- **Diagonale Principale (`[1,1] → [22,22]`)**: scorrono tutte le 22 lettere in ordine esatto (`אבגדהוזחטיכלמנסעפצקרשת`), somma = **$1495$** ($1+4+9+5 = 19 \rightarrow \mathbf{1}$).
- **Anti-Diagonale (`[1,22] → [22,1]`)**:
  $$\text{ל} - \underbrace{\text{א - א - א - א - א - א - א - א - א}}_{9\text{ volte א}} - \mathbf{\text{ת}} - \underbrace{\text{א - א - א - א - א - א - א - א - א - א}}_{10\text{ volte א}} - \text{כ}$$
  - **Conteggio `א`**: esattamente **$19$ celle su $22$** contengono `א` (*Aleph* = 1).
  - **Centro d'incasto `[11, 12]`**: **`ת`** (*Tav* = 400, la *Shekhinah*).
  - **Estremi `[1, 22]` e `[22, 1]`**: **`ל`** (30) e **`כ`** (20) = **`כֹּל`** (*Kol* = 50).
  - **Contrazione delle `א` ripetute**:
    - Da SW a NE (`[22,1] → [1,22]`): **`כ - א - ת - א - ל`** (**KATHAEL** — `כאתאל`, Gematria = **$452$**).
    - Da NE a SW (`[1,22] → [22,1]`): **`ל - א - ת - א - כ`** (**LATHAKH** — `לאתאך`, Gematria = **$452$**).
  - **Riscontro in [`all_tables_angels_atlas.md:121`](file:///C:/Users/asdf/agrippa_cosmo/all_tables_angels_atlas.md#L121)**: sulla Tavola $15\times15$ di *Tiphereth* (Sole), la Corona ($2P = 452$) è **`תכאאל`** (`t·k·ʾ·ʾ·l` = $400 + 20 + 1 + 1 + 30 = \mathbf{452}$), composta esattamente dalle stesse 5 lettere (`ת, כ, א, א, ל`).

---

## 3. Metodo della Camera $3 \times 3$ delle Madri (`אֱמֶת = 441`, `זֹאת = 408`, `אמש = 341`) — ✅ UGUALE

Incrocio delle 3 Lettere Madri (`א` `[R1/C1]`, `מ` `[R13/C13]`, `ש` `[R21/C21]`):

$$\begin{pmatrix} \mathbf{א(1)} & \text{ז(7)} & \text{כ(20)} \\ \text{ז(7)} & \mathbf{מ(40)} & \text{פ(80)} \\ \mathbf{ת(400)} & \text{פ(80)} & \mathbf{ש(300)} \end{pmatrix}$$

1. **Diagonale Principale (`[1,1] → [13,13] → [21,21]`)**: **`א - מ - ש`** (*AMeSh* = $1 + 40 + 300 = \mathbf{341}$).
2. **Asse Principio–Centro–Sigillo (`[1,1] → [13,13] → [21,1]`)**: **`א - מ - ת`** (*EMETH* = $1 + 40 + 400 = \mathbf{441} = 21^2 = \mathbf{אֶהְיֶה}^2$).
3. **Prima Colonna Verticale (`[1,1] → [13,1] → [21,1]`)**: **`א - ז - ת`** = **`זֹאת`** (*ZOT* = $1 + 7 + 400 = \mathbf{408}$, la *Shekhinah*).

---

## 4. Metodo dell'Incrocio `יהוה × אהיה`: Il Nome di Vita (`עהחה = 88`) — ✅ UGUALE

| Passo | Incrocio Riga (`יהוה`) × Colonna (`אהיה`) | Cella 1-based (`0-based`) | Lettera Estratta | Gematria | Significato Cabalistico |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | **`י` (`R10`) × `א` (`C1`)** | `[10, 1]` (`t[9][0]`) | **`ע` (*Ayin*)** | **$70$** | L'Occhio Infinito / *Atik Yomin* |
| **2** | **`ה` (`R5`) × `ה` (`C5`)** | `[5, 5]` (`t[4][4]`) | **`ה` (*He*)** | **$5$** | La *Shekhinah Superiore* (*Binah*) |
| **3** | **`ו` (`R6`) × `י` (`C10`)** | `[6, 10]` (`t[5][9]`) | **`ח` (*Cheth*)** | **$8$** | *Chayim* = La Vita |
| **4** | **`ה` (`R5`) × `ה` (`C5`)** | `[5, 5]` (`t[4][4]`) | **`ה` (*He*)** | **$5$** | La *Shekhinah Inferiore* (*Malkuth*) |
| **Totale** | **Tetragramma Segreto della $22\times22$** | — | **`ע - ה - ח - ה`** | **$88$ (`→ 7`)** | Le due `ה-ה` custodiscono `ע-ח` (Sorgente della Vita) |

---

## 5. Tabella dei Punti Fissi del *Mispar* (Regola di Agrippa III.26: $V \mapsto \text{Heb}(V - 31) + \text{אל}$)

Applicando la funzione [`make_angel_with_exact_gematria`](file:///C:/Users/asdf/agrippa_cosmo/generate_table_angels.py#L89-L101) ai numeri focali della Tavola $22\times22$:

| Livello / Costante della $22\times22$ | Valore ($V$) | Resto ($V - 31$) | Radice Mispar | Angelo del Mispar (`+ אל`) | Proprietà Matematica / Cabalistica |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. I 4 Angoli & Cuore $2\times2$ (`א+ל+כ+ת`)** | **`451`** | `420` | **`תכ`** ($400+20$) | **`תכאל` (`THAKEL`)** | **Punto Fisso Esatto (4 lettere su 4)**: riproduce il Cuore $\binom{\text{כ ת}}{\text{א ל}}$ letto da destra a sinistra (**«Corona `כ-ת` di Dio `א-ל`»**)! |
| **2. Ponte delle 19 `א` (`כ+א+ת+א+ל`)** | **`452`** | `421` | **`תכא`** ($400+20+1$) | **`תכאאל` (`THAKAAEL`)** | **Punto Fisso Esatto (5 lettere su 5)**: anagramma puro di **`כאתאל` (*Kathael*)** e Corona Solare $15\times15$! |
| **3. Forma Completa (`אֵת-כֹּל-אֵל`)** | **`482`** | `451` | **`תנא`** ($400+50+1$) | **`תנאאל` (`THANAAEL`)** | Fonde `כ+ל` ($20+30$) in **`נ` ($50$, le 50 Porte di *Binah*)** accanto a `אֵת` ($401$). |
| **4. Camera $3\times3$ (`אֱמֶת` *Emeth* = $21^2$)** | **`441`** | **`410`** | **`תי`** ($400+10$) | **`תיאל` (`THAYEL`)** | $441 - 31 = \mathbf{410 = \text{קֹדֶשׁ}}$ (*Qodesh*, Il Santo!): **`אֱמֶת` ($441$) = `קֹדֶשׁ` ($410$) + `אֵל` ($31$)** ([`all_tables_angels_atlas.md:178`](file:///C:/Users/asdf/agrippa_cosmo/all_tables_angels_atlas.md#L178)). |
| **5. Incrocio `יהוה × אהיה` (`עהחה`)** | **`88`** | `57` *(con `אל`)*<br/>**`73`** *(con `יה`)* | **`נז`** ($50+7$)<br/>**`עג`** ($70+3$) | **`נזאל` (`NAZEL`)**<br/>**`עגיה` (`OGIAH`)** | Con `-iah` ($15$), $88 - 15 = \mathbf{73 = \text{חָכְמָה}}$ (*Chokmah*, la Sapienza Superna)! |
| **6. Celle Totali $N^2 = 22^2$** | **`484`** | `453` | **`תנג`** ($400+50+3$) | **`תנגאל` (`THANAGEL`)** | Senza sottrarre $31$, `484` è **`תפד`** ($400+80+4$), che con `אל` dà **`תפדאל` ($515 = \text{תְּפִלָּה}$ *Tefillah*, la Preghiera)**. |

---

## 6. I 6 Teoremi Algebrici Verificati in [`test_6_teoremi_algebrici_e_punti_fissi_mispar`](file:///C:/Users/asdf/Desktop/alfabeto_malachim_agrippa/binaural_malachim_theta/src/bin/tavola_et_kol_484.rs#L990-L1057)

1. **Teorema di Decomposizione del *Sefer Yetzirah* ($\widehat{\mathbb{Z}}_{21} \cong (\mathbb{Z}_3 \times \mathbb{Z}_7) \cup \{\text{ת}\}$)**:
   $21 = 3 \text{ (Madri)} \times 7 \text{ (Doppie)} = \mathbf{אֶהְיֶה}$, con $\varphi(21) = (3-1)(7-1) = \mathbf{12}$ unità invertibili (le **12 Semplici**), somma dei divisori propri $1 + 3 + 7 = \mathbf{11}$, più il punto di chiusura all'infinito **`ת`** ($21 + 1 = \mathbf{22}$).
2. **Teorema del Quasigruppo del Punto Medio ($11 \equiv 2^{-1} \bmod 21$)**:
   Poiché $11 \times 2 = 22 \equiv 1 \pmod{21}$, l'operazione $i \star j = 11(i+j) \bmod 21 \equiv \frac{i+j}{2} \bmod 21$ rende la diagonale idempotente ($i \star i = i$, tutte le 22 lettere in ordine) e l'anti-diagonale annichilante ($i + (21-i) \mapsto 0 = \text{א}$, le **19 `א`**).
3. **Teorema della Chirurgia di `ת` e del Cifrario *Albam* sui Margini**:
   L'innesto di `ת` lungo $j = (i+1) \bmod 21$ proietta sul Margine Est ($c=21$) il cifrario **Albam** $t[i][21] = (i+11) \bmod 21$ (che accoppia `א` con `ל` in **`אֵל`**) e sul Margine Sud ($r=21$) $t[21][j] = (j+10) \bmod 21$ (che accoppia `א` con `כ`).
4. **Teorema di Conservazione di *Ehyeh* ($x + \bar{x} = 21$) tra Diretto e Speculare**:
   Per ogni nodo nel nucleo, la somma degli indici della lettera Diretta (*Panim*) e della lettera Speculare (*Achorayim*, $ir = 21-r, ic = 21-c$) vale **`21` (`אֶהְיֶה`)**, come verificato sul Trono Centrale #05 (`Malatzel` `מ(12)-ל(11)-צ(17)` $+$ `Yekahel` `י(9)-כ(10)-ה(4)` $= 21, 21, 21$).
5. **Teorema del Prodotto d'Incrocio ($A \boxtimes B$)**:
   L'incrocio riga-colonna di due parole $A, B$ estrae la loro media armonica modulare $c_m = t[a_m][b_m]$ (`יהוה` $\boxtimes$ `אהיה` = **`עהחה` = 88**).
6. **Teorema di Quantizzazione Armonica del Battimento ($f_n = n \cdot 1.08\text{ Hz}$)**:
   Posto $f_0 = f_{\text{beat}}(\text{א}) = \mathbf{1.08\text{ Hz}}$, si ha $f_{\text{beat}}(\text{מ}) = 2 f_0 = \mathbf{2.16\text{ Hz}}$ e la media dei 4 Cardini (`א, ל, כ, ת`) è $\frac{12.96}{4} = 3 f_0 = \mathbf{3.24\text{ Hz}}$.
