# Průvodce Stylu SubscriptionSage

Tento dokument popisuje standardy kódování a nejlepší postupy pro projekt SubscriptionSage.

## Styl Kódu Python

### Obecná Pravidla

- Dodržujte průvodce stylem [PEP 8](https://peps.python.org/pep-0008/)
- Používejte 4 mezery pro odsazení (bez tabulátorů)
- Maximální délka řádku: 88 znaků (výchozí nastavení formátovače Black)
- Používejte smysluplné názvy proměnných a funkcí
- Pište docstringy pro všechny veřejné funkce, třídy a moduly

### Konvence Pojmenování

- **Proměnné a Funkce**: Používejte `snake_case`
  ```python
  def calculate_total_cost():
      subscription_price = 9.99
  ```

- **Třídy**: Používejte `PascalCase`
  ```python
  class SubscriptionManager:
      pass
  ```

- **Konstanty**: Používejte `UPPER_SNAKE_CASE`
  ```python
  MAX_RETRY_ATTEMPTS = 3
  DEFAULT_CURRENCY = "USD"
  ```

### Importy

- Seskupujte importy v následujícím pořadí:
  1. Importy ze standardní knihovny
  2. Importy třetích stran
  3. Místní importy aplikace
- Řaďte importy abecedně v rámci skupin
- Používejte absolutní importy

```python
# Standardní knihovna
import datetime
import os
from typing import List, Optional

# Třetí strany
from flask import Flask, request
from sqlalchemy import Column, Integer

# Místní
from models import User
from utils import format_currency
```

### Typové Anotace

- Používejte typové anotace pro parametry funkcí a návratové hodnoty
- Používejte `Optional` pro parametry, které mohou být `None`
- Používejte `List`, `Dict` atd. z modulu `typing`

```python
from typing import List, Optional

def get_user_subscriptions(user_id: int) -> List[Subscription]:
    pass

def update_subscription(sub_id: int, price: Optional[float] = None) -> bool:
    pass
```

## Pokyny Specifické pro Flask

### Organizace Routů

- Seskupujte související routy dohromady
- Používejte popisné názvy rout
- Dodržujte RESTful konvence kde je to vhodné

```python
# Dobře
@app.route('/subscriptions', methods=['GET'])
def list_subscriptions():
    pass

@app.route('/subscriptions/<int:sub_id>', methods=['GET'])
def get_subscription(sub_id):
    pass

# Vyhněte se
@app.route('/get_sub', methods=['GET'])
def get_sub():
    pass
```

### Organizace Šablon

- Uchovávejte šablony v adresáři `templates/`
- Používejte dědičnost šablon se základními šablonami
- Pojmenovávejte soubory šablon ve formátu `snake_case.html`
- Používejte smysluplné názvy bloků

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

{% block title %}Moje Předplatné{% endblock %}

{% block content %}
    <!-- Obsah zde -->
{% endblock %}
```

## Modely SQLAlchemy

### Organizace Modelů

- Jeden model na soubor v adresáři `models/`
- Používejte popisné názvy modelů
- Zahrňte vhodné vztahy a omezení

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

### Obecná Pravidla

- Používejte funkce ES6+
- Používejte smysluplné názvy proměnných a funkcí
- Používejte `const` a `let` místo `var`
- Používejte šipkové funkce pro callbacky

```javascript
// Dobře
const calculateTotal = (subscriptions) => {
    return subscriptions.reduce((sum, sub) => sum + sub.price, 0);
};

// Vyhněte se
var total = 0;
for (var i = 0; i < subs.length; i++) {
    total += subs[i].price;
}
```

### Obsluhovače Událostí

- Používejte popisné názvy obsluhovačů
- Udržujte obsluhovače zaměřené a malé
- Používejte delegaci událostí kde je to vhodné

```javascript
// Dobře
document.querySelector('.subscription-list').addEventListener('click', (e) => {
    if (e.target.matches('.delete-btn')) {
        handleDelete(e.target.dataset.id);
    }
});
```

## Styl CSS

### Organizace

- Používejte konvenci pojmenování BEM (Block Element Modifier)
- Seskupujte související styly dohromady
- Používejte CSS proměnné pro běžné hodnoty

```css
/* Dobře */
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

## Git Pracovní Postup

### Pojmenování Větví

- Větve funkcí: `feature/popis`
- Opravy chyb: `fix/popis`
- Dokumentace: `docs/popis`
- Hotfixy: `hotfix/popis`

### Zprávy Commitů

- Používejte přítomný čas
- Začněte slovesem
- Udržujte první řádek pod 50 znaky
- Používejte tělo pro podrobné vysvětlení

```
feat: přidej funkcionalitu importu předplatného

- Přidej podporu pro import CSV
- Validuj importovaná data
- Zpracuj duplicitní záznamy
```

## Testování

### Organizace Testů

- Jeden testovací soubor na modul
- Pojmenovávejte testovací soubory s předponou `test_`
- Používejte popisné názvy testů
- Dodržujte vzor AAA (Arrange, Act, Assert)

```python
def test_calculate_monthly_total():
    # Arrange
    subscriptions = [
        Subscription(price=10.0),
        Subscription(price=15.0)
    ]
``` 