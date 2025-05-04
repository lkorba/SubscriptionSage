# Funkcje Użytkowe

Ten dokument opisuje funkcje użytkowe dostępne w aplikacji SubscriptionSage.

## Kursy Wymiany

Aplikacja używa Exchange Rate API do pobierania i aktualizacji kursów wymiany. Kursy są przechowywane w bazie danych i aktualizowane codziennie.

### Konfiguracja

1. Zarejestruj się, aby otrzymać darmowy klucz API na [exchangerate-api.com](https://www.exchangerate-api.com/)
2. Przejdź do strony Raporty w aplikacji
3. Kliknij "Zarządzaj kluczem API" i wprowadź swój klucz API
4. Kursy wymiany będą automatycznie aktualizowane

### Funkcje

- `fetch_exchange_rates()`: Pobiera najnowsze kursy wymiany z API i aktualizuje bazę danych
- `convert_currency(amount, from_currency, to_currency)`: Konwertuje kwotę z jednej waluty na drugą
- `format_currency(amount, currency)`: Formatuje kwotę z odpowiednim symbolem waluty

## Zarządzanie Walutami

### `fetch_exchange_rates()`

Pobiera najnowsze kursy wymiany z zewnętrznego API i aktualizuje bazę danych.

- **Obsługiwane Waluty**: USD, EUR, CZK, PLN
- **API**: Używa [Exchange Rate API](https://www.exchangerate-api.com/) (darmowa wersja)
- **Awaryjne**: Dodaje domyślne kursy, jeśli pobieranie z API nie powiedzie się
- **Użycie**: Wywoływane przez harmonogram, aby utrzymać kursy aktualne

### `add_default_exchange_rates()`

Dodaje domyślne kursy wymiany do bazy danych, jeśli pobieranie z API nie powiedzie się.

- **Domyślne Kursy**: Wstępnie skonfigurowane kursy dla wszystkich obsługiwanych par walut
- **Użycie**: Funkcja wewnętrzna, wywoływana przez `fetch_exchange_rates()`

### `convert_currency(amount, from_currency, to_currency)`

Konwertuje kwotę z jednej waluty na drugą.

- **Parametry**:
  - `amount`: Kwota do konwersji
  - `from_currency`: Kod waluty źródłowej
  - `to_currency`: Kod waluty docelowej
- **Zwraca**: Skonwertowaną kwotę
- **Awaryjne**: Zwraca oryginalną kwotę, jeśli konwersja nie jest możliwa

### `format_currency(amount, currency)`

Formatuje kwotę z odpowiednim symbolem waluty.

- **Parametry**:
  - `amount`: Kwota do sformatowania
  - `currency`: Kod waluty
- **Zwraca**: Sformatowany ciąg znaków ze symbolem waluty
- **Obsługiwane Waluty**: USD ($), EUR (€), CZK (Kč), PLN (zł)

## System Przypomnień

Aplikacja może wysyłać przypomnienia e-mail o nadchodzących płatnościach za subskrypcje. Każda subskrypcja może mieć skonfigurowane do 3 przypomnień.

### Konfiguracja

1. Skonfiguruj ustawienia e-mail w pliku `.env`:
   ```
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password_here
   ```

### Funkcje

- `check_upcoming_reminders()`: Sprawdza nadchodzące płatności i wysyła przypomnienia
- `send_reminder_email(user, subscription, days_until_payment)`: Wysyła przypomnienie e-mail
- `reset_reminders_for_next_period()`: Resetuje przypomnienia dla następnego okresu rozliczeniowego

### Limity Przypomnień

- Maksymalnie 3 przypomnienia na subskrypcję
- Każde przypomnienie można skonfigurować dla:
  - Dni przed płatnością (1-30 dni)
  - Typu powiadomienia (e-mail i/lub push)
- Przypomnienia są automatycznie wyłączane dla subskrypcji dożywotnich

## Zarządzanie Płatnościami

### `mark_subscription_paid(subscription_id)`

Oznacza płatność za subskrypcję jako zakończoną i aktualizuje datę następnej płatności.

- **Parametry**:
  - `subscription_id`: ID subskrypcji
- **Zwraca**: Zaktualizowaną datę następnej płatności
- **Akcje**:
  - Aktualizuje datę następnej płatności na podstawie cyklu rozliczeniowego
  - Resetuje przypomnienia dla następnego okresu
  - Odpowiednio obsługuje subskrypcje dożywotnie

### Użycie

```python
# Oznacz subskrypcję jako opłaconą
next_payment_date = mark_subscription_paid(subscription_id)
```

## Zarządzanie Usługami

### `get_logo_url_for_service(service_name, url=None)`

Pobiera URL logo dla konkretnej usługi.

- **Parametry**:
  - `service_name`: Nazwa usługi
  - `url`: Opcjonalny URL strony internetowej dla awaryjnego favicon
- **Zwraca**: URL do logo usługi
- **Awaryjne**: Próbuje pobrać favicon, jeśli nie znaleziono logo

### `update_subscription_logos()`

Aktualizuje logo dla wszystkich subskrypcji.

- **Użycie**: Funkcja konserwacyjna
- **Akcje**: Aktualizuje logo dla wszystkich aktywnych subskrypcji

### `handle_image_upload(file, subscription_id)`

Obsługuje niestandardowe przesyłanie logo dla subskrypcji.

- **Parametry**:
  - `file`: Przesłany obiekt pliku
  - `subscription_id`: ID subskrypcji
- **Zwraca**: Ścieżkę do zapisanego obrazu
- **Bezpieczeństwo**: Weryfikuje typ i rozmiar pliku

## Przykłady Użycia

### Konwersja Walut

```python
# Konwertuj 100 USD na EUR
amount_eur = convert_currency(100, 'USD', 'EUR')

# Formatuj wynik
formatted_amount = format_currency(amount_eur, 'EUR')
```

### System Przypomnień

```python
# Sprawdź nadchodzące przypomnienia
check_upcoming_reminders()

# Resetuj przypomnienia po odnowieniu
reset_reminders_for_next_period()
```

### Zarządzanie Logo Usług

```python
# Pobierz logo dla usługi
logo_url = get_logo_url_for_service('netflix')

# Aktualizuj wszystkie logo subskrypcji
update_subscription_logos()
```

## Zależności

- Flask-Mail dla funkcjonalności e-mail
- Requests dla wywołań API
- SQLAlchemy dla operacji bazodanowych
- Logging dla śledzenia błędów

## Obsługa Błędów

Wszystkie funkcje użytkowe zawierają:
- Odpowiednie logowanie błędów
- Eleganckie rozwiązania awaryjne
- Obsługę wyjątków
- Walidację danych wejściowych

## Konfiguracja

### Konfiguracja Exchange Rate API

Aplikacja używa Exchange Rate API do konwersji walut. Aby skonfigurować API:

1. **Uzyskaj Klucz API**:
   - Odwiedź [Exchange Rate API](https://www.exchangerate-api.com/)
   - Zarejestruj się za darmowe konto
   - Przejdź do swojego panelu
   - Skopiuj swój klucz API

2. **Skonfiguruj Klucz API**:
   - Dodaj klucz do pliku `.env`:
     ```
     EXCHANGE_RATE_API_KEY=your_api_key_here
     ```
   - Lub ustaw go w `docker-compose.yml` dla rozwoju:
     ```yaml
     environment:
       - EXCHANGE_RATE_API_KEY=your_api_key_here
     ```

3. **Limity API**:
   - Darmowa wersja: 1,500 zapytań miesięcznie
   - Aktualizacje kursów: Co 24 godziny
   - Obsługiwane waluty: USD, EUR, CZK, PLN

4. **Zachowanie Awaryjne**:
   - Jeśli API jest niedostępne, używane są domyślne kursy
   - Domyślne kursy są aktualizowane ręcznie w razie potrzeby
   - Aplikacja kontynuuje działanie z ostatnimi znanymi kursami

### Konfiguracja E-mail

Zobacz [Przewodnik Deweloperski](DEVELOPMENT.md) dla szczegółów konfiguracji e-mail. 