# Užitečné Funkce

Tento dokument popisuje užitečné funkce dostupné v aplikaci SubscriptionSage.

## Směnné Kurzy

Aplikace používá Exchange Rate API pro získávání a aktualizaci směnných kurzů. Kurzy jsou uloženy v databázi a aktualizovány denně.

### Nastavení

1. Zaregistrujte se pro získání bezplatného API klíče na [exchangerate-api.com](https://www.exchangerate-api.com/)
2. Přejděte na stránku Reporty v aplikaci
3. Klikněte na "Spravovat API klíč" a zadejte svůj API klíč
4. Směnné kurzy budou automaticky aktualizovány

### Funkce

- `fetch_exchange_rates()`: Získá nejnovější směnné kurzy z API a aktualizuje databázi
- `convert_currency(amount, from_currency, to_currency)`: Převede částku z jedné měny na druhou
- `format_currency(amount, currency)`: Formátuje částku s příslušným symbolem měny

## Správa Měn

### `fetch_exchange_rates()`

Získá nejnovější směnné kurzy z externího API a aktualizuje databázi.

- **Podporované Měny**: USD, EUR, CZK, PLN
- **API**: Používá [Exchange Rate API](https://www.exchangerate-api.com/) (bezplatná verze)
- **Záložní**: Přidá výchozí kurzy, pokud se získání z API nezdaří
- **Použití**: Voláno plánovačem pro udržení aktuálních kurzů

### `add_default_exchange_rates()`

Přidá výchozí směnné kurzy do databáze, pokud se získání z API nezdaří.

- **Výchozí Kurzy**: Předkonfigurované kurzy pro všechny podporované měnové páry
- **Použití**: Interní funkce, volaná `fetch_exchange_rates()`

### `convert_currency(amount, from_currency, to_currency)`

Převede částku z jedné měny na druhou.

- **Parametry**:
  - `amount`: Částka k převodu
  - `from_currency`: Zdrojový měnový kód
  - `to_currency`: Cílový měnový kód
- **Vrací**: Převedenou částku
- **Záložní**: Vrací původní částku, pokud převod není možný

### `format_currency(amount, currency)`

Formátuje částku s příslušným symbolem měny.

- **Parametry**:
  - `amount`: Částka k formátování
  - `currency`: Měnový kód
- **Vrací**: Formátovaný řetězec se symbolem měny
- **Podporované Měny**: USD ($), EUR (€), CZK (Kč), PLN (zł)

## Systém Připomínek

Aplikace může posílat e-mailové připomínky pro nadcházející platby předplatného. Každé předplatné může mít nakonfigurováno až 3 připomínky.

### Nastavení

1. Nakonfigurujte nastavení e-mailu v souboru `.env`:
   ```
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password_here
   ```

### Funkce

- `check_upcoming_reminders()`: Kontroluje nadcházející platby a posílá připomínky
- `send_reminder_email(user, subscription, days_until_payment)`: Posílá e-mailovou připomínku
- `reset_reminders_for_next_period()`: Resetuje připomínky pro další fakturační období

### Limity Připomínek

- Maximálně 3 připomínky na předplatné
- Každá připomínka může být nakonfigurována pro:
  - Dny před platbou (1-30 dní)
  - Typ notifikace (e-mail a/nebo push)
- Připomínky jsou automaticky deaktivovány pro doživotní předplatné

## Správa Plateb

### `mark_subscription_paid(subscription_id)`

Označí platbu předplatného jako dokončenou a aktualizuje datum další platby.

- **Parametry**:
  - `subscription_id`: ID předplatného
- **Vrací**: Aktualizované datum další platby
- **Akce**:
  - Aktualizuje datum další platby na základě fakturačního cyklu
  - Resetuje připomínky pro další období
  - Správně zpracovává doživotní předplatné

### Použití

```python
# Označ předplatné jako zaplacené
next_payment_date = mark_subscription_paid(subscription_id)
```

## Správa Služeb

### `get_logo_url_for_service(service_name, url=None)`

Získá URL loga pro konkrétní službu.

- **Parametry**:
  - `service_name`: Název služby
  - `url`: Volitelná URL webové stránky pro záložní favicon
- **Vrací**: URL k logu služby
- **Záložní**: Pokusí se získat favicon, pokud není nalezeno logo

### `update_subscription_logos()`

Aktualizuje loga pro všechna předplatná.

- **Použití**: Údržbová funkce
- **Akce**: Aktualizuje loga pro všechna aktivní předplatná

### `handle_image_upload(file, subscription_id)`

Zpracovává vlastní nahrávání log pro předplatná.

- **Parametry**:
  - `file`: Nahrávaný soubor
  - `subscription_id`: ID předplatného
- **Vrací**: Cestu k uloženému obrázku
- **Bezpečnost**: Ověřuje typ a velikost souboru

## Příklady Použití

### Převod Měn

```python
# Převeď 100 USD na EUR
amount_eur = convert_currency(100, 'USD', 'EUR')

# Formátuj výsledek
formatted_amount = format_currency(amount_eur, 'EUR')
```

### Systém Připomínek

```python
# Zkontroluj nadcházející připomínky
check_upcoming_reminders()

# Resetuj připomínky po obnovení
reset_reminders_for_next_period()
```

### Správa Log Služeb

```python
# Získej logo pro službu
logo_url = get_logo_url_for_service('netflix')

# Aktualizuj všechna loga předplatných
update_subscription_logos()
```

## Závislosti

- Flask-Mail pro e-mailovou funkcionalitu
- Requests pro API volání
- SQLAlchemy pro databázové operace
- Logging pro sledování chyb

## Zpracování Chyb

Všechny užitečné funkce zahrnují:
- Správné logování chyb
- Elegantní záložní řešení
- Zpracování výjimek
- Validaci vstupních dat

## Konfigurace

### Konfigurace Exchange Rate API

Aplikace používá Exchange Rate API pro převod měn. Pro nastavení API:

1. **Získej API Klíč**:
   - Navštivte [Exchange Rate API](https://www.exchangerate-api.com/)
   - Zaregistrujte se pro bezplatný účet
   - Přejděte do svého dashboardu
   - Zkopírujte svůj API klíč

2. **Nakonfiguruj API Klíč**:
   - Přidejte klíč do souboru `.env`:
     ```
     EXCHANGE_RATE_API_KEY=your_api_key_here
     ```
   - Nebo ho nastavte v `docker-compose.yml` pro vývoj:
     ```yaml
     environment:
       - EXCHANGE_RATE_API_KEY=your_api_key_here
     ```

3. **Limity API**:
   - Bezplatná verze: 1,500 požadavků měsíčně
   - Aktualizace kurzů: Každých 24 hodin
   - Podporované měny: USD, EUR, CZK, PLN

4. **Záložní Chování**:
   - Pokud je API nedostupné, použijí se výchozí kurzy
   - Výchozí kurzy jsou aktualizovány ručně podle potřeby
   - Aplikace pokračuje v činnosti s posledními známými kurzy

### Konfigurace E-mailu

Viz [Vývojový Průvodce](DEVELOPMENT.md) pro podrobnosti konfigurace e-mailu. 