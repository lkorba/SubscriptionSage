# Współtworzenie SubscriptionSage

Dziękujemy za zainteresowanie współtworzeniem SubscriptionSage! Ten dokument zawiera wytyczne i instrukcje dotyczące współtworzenia projektu.

## Spis Treści

- [Kodeks Postępowania](#kodeks-postępowania)
- [Rozpoczęcie Pracy](#rozpoczęcie-pracy)
- [Przepływ Pracy Deweloperskiej](#przepływ-pracy-deweloperskiej)
- [Proces Pull Request](#proces-pull-request)
- [Wytyczne Deweloperskie](#wytyczne-deweloperskie)
- [Testowanie](#testowanie)
- [Dokumentacja](#dokumentacja)
- [Pytania i Dyskusje](#pytania-i-dyskusje)

## Kodeks Postępowania

Uczestnicząc w tym projekcie, zgadzasz się przestrzegać naszego [Kodeksu Postępowania](CODE_OF_CONDUCT.md). Prosimy o zapoznanie się z nim przed rozpoczęciem współtworzenia.

## Rozpoczęcie Pracy

1. Sforkuj repozytorium
2. Sklonuj swój fork:
   ```bash
   git clone https://github.com/twoja-nazwa-uzytkownika/SubscriptionSage.git
   cd SubscriptionSage
   ```
3. Skonfiguruj środowisko deweloperskie używając Dev Containers (patrz [Przewodnik Deweloperski](DEVELOPMENT.md))
4. Utwórz nową gałąź dla swojej funkcji lub poprawki błędu

## Przepływ Pracy Deweloperskiej

1. **Utwórz Gałąź**
   - Konwencja nazewnictwa gałęzi:
     - Funkcje: `feature/opis`
     - Poprawki błędów: `fix/opis`
     - Dokumentacja: `docs/opis`
     - Gorące poprawki: `hotfix/opis`

2. **Wprowadź Zmiany**
   - Postępuj zgodnie z [Przewodnikiem Stylu](STYLE_GUIDE.md)
   - Pisz jasne, opisowe komunikaty commitów
   - Utrzymuj zmiany skupione i atomowe
   - Aktualizuj dokumentację w razie potrzeby

3. **Przetestuj Swoje Zmiany**
   - Napisz lub zaktualizuj testy w razie potrzeby
   - Upewnij się, że wszystkie testy przechodzą
   - Przetestuj swoje zmiany ręcznie

4. **Złóż Pull Request**
   - Wypchnij swoją gałąź do swojego forka
   - Utwórz pull request przeciwko głównemu repozytorium
   - Wypełnij szablon pull requesta

## Proces Pull Request

1. **Przed Złożeniem**
   - Upewnij się, że Twój kod jest zgodny z przewodnikiem stylu
   - Zaktualizuj dokumentację dla nowych funkcji
   - Dodaj testy dla nowej funkcjonalności
   - Upewnij się, że wszystkie testy przechodzą
   - Zaktualizuj changelog jeśli dotyczy

2. **Szablon Pull Requesta**
   - Opis zmian
   - Numer powiązanego issue (jeśli dotyczy)
   - Typ zmiany (funkcja, poprawka błędu, dokumentacja)
   - Przeprowadzone testy
   - Zrzuty ekranu (jeśli dotyczy)

3. **Proces Przeglądu**
   - Wszystkie pull requesty wymagają co najmniej jednego przeglądu
   - Odpowiedz na wszelkie uwagi od recenzentów
   - Utrzymuj pull request aktualny z główną gałęzią

## Wytyczne Deweloperskie

### Styl Kodu

- Postępuj zgodnie z [Przewodnikiem Stylu](STYLE_GUIDE.md)
- Używaj znaczących nazw zmiennych i funkcji
- Pisz jasne, zwięzłe komentarze
- Utrzymuj funkcje małe i skupione
- Używaj adnotacji typów dla kodu Pythona

### Zmiany w Bazie Danych

- Twórz migracje dla wszelkich zmian schematu bazy danych
- Testuj migracje w obu kierunkach
- Dołącz skrypty migracji danych jeśli potrzebne
- Dokumentuj wszelkie zmiany łamiące kompatybilność

### Rozwój Frontendu

- Postępuj zgodnie z konwencją nazewnictwa BEM dla CSS
- Używaj semantycznego HTML
- Zapewnij responsywny design
- Testuj na różnych przeglądarkach
- Optymalizuj zasoby

## Testowanie

### Uruchamianie Testów

```bash
# Uruchom wszystkie testy
pytest

# Uruchom konkretny plik testowy
pytest tests/test_file.py

# Uruchom z pokryciem
pytest --cov=.
```

### Pisanie Testów

- Pisz testy dla nowych funkcji
- Aktualizuj testy dla poprawek błędów
- Postępuj zgodnie z wzorcem AAA (Arrange, Act, Assert)
- Używaj znaczących nazw testów
- Testuj przypadki brzegowe i warunki błędów

## Dokumentacja

### Dokumentacja Kodu

- Dokumentuj wszystkie publiczne API
- Używaj jasnych, zwięzłych docstringów
- Dołącz przykłady dla złożonych funkcji
- Utrzymuj dokumentację aktualną

### Dokumentacja Użytkownika

- Aktualizuj README.md dla znaczących zmian
- Dokumentuj nowe funkcje
- Aktualizuj dokumentację API
- Dołącz przykłady użycia

## Pytania i Dyskusje

- Używaj GitHub Issues do raportowania błędów i zgłaszania funkcji
- Używaj GitHub Discussions do ogólnych pytań
- Dołącz do naszego czatu społeczności (jeśli dostępny)
- Sprawdź istniejące issue i dyskusje przed utworzeniem nowych

## Dodatkowe Zasoby

- [Przewodnik Deweloperski](DEVELOPMENT.md)
- [Przewodnik Stylu](STYLE_GUIDE.md)
- [Kodeks Postępowania](CODE_OF_CONDUCT.md)
- [Mapa Drogowa Projektu](ROADMAP.md) (jeśli dostępna)

## Uzyskiwanie Pomocy

Jeśli potrzebujesz pomocy lub masz pytania:

1. Sprawdź dokumentację
2. Przeszukaj istniejące issue i dyskusje
3. Utwórz nowe issue lub dyskusję
4. Skontaktuj się z opiekunami pod adresem lukasz.korbasiewicz@gmail.com

Dziękujemy za współtworzenie SubscriptionSage! 