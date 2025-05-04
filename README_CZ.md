# SubscriptionSage

SubscriptionSage je webová aplikace, která pomáhá uživatelům sledovat a spravovat jejich předplatné na jednom centralizovaném místě.

![Logo SubscriptionSage](https://example.com/logo.png)

## Přehled

V dnešní digitální ekonomice lidé často odebírají mnoho služeb na různých platformách, což ztěžuje sledování všech aktivních předplatných, fakturačních cyklů a nadcházejících plateb. SubscriptionSage tento problém řeší tím, že poskytuje jednotný dashboard, kde mohou uživatelé spravovat všechny své předplatné služby.

## Funkce

- **Sledování předplatného**: Snadné přidávání, úprava a mazání předplatných služeb
- **Přehled dashboardu**: Rychlý přehled aktivních předplatných, měsíčních výdajů a nadcházejících plateb
- **Systém připomínek**: Nastavte až 3 e-mailová upozornění na nadcházející obnovení předplatného
- **Správa plateb**: Označte platby jako dokončené a automaticky aktualizujte data dalších plateb
- **Podpora více měn**: Sledujte předplatné v různých měnách s automatickou konverzí na preferovanou měnu
- **Správa fakturačního cyklu**: Podpora týdenních, měsíčních, čtvrtletních, pololetních, ročních a doživotních předplatných
- **Analýza dat**: Vizualizujte vzorce výdajů na předplatné
- **Import/Export**: Importujte a exportujte data předplatného jako CSV soubory
- **Uživatelské profily**: Personalizovaná nastavení s jazykovými a měnovými preferencemi

## Technologický stack

- **Backend**: Flask (Python 3.11)
- **Databáze**: PostgreSQL 16 s SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript
- **Autentizace**: Flask-Login
- **E-mailová upozornění**: Flask-Mail
- **Úlohy na pozadí**: APScheduler
- **Vývoj**: Docker & Dev Containers

## Rychlý start

1. Naklonujte repozitář
2. Otevřete ve VS Code s rozšířením Dev Containers
3. Vytvořte soubor `.env` s nastavením e-mailu (viz [Vývojový průvodce](DEVELOPMENT.md))
4. Aplikace bude dostupná na http://localhost:5000

Podrobné instrukce k nastavení naleznete ve [Vývojovém průvodci](DEVELOPMENT.md).

## Použití

1. **Registrace/Přihlášení**: Vytvořte účet nebo se přihlaste
2. **Přidání předplatného**: Zadejte podrobnosti o předplatných službách
3. **Nastavení připomínek**: Nakonfigurujte, kdy chcete dostávat upozornění na nadcházející platby
4. **Monitorování dashboardu**: Sledujte výdaje a nadcházející obnovení
5. **Správa předplatného**: Aktualizujte nebo zrušte předplatné podle potřeby

## Screenshoty

[Screenshoty budou přidány zde]

## Přispívání

Příspěvky jsou vítány! Neváhejte zaslat Pull Request. Instrukce k vývojovému nastavení naleznete ve [Vývojovém průvodci](DEVELOPMENT.md).

## Licence

Tento projekt je licencován pod MIT licencí - podrobnosti naleznete v souboru [LICENSE](LICENSE).

## Kontakt

Pro podporu nebo dotazy, prosím [kontaktujte mě](mailto:lukasz.korbasiewicz@gmail.com).

---

SubscriptionSage - Převzít kontrolu nad svými digitálními předplatnými 