# Przewodnik Deweloperski SubscriptionSage

Ten przewodnik pomoże Ci skonfigurować środowisko deweloperskie do pracy nad SubscriptionSage przy użyciu Dev Containers.

## Wymagania Wstępne

- [Docker](https://www.docker.com/products/docker-desktop)
- [VS Code](https://code.visualstudio.com/) z rozszerzeniem [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Git

## Instrukcje Konfiguracji

### 1. Sklonuj Repozytorium

```bash
git clone [repository-url]
cd SubscriptionSage
```

### 2. Otwórz w VS Code z Dev Containers

1. Otwórz projekt w VS Code:
   ```bash
   code .
   ```

2. Po wyświetleniu monitu, kliknij "Reopen in Container" lub użyj palety poleceń (F1) i wybierz "Dev Containers: Reopen in Container"

   To spowoduje:
   - Zbudowanie kontenera deweloperskiego
   - Zainstalowanie wszystkich zależności
   - Skonfigurowanie bazy danych PostgreSQL
   - Konfigurację środowiska deweloperskiego

### 3. Zmienne Środowiskowe

Kontener deweloperski używa dwóch typów zmiennych środowiskowych:

1. Ustawienia deweloperskie (w `docker-compose.yml`):
```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:postgres@db:5432/subscriptionsage
SESSION_SECRET=your-secret-key-here
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=subscriptionsage
```

2. Ustawienia użytkownika (w `.env`):
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=noreply@subscriptiontracker.com
```

#### Uzyskanie Klucza API Exchange Rate

Aplikacja używa Exchange Rate API do konwersji walut. Aby uzyskać klucz API:

1. Odwiedź [Exchange Rate API](https://www.exchangerate-api.com/)
2. Zarejestruj się za darmowe konto
3. Przejdź do swojego panelu
4. Skopiuj swój klucz API
5. Dodaj go do pliku `.env` jako `EXCHANGE_RATE_API_KEY`

Darmowa wersja zawiera:
- 1,500 zapytań miesięcznie
- Aktualizacje co 24 godziny
- Wsparcie dla USD, EUR, CZK i PLN

Jeśli API jest niedostępne, aplikacja użyje domyślnych kursów wymiany.

Ważne uwagi dotyczące bezpieczeństwa:
- Plik `.env` jest automatycznie ignorowany przez git (jest w `.gitignore`)
- Nigdy nie commituj wrażliwych danych uwierzytelniających do kontroli wersji
- Zabezpiecz swój plik `.env` i nie udostępniaj go
- Dla rozwoju zespołowego, używaj bezpiecznej metody udostępniania zmiennych środowiskowych (jak menedżer haseł lub bezpieczny sejf)

### 4. Uruchom Serwer Deweloperski

Serwer deweloperski uruchomi się automatycznie po zbudowaniu kontenera. Możesz uzyskać dostęp do aplikacji pod adresem http://localhost:5000.

Jeśli potrzebujesz zrestartować serwer:

```bash
docker compose down
docker compose up -d
```

## Przepływ Pracy Deweloperskiej

1. Utwórz nową gałąź dla swojej funkcji lub poprawki błędu
2. Wprowadź zmiany
3. Uruchom testy (jeśli są dostępne)
4. Złóż pull request

## Struktura Projektu

- `app.py`: Konfiguracja i ustawienia aplikacji
- `models.py`: Modele bazy danych
- `routes.py`: Obsługiwacze tras URL
- `scheduler.py`: Harmonogram zadań w tle
- `utils.py`: Funkcje użytkowe
- `templates/`: Szablony HTML
- `static/`: Pliki statyczne (CSS, JS, obrazy)
- `.devcontainer/`: Konfiguracja kontenera deweloperskiego
- `docker-compose.yml`: Konfiguracja usług Docker
- `.env`: Zmienne środowiskowe użytkownika (nie commitowane do gita)

## Funkcje Kontenera Deweloperskiego

Kontener deweloperski zawiera:

- Python 3.11
- PostgreSQL 16
- Wszystkie wymagane pakiety Pythona
- Wstępnie skonfigurowane środowisko deweloperskie
- Hot-reloading dla rozwoju
- Zintegrowane zarządzanie bazą danych

## Uwagi

- Aplikacja używa Flask jako frameworka webowego
- SQLAlchemy jest używany do ORM bazy danych
- Zadania w tle są obsługiwane przez APScheduler
- Cały rozwój odbywa się wewnątrz środowiska konteneryzowanego
- Nie ma potrzeby instalowania Pythona lub PostgreSQL lokalnie
- Spójne środowisko deweloperskie dla wszystkich członków zespołu

# Konfiguracja Deweloperska

1. Sklonuj repozytorium
2. Utwórz środowisko wirtualne:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Na Windows: venv\Scripts\activate
   ```
3. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
4. Utwórz plik `.env` w katalogu głównym z następującymi zmiennymi:
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
5. Zainicjalizuj bazę danych:
   ```bash
   flask db upgrade
   ```
6. Uruchom serwer deweloperski:
   ```bash
   flask run
   ```

## Konfiguracja Exchange Rate API

1. Zarejestruj się za darmowy klucz API na [exchangerate-api.com](https://www.exchangerate-api.com/)
2. Po otrzymaniu klucza API, przejdź do strony Raporty w aplikacji
3. Kliknij "Zarządzaj kluczem API" i wprowadź swój klucz API
4. Kursy wymiany będą automatycznie aktualizowane

## Migracje Bazy Danych

Aby utworzyć nową migrację:
```bash
flask db migrate -m "Opis zmian"
```

Aby zastosować migracje:
```bash
flask db upgrade
```

## Uruchamianie Testów

```bash
python -m pytest
```

## Styl Kodu

Projekt używa Black do formatowania kodu. Aby sformatować swój kod:
```bash
black .
```

## Współtworzenie

1. Utwórz nową gałąź dla swojej funkcji
2. Wprowadź zmiany
3. Uruchom testy i upewnij się, że przechodzą
4. Złóż pull request 