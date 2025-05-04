# Přispívání do SubscriptionSage

Děkujeme za váš zájem o přispívání do SubscriptionSage! Tento dokument poskytuje pokyny a instrukce pro přispívání do projektu.

## Obsah

- [Kodex Chování](#kodex-chování)
- [Začínáme](#začínáme)
- [Vývojový Pracovní Postup](#vývojový-pracovní-postup)
- [Proces Pull Requestu](#proces-pull-requestu)
- [Vývojové Pokyny](#vývojové-pokyny)
- [Testování](#testování)
- [Dokumentace](#dokumentace)
- [Otázky a Diskuze](#otázky-a-diskuze)

## Kodex Chování

Účastí na tomto projektu souhlasíte s dodržováním našeho [Kodexu Chování](CODE_OF_CONDUCT.md). Přečtěte si ho prosím před přispíváním.

## Začínáme

1. Fork repozitáře
2. Naklonujte svůj fork:
   ```bash
   git clone https://github.com/vaše-uživatelské-jméno/SubscriptionSage.git
   cd SubscriptionSage
   ```
3. Nastavte vývojové prostředí pomocí Dev Containers (viz [Vývojový Průvodce](DEVELOPMENT.md))
4. Vytvořte novou větev pro vaši funkci nebo opravu chyby

## Vývojový Pracovní Postup

1. **Vytvořte Větev**
   - Konvence pojmenování větví:
     - Funkce: `feature/popis`
     - Opravy chyb: `fix/popis`
     - Dokumentace: `docs/popis`
     - Hotfixy: `hotfix/popis`

2. **Proveďte Změny**
   - Dodržujte [Stylový Průvodce](STYLE_GUIDE.md)
   - Pište jasné, popisné commit zprávy
   - Udržujte změny zaměřené a atomické
   - Aktualizujte dokumentaci podle potřeby

3. **Otestujte Své Změny**
   - Napište nebo aktualizujte testy podle potřeby
   - Ujistěte se, že všechny testy procházejí
   - Otestujte své změny ručně

4. **Odešlete Pull Request**
   - Pushujte svou větev do svého forku
   - Vytvořte pull request proti hlavnímu repozitáři
   - Vyplňte šablonu pull requestu

## Proces Pull Requestu

1. **Před Odesláním**
   - Ujistěte se, že váš kód dodržuje stylový průvodce
   - Aktualizujte dokumentaci pro nové funkce
   - Přidejte testy pro novou funkcionalitu
   - Ujistěte se, že všechny testy procházejí
   - Aktualizujte changelog pokud je to relevantní

2. **Šablona Pull Requestu**
   - Popis změn
   - Číslo souvisejícího issue (pokud je relevantní)
   - Typ změny (funkce, oprava chyby, dokumentace)
   - Provedené testy
   - Screenshoty (pokud je to relevantní)

3. **Proces Revize**
   - Všechny pull requesty vyžadují alespoň jednu revizi
   - Reagujte na jakoukoli zpětnou vazbu od revizorů
   - Udržujte pull request aktuální s hlavní větví

## Vývojové Pokyny

### Styl Kódu

- Dodržujte [Stylový Průvodce](STYLE_GUIDE.md)
- Používejte smysluplné názvy proměnných a funkcí
- Pište jasné, stručné komentáře
- Udržujte funkce malé a zaměřené
- Používejte typové anotace pro Python kód

### Změny v Databázi

- Vytvářejte migrace pro jakékoli změny schématu databáze
- Testujte migrace oběma směry
- Zahrňte skripty pro migraci dat pokud je to potřeba
- Dokumentujte jakékoli breaking changes

### Frontend Vývoj

- Dodržujte BEM konvenci pojmenování pro CSS
- Používejte sémantický HTML
- Zajistěte responzivní design
- Testujte napříč různými prohlížeči
- Optimalizujte assety

## Testování

### Spouštění Testů

```bash
# Spusťte všechny testy
pytest

# Spusťte konkrétní testovací soubor
pytest tests/test_file.py

# Spusťte s pokrytím
pytest --cov=.
```

### Psaní Testů

- Pište testy pro nové funkce
- Aktualizujte testy pro opravy chyb
- Dodržujte AAA vzor (Arrange, Act, Assert)
- Používejte smysluplné názvy testů
- Testujte hraniční případy a chybové stavy

## Dokumentace

### Dokumentace Kódu

- Dokumentujte všechna veřejná API
- Používejte jasné, stručné docstringy
- Zahrňte příklady pro složité funkce
- Udržujte dokumentaci aktuální

### Uživatelská Dokumentace

- Aktualizujte README.md pro významné změny
- Dokumentujte nové funkce
- Aktualizujte API dokumentaci
- Zahrňte příklady použití

## Otázky a Diskuze

- Používejte GitHub Issues pro hlášení chyb a požadavky na funkce
- Používejte GitHub Discussions pro obecné otázky
- Připojte se k našemu komunitnímu chatu (pokud je dostupný)
- Zkontrolujte existující issues a diskuze před vytvořením nových

## Další Zdroje

- [Vývojový Průvodce](DEVELOPMENT.md)
- [Stylový Průvodce](STYLE_GUIDE.md)
- [Kodex Chování](CODE_OF_CONDUCT.md)
- [Roadmapa Projektu](ROADMAP.md) (pokud je dostupná)

## Získání Pomoci

Pokud potřebujete pomoc nebo máte otázky:

1. Zkontrolujte dokumentaci
2. Prohledejte existující issues a diskuze
3. Vytvořte nový issue nebo diskuzi
4. Kontaktujte správce na lukasz.korbasiewicz@gmail.com

Děkujeme za přispívání do SubscriptionSage! 