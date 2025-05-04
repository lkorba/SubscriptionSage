# Vývojový Průvodce SubscriptionSage

Tento průvodce vám pomůže nastavit vývojové prostředí pro práci na SubscriptionSage pomocí Dev Containers.

## Předpoklady

- [Docker](https://www.docker.com/products/docker-desktop)
- [VS Code](https://code.visualstudio.com/) s rozšířením [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Git

## Instrukce k Nastavení

### 1. Naklonujte Repozitář

```bash
git clone [repository-url]
cd SubscriptionSage
```

### 2. Otevřete ve VS Code s Dev Containers

1. Otevřete projekt ve VS Code:
   ```bash
   code .
   ```

2. Po zobrazení výzvy klikněte na "Reopen in Container" nebo použijte paletu příkazů (F1) a vyberte "Dev Containers: Reopen in Container"

   Toto způsobí:
   - Sestavení vývojového kontejneru
   - Instalaci všech závislostí
   - Nastavení databáze PostgreSQL
   - Konfiguraci vývojového prostředí

### 3. Proměnné Prostředí

Vývojový kontejner používá dva typy proměnných prostředí:

1. Vývojová nastavení (v `docker-compose.yml`):
```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:postgres@db:5432/subscriptionsage
SESSION_SECRET=your-secret-key-here
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=subscriptionsage
```

2. Uživatelská nastavení (v `.env`):
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=noreply@subscriptiontracker.com
```

#### Získání API Klíče Exchange Rate

Aplikace používá Exchange Rate API pro převod měn. Pro získání API klíče:

1. Navštivte [Exchange Rate API](https://www.exchangerate-api.com/)
2. Zaregistrujte se pro bezplatný účet
3. Přejděte do svého dashboardu
4. Zkopírujte svůj API klíč
5. Přidejte ho do souboru `.env` jako `EXCHANGE_RATE_API_KEY`

Bezplatná verze zahrnuje:
- 1,500 požadavků měsíčně
- Aktualizace každých 24 hodin
- Podporu pro USD, EUR, CZK a PLN

Pokud je API nedostupné, aplikace použije výchozí směnné kurzy.

Důležité bezpečnostní poznámky:
- Soubor `.env` je automaticky ignorován gitem (je v `.gitignore`)
- Nikdy necommitujte citlivé přihlašovací údaje do verzového systému
- Uchovávejte svůj soubor `.env` v bezpečí a nesdílejte ho
- Pro týmový vývoj používejte bezpečnou metodu sdílení proměnných prostředí (jako správce hesel nebo bezpečný trezor)

### 4. Spusťte Vývojový Server

Vývojový server se spustí automaticky po sestavení kontejneru. K aplikaci můžete přistupovat na http://localhost:5000.

Pokud potřebujete restartovat server:

```bash
docker compose down
docker compose up -d
```

## Vývojový Pracovní Postup

1. Vytvořte novou větev pro vaši funkci nebo opravu chyby
2. Proveďte změny
3. Spusťte testy (pokud jsou k dispozici)
4. Odešlete pull request

## Struktura Projektu

- `app.py`: Nastavení a konfigurace aplikace
- `models.py`: Databázové modely
- `routes.py`: Obsluhy URL tras
- `scheduler.py`: Plánovač úloh na pozadí
- `utils.py`: Užitečné funkce
- `templates/`: HTML šablony
- `static/`: Statické soubory (CSS, JS, obrázky)
- `.devcontainer/`: Konfigurace vývojového kontejneru
- `docker-compose.yml`: Konfigurace Docker služeb
- `.env`: Uživatelské proměnné prostředí (necommitované do gitu)

## Funkce Vývojového Kontejneru

Vývojový kontejner obsahuje:

- Python 3.11
- PostgreSQL 16
- Všechny požadované Python balíčky
- Předkonfigurované vývojové prostředí
- Hot-reloading pro vývoj
- Integrovanou správu databáze

## Poznámky

- Aplikace používá Flask jako webový framework
- SQLAlchemy je používán pro databázový ORM
- Úlohy na pozadí jsou zpracovávány APSchedulerem
- Veškerý vývoj probíhá uvnitř kontejnerizovaného prostředí
- Není potřeba instalovat Python nebo PostgreSQL lokálně
- Konzistentní vývojové prostředí pro všechny členy týmu

# Vývojové Nastavení

1. Naklonujte repozitář
2. Vytvořte virtuální prostředí:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Na Windows: venv\Scripts\activate
   ```
3. Nainstalujte závislosti:
   ```bash
   pip install -r requirements.txt
   ```
4. Vytvořte soubor `.env` v kořenovém adresáři s následujícími proměnnými:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password_here
   ```
5. Inicializujte databázi:
   ```bash
   flask db upgrade
   ```
6. Spusťte vývojový server:
   ```bash
   flask run
   ```

## Nastavení Exchange Rate API

1. Zaregistrujte se pro bezplatný API klíč na [exchangerate-api.com](https://www.exchangerate-api.com/)
2. Po získání API klíče přejděte na stránku Reporty v aplikaci
3. Klikněte na "Spravovat API klíč" a zadejte svůj API klíč
4. Směnné kurzy budou automaticky aktualizovány

## Migrace Databáze

Pro vytvoření nové migrace:
```bash
flask db migrate -m "Popis změn"
```

Pro aplikaci migrací:
```bash
flask db upgrade
```

## Spouštění Testů

```bash
python -m pytest
```

## Styl Kódu

Projekt používá Black pro formátování kódu. Pro formátování vašeho kódu:
```bash
black .
```

## Přispívání

1. Vytvořte novou větev pro vaši funkci
2. Proveďte změny
3. Spusťte testy a ujistěte se, že procházejí
4. Odešlete pull request 