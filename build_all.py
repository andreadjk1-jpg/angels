"""Master Build Script: Generatore Universale di Tutto l'Archivio Agrippa Cosmo.

Questo script esegue l'intera pipeline generativa procedurale in sequenza:
1. Nomi e angeli strutturali delle tavole planetarie (3x3 - 21x21)
2. Nomi generati dal Nome a 42 lettere (Ana Bekoach)
3. Formule dei Nomi Divini di 42 lettere
4. Gerarchie lunari delle 28 Mansioni (Agrippa III.27)
5. Audit astronomico delle sfere e dello zodiaco IAU
6. Compilazione del visualizzatore dei 12 Cieli
7. Compilazione del Catalogo Completo (complete_angel_catalog.html & .json)
8. Esecuzione della test suite automatizzata (19 test unitari)

Uso:
    python -X utf8 build_all.py
"""
import os
import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

PIPELINE = [
    {
        "name": "1. Struttura delle Tavole Planetarie (3x3 - 21x21)",
        "script": "generate_table_angels.py",
        "description": "Genera table_angels_generated.json e all_tables_angels_atlas.md"
    },
    {
        "name": "2. Nomi Generati Shem 42 (Ana Bekoach)",
        "script": "generate_shem42_angels.py",
        "description": "Genera shem42_generated_angels.json e shem42_generated_angels.md"
    },
    {
        "name": "3. Nomi Divini a 42 Lettere",
        "script": "divine_names.py",
        "description": "Genera shem42_divine_names.json e shem42_letter_name.md"
    },
    {
        "name": "4. Gerarchie Lunari delle 28 Mansioni",
        "script": "lunar_names.py",
        "description": "Genera lunar_angels_generated.json e lunar_generated_angels.md"
    },
    {
        "name": "5. Audit Sfere e Zodiaco IAU",
        "script": "sphere_zodiac.py",
        "description": "Genera verify_spheres_zodiac.json e verify_spheres_zodiac.md"
    },
    {
        "name": "6. Compilazione HTML 12 Cieli",
        "script": "build_angels_html.py",
        "description": "Compila angels_12_heavens.html"
    },
    {
        "name": "7. Compilazione Catalogo Completo Unificato",
        "script": "build_complete_catalog.py",
        "description": "Compila complete_angel_catalog.html e complete_angel_catalog.json"
    }
]


def run_pipeline():
    start_total = time.time()
    print("=" * 70)
    print("       AGRIPPA COSMO: GENERATORE UNIVERSALE PROCEDURALE")
    print("=" * 70)
    print(f"Directory radice: {BASE_DIR}\n")

    for step in PIPELINE:
        name = step["name"]
        script = step["script"]
        desc = step["description"]
        script_path = BASE_DIR / script

        print(f"[*] Avvio: {name}")
        print(f"    Script: {script} ({desc})")
        
        t0 = time.time()
        cmd = [sys.executable, "-X", "utf8", str(script_path)]
        res = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True)
        elapsed = time.time() - t0

        if res.returncode != 0:
            print(f"\n[!] ERRORE durante {script} (codice {res.returncode}):")
            print(res.stderr or res.stdout)
            sys.exit(res.returncode)
        
        output_clean = res.stdout.strip()
        if output_clean:
            first_line = output_clean.splitlines()[0]
            print(f"    Output: {first_line}")
        print(f"    [✔] Completato in {elapsed:.2f}s\n")

    # Passo 8: Esecuzione Test Suite
    print("=" * 70)
    print("[*] Passo 8: Esecuzione della Test Suite Completa (19 Test Unitari)...")
    t0 = time.time()
    test_cmd = [sys.executable, "-m", "unittest", "discover", "-s", str(BASE_DIR), "-p", "test_*.py"]
    test_res = subprocess.run(test_cmd, cwd=str(BASE_DIR), capture_output=True, text=True)
    test_elapsed = time.time() - t0

    if test_res.returncode != 0:
        print("[!] Alcuni test sono falliti:")
        print(test_res.stderr or test_res.stdout)
        sys.exit(test_res.returncode)
    else:
        print(f"    [✔] Tutti i test unitari superati con successo in {test_elapsed:.2f}s!")

    total_time = time.time() - start_total
    print("\n" + "=" * 70)
    print(f"    GENERAZIONE TOTALE COMPLETATA CON SUCCESSO IN {total_time:.2f}s!")
    print("    Tutti i cataloghi, JSON, MD e HTML sono sincronizzati e verificati.")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()
