#!/usr/bin/env python3
"""
SEO Meta Tags Updater for Domain Pages
Updates all 17 domain pages with optimized SEO meta tags
"""

import re
from pathlib import Path

# Domain pages configuration with SEO-optimized titles and descriptions
DOMAIN_PAGES = {
    "executari-silite.html": {
        "title": "Executări Silite Fălticeni | Avocat Murarașu - Contestații și Recuperare",
        "description": "Asistență executări silite în Fălticeni și Suceava. Contestații, recuperare creanțe, proceduri ANAF. Cabinet Avocat Murarașu.",
        "keywords": "executări silite fălticeni, contestație executare, recuperare creanțe, ANAF, avocat executare"
    },
    "drept-familie.html": {
        "title": "Drept Familie Fălticeni | Divorț, Custodie | Avocat Murarașu Suceava",
        "description": "Specialist drept de familie în Fălticeni: divorț, custodie, pensie alimentară. Abordare empatică. Avocat Andreea Murarașu ☎️ +40 747 926 723",
        "keywords": "drept familie fălticeni, divorț suceava, custodie copii, pensie alimentară, avocat familie"
    },
    "drept-penal.html": {
        "title": "Drept Penal Fălticeni | Apărare Penală | Avocat Murarașu Suceava",
        "description": "Apărare penală specializată în Fălticeni: inculpați, parte vătămată, cauțiune. Experiență 15 ani. Avocat Murarașu ☎️ +40 747 926 723",
        "keywords": "drept penal fălticeni, avocat penal suceava, apărare penală, inculpat, parte vătămată"
    },
    "drept-imobiliar.html": {
        "title": "Drept Imobiliar Fălticeni | Tranzacții și Litigii | Avocat Murarașu",
        "description": "Drept imobiliar Fălticeni: vânzare-cumpărare, verificare documente, uzucapiune. Avocat specializat. ☎️ +40 747 926 723",
        "keywords": "drept imobiliar fălticeni, tranzacții imobiliare, uzucapiune, verificare acte, avocat imobiliar"
    },
    "dreptul-muncii.html": {
        "title": "Dreptul Muncii Fălticeni | Litigii Angajați | Avocat Murarașu Suceava",
        "description": "Dreptul muncii Fălticeni: concediere, drepturi salariale, hărțuire. Protejăm drepturile angajaților. Avocat Murarașu ☎️ +40 747 926 723",
        "keywords": "dreptul muncii fălticeni, concediere abuzivă, drepturi angajați, litigii muncă, avocat muncă"
    },
    "migratie-azil.html": {
        "title": "Migrație și Azil Fălticeni | Avocat Murarașu - Statut Refugiat",
        "description": "Asistență migrație și azil în Fălticeni: cerere azil, statut refugiat, protecție subsidiară. Avocat specializat Murarașu ☎️ +40 747 926 723",
        "keywords": "migrație azil fălticeni, cerere azil românia, statut refugiat, protecție subsidiară, avocat imigrație"
    },
    "societati-comerciale.html": {
        "title": "Societăți Comerciale Fălticeni | Înființare SRL | Avocat Murarașu",
        "description": "Servicii societăți comerciale Fălticeni: înființare SRL, PFA, modificări, dizolvare. Avocat Murarașu Suceava ☎️ +40 747 926 723",
        "keywords": "înființare srl fălticeni, societăți comerciale, PFA, dizolvare firmă, avocat afaceri"
    },
    "drept-bancar-si-fiscal.html": {
        "title": "Drept Bancar și Fiscal Fălticeni | Avocat Murarașu Suceava",
        "description": "Drept bancar și fiscal Fălticeni: litigii bancare, ANAF, datorii, restructurare. Avocat specializat Murarașu ☎️ +40 747 926 723",
        "keywords": "drept bancar fălticeni, litigii fiscale, ANAF, datorii bancare, avocat fiscal"
    },
    "proprietate-intelectuala.html": {
        "title": "Proprietate Intelectuală Fălticeni | Mărci, Brevete | Avocat Murarașu",
        "description": "Protecție proprietate intelectuală: mărci, brevete, drepturi autor, design. Avocat Murarașu Fălticeni ☎️ +40 747 926 723",
        "keywords": "proprietate intelectuală, înregistrare marcă, brevete, drepturi autor, avocat PI"
    },
    "contracte.html": {
        "title": "Redactare Contracte Fălticeni | Avocat Murarașu - Consultanță Juridică",
        "description": "Redactare și verificare contracte în Fălticeni: comerciale, civile, muncă. Avocat specialist Murarașu ☎️ +40 747 926 723",
        "keywords": "redactare contracte fălticeni, verificare contract, consultanță contractuală, avocat contracte"
    },
    "consultanta-negocieri.html": {
        "title": "Consultanță Juridică Fălticeni | Negocieri | Avocat Murarașu Suceava",
        "description": "Consultanță juridică și negocieri în Fălticeni. Soluții amiabile, mediere, negocieri contractuale. Avocat Murarașu ☎️ +40 747 926 723",
        "keywords": "consultanță juridică fălticeni, negocieri juridice, mediere, soluții amiabile, avocat consultant"
    },
    "asociatii-fundatii.html": {
        "title": "Asociații și Fundații Fălticeni | Înființare ONG | Avocat Murarașu",
        "description": "Servicii asociații și fundații Fălticeni: înființare ONG, modificări statute, dizolvare. Avocat Murarașu ☎️ +40 747 926 723",
        "keywords": "înființare asociație fălticeni, ONG, fundații, statute asociație, avocat non-profit"
    },
    "amenzi-contraventii.html": {
        "title": "Amenzi și Contravenții Fălticeni | Contestații | Avocat Murarașu",
        "description": "Contestații amenzi și contravenții Fălticeni. Anulare procese verbale, reducere amenzi. Avocat Murarașu ☎️ +40 747 926 723",
        "keywords": "contestație amendă fălticeni, contravenții, anulare proces verbal, avocat contravenții"
    },
    "accidente-auto.html": {
        "title": "Accidente Auto Fălticeni | Daune RCA | Avocat Murarașu Suceava",
        "description": "Asistență accidente auto Fălticeni: daune RCA, CASCO, vătămări corporale. Recuperare despăgubiri. Avocat Murarașu ☎️ +40 747 926 723",
        "keywords": "accident auto fălticeni, daune RCA, despăgubiri, vătămări corporale, avocat asigurări"
    },
    "cetatenie.html": {
        "title": "Cetățenie Română Fălticeni | Avocat Murarașu - Redobândire Cetățenie",
        "description": "Asistență cetățenie română Fălticeni: redobândire, dobândire, renunțare. Dosare complete. Avocat Murarașu ☎️ +40 747 926 723",
        "keywords": "cetățenie română, redobândire cetățenie, dobândire cetățenie, avocat cetățenie fălticeni"
    },
    "vize-permise-sedere.html": {
        "title": "Vize și Permise Ședere Fălticeni | Avocat Murarașu Suceava",
        "description": "Asistență vize și permise de ședere Fălticeni: prelungire, obținere, contestații. Avocat specializat Murarașu ☎️ +40 747 926 723",
        "keywords": "vize românia, permise ședere, prelungire viză, rezidență, avocat imigrație fălticeni"
    }
}

def update_domain_page(file_path, seo_data):
    """Update a single domain page with SEO meta tags"""

    content = file_path.read_text(encoding='utf-8')

    # Pattern to match the old meta tags section
    old_pattern = re.compile(
        r'(<meta charset="UTF-8">.*?<meta name="twitter:image"[^>]+>)',
        re.DOTALL
    )

    # Create new meta tags block
    new_meta = f'''<meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="language" content="Romanian">

    <!-- Primary Meta Tags -->
    <title>{seo_data["title"]}</title>
    <meta name="description" content="{seo_data["description"]}">
    <meta name="keywords" content="{seo_data["keywords"]}">
    <link rel="canonical" href="https://www.avocatmurarasu.ro/pages/domenii/{file_path.name}">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://www.avocatmurarasu.ro/pages/domenii/{file_path.name}">
    <meta property="og:title" content="{seo_data["title"]}">
    <meta property="og:description" content="{seo_data["description"]}">
    <meta property="og:image" content="https://www.avocatmurarasu.ro/public/images/andreea-01.jpeg">
    <meta property="og:locale" content="ro_RO">
    <meta property="og:site_name" content="Avocat Andreea Murarașu">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://www.avocatmurarasu.ro/pages/domenii/{file_path.name}">
    <meta name="twitter:title" content="{seo_data["title"]}">
    <meta name="twitter:description" content="{seo_data["description"]}">
    <meta name="twitter:image" content="https://www.avocatmurarasu.ro/public/images/andreea-01.jpeg">'''

    # Replace the old meta tags
    updated_content = old_pattern.sub(new_meta, content)

    # Write back
    file_path.write_text(updated_content, encoding='utf-8')
    return True

def main():
    """Update all domain pages"""
    domain_dir = Path("pages/domenii")

    if not domain_dir.exists():
        print(f"Error: Directory {domain_dir} not found")
        return

    updated_count = 0

    for filename, seo_data in DOMAIN_PAGES.items():
        file_path = domain_dir / filename

        if file_path.exists():
            try:
                update_domain_page(file_path, seo_data)
                print(f"✓ Updated: {filename}")
                updated_count += 1
            except Exception as e:
                print(f"✗ Error updating {filename}: {e}")
        else:
            print(f"✗ File not found: {filename}")

    print(f"\n{updated_count}/{len(DOMAIN_PAGES)} domain pages updated successfully!")

if __name__ == "__main__":
    main()
