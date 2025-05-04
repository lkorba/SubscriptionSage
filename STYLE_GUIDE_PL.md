# Przewodnik Stylu SubscriptionSage

Ten dokument przedstawia standardy kodowania i najlepsze praktyki dla projektu SubscriptionSage.

## Styl Kodu Python

### Ogólne Zasady

- Przestrzegaj przewodnika stylu [PEP 8](https://peps.python.org/pep-0008/)
- Używaj 4 spacji do wcięć (bez tabulatorów)
- Maksymalna długość linii: 88 znaków (domyślne ustawienie formatera Black)
- Używaj znaczących nazw zmiennych i funkcji
- Pisz docstringi dla wszystkich publicznych funkcji, klas i modułów

### Konwencje Nazewnictwa

- **Zmienne i Funkcje**: Używaj `snake_case`
  ```python
  def calculate_total_cost():
      subscription_price = 9.99
  ```

- **Klasy**: Używaj `PascalCase`
  ```python
  class SubscriptionManager:
      pass
  ```

- **Stałe**: Używaj `UPPER_SNAKE_CASE`
  ```python
  MAX_RETRY_ATTEMPTS = 3
  DEFAULT_CURRENCY = "USD"
  ```

### Importy

- Grupuj importy w następującej kolejności:
  1. Importy z biblioteki standardowej
  2. Importy z bibliotek zewnętrznych
  3. Importy lokalne z aplikacji
- Sortuj importy alfabetycznie w ramach grup
- Używaj importów absolutnych

```python
# Biblioteka standardowa
import datetime
import os
from typing import List, Optional

# Biblioteki zewnętrzne
from flask import Flask, request
from sqlalchemy import Column, Integer

# Lokalne
from models import User
from utils import format_currency
```

### Adnotacje Typów

- Używaj adnotacji typów dla parametrów funkcji i wartości zwracanych
- Używaj `Optional` dla parametrów, które mogą być `None`
- Używaj `List`, `Dict` itp. z modułu `typing`

```python
from typing import List, Optional

def get_user_subscriptions(user_id: int) -> List[Subscription]:
    pass

def update_subscription(sub_id: int, price: Optional[float] = None) -> bool:
    pass
```

## Wytyczne Specyficzne dla Flask

### Organizacja Tras

- Grupuj powiązane trasy razem
- Używaj opisowych nazw tras
- Przestrzegaj konwencji RESTful gdzie to odpowiednie

```python
# Dobrze
@app.route('/subscriptions', methods=['GET'])
def list_subscriptions():
    pass

@app.route('/subscriptions/<int:sub_id>', methods=['GET'])
def get_subscription(sub_id):
    pass

# Unikaj
@app.route('/get_sub', methods=['GET'])
def get_sub():
    pass
```

### Organizacja Szablonów

- Przechowuj szablony w katalogu `templates/`
- Używaj dziedziczenia szablonów z szablonami bazowymi
- Nazywaj pliki szablonów w formacie `snake_case.html`
- Używaj znaczących nazw bloków

```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

<!-- subscription_list.html -->
{% extends "base.html" %}

{% block title %}Moje Subskrypcje{% endblock %}

{% block content %}
    <!-- Treść tutaj -->
{% endblock %}
```

## Modele SQLAlchemy

### Organizacja Modeli

- Jeden model na plik w katalogu `models/`
- Używaj opisowych nazw modeli
- Uwzględniaj odpowiednie relacje i ograniczenia

```python
class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='subscriptions')
```

## Styl JavaScript

### Ogólne Zasady

- Używaj funkcji ES6+
- Używaj znaczących nazw zmiennych i funkcji
- Używaj `const` i `let` zamiast `var`
- Używaj funkcji strzałkowych dla callbacków

```javascript
// Dobrze
const calculateTotal = (subscriptions) => {
    return subscriptions.reduce((sum, sub) => sum + sub.price, 0);
};

// Unikaj
var total = 0;
for (var i = 0; i < subs.length; i++) {
    total += subs[i].price;
}
```

### Obsługiwacze Zdarzeń

- Używaj opisowych nazw obsługiwaczy
- Utrzymuj obsługiwacze skoncentrowane i małe
- Używaj delegacji zdarzeń gdzie to odpowiednie

```javascript
// Dobrze
document.querySelector('.subscription-list').addEventListener('click', (e) => {
    if (e.target.matches('.delete-btn')) {
        handleDelete(e.target.dataset.id);
    }
});
```

## Styl CSS

### Organizacja

- Używaj konwencji nazewnictwa BEM (Block Element Modifier)
- Grupuj powiązane style razem
- Używaj zmiennych CSS dla wspólnych wartości

```css
/* Dobrze */
.subscription-card {
    padding: 1rem;
    border-radius: 4px;
}

.subscription-card__title {
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
}

.subscription-card--active {
    border: 2px solid var(--color-success);
}
```

## Przepływ Pracy w Git

### Nazewnictwo Gałęzi

- Gałęzie funkcji: `feature/opis`
- Naprawy błędów: `fix/opis`
- Dokumentacja: `docs/opis`
- Hotfixy: `hotfix/opis`

### Wiadomości Commitów

- Używaj czasu teraźniejszego
- Zacznij od czasownika
- Utrzymuj pierwszą linię poniżej 50 znaków
- Używaj treści dla szczegółowego wyjaśnienia

```
feat: dodaj funkcjonalność importu subskrypcji

- Dodaj wsparcie dla importu CSV
- Waliduj zaimportowane dane
- Obsługuj zduplikowane wpisy
```

## Testowanie

### Organizacja Testów

- Jeden plik testowy na moduł
- Nazywaj pliki testowe z przedrostkiem `test_`
- Używaj opisowych nazw testów
- Przestrzegaj wzorca AAA (Arrange, Act, Assert)

```python
def test_calculate_monthly_total():
    # Arrange
    subscriptions = [
        Subscription(price=10.0),
        Subscription(price=15.0)
    ]
``` 