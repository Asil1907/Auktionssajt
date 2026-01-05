# Funktionsbeskrivning - Auktionsapplikation

## Översikt
Detta är en Flask-baserad webbapplikation för att hantera auktioner. Användare kan se, söka och filtrera auktioner, lägga bud samt ge likes/dislikes. Administratörer kan skapa, redigera och ta bort auktioner.

---

## Huvudkomponenter

### 1. **flask_app.py**
Huvudfilen som startar Flask-applikationen.

**Funktioner:**
- Initialiserar Flask-applikationen
- Registrerar blueprints (auctions_bp)
- Initialiserar databasen
- Startar utvecklingsservern när filen körs direkt

---

### 2. **database.py**
Hanterar databasanslutning och initialisering.

**Funktioner:**

#### `get_db()`
- Hämtar eller skapar en databasanslutning
- Sparar anslutningen i Flask's `g`-objekt för att återanvända under samma request
- Konfigurerar `row_factory` för att få tillgång till kolumner via namn

#### `close_db(e=None)`
- Stänger databasanslutningen när requesten är klar
- Kallas automatiskt av Flask efter varje request

#### `init_db(app)`
- Initialiserar databasen när applikationen startar
- Kontrollerar om tabellerna redan finns
- Kör `schema.sql` för att skapa tabeller om de inte finns
- Registrerar `close_db` som teardown-funktion

---

## Repository-klasser

### 3. **AuctionRepository**
Hanterar alla databas-operationer för auktioner.

**Funktioner:**

#### `get_all()`
- Hämtar alla auktioner som inte har gått ut
- Sorterar efter ID i fallande ordning (nyaste först)

#### `get_active()`
- Hämtar endast pågående auktioner
- Sorterar efter sluttid (snarast först)

#### `get_completed_with_bids()`
- Hämtar avslutade auktioner som har minst ett bud
- Sorterar efter sluttid i fallande ordning

#### `get_by_id(auction_id)`
- Hämtar en specifik auktion baserat på ID
- Returnerar ett enda auktionsobjekt

#### `search(keyword)`
- Söker auktioner där titeln innehåller sökordet
- Använder LIKE-operator för partiell matchning
- Visar endast pågående auktioner

#### `create(title, description, starting_bid, end_datetime, category)`
- Skapar en ny auktion i databasen
- Tar emot alla nödvändiga parametrar
- Standardkategori är "Övrigt"

#### `delete(auction_id)`
- Tar bort en auktion från databasen baserat på ID

#### `update(auction_id, title, description, starting_bid, end_datetime, category)`
- Uppdaterar en befintlig auktion med nya värden
- Alla fält kan uppdateras

#### `like(auction_id)`
- Ökar antalet likes för en auktion med 1

#### `dislike(auction_id)`
- Ökar antalet dislikes för en auktion med 1

#### `get_all_categories()`
- Hämtar alla unika kategorier från databasen
- Sorterar kategorierna alfabetiskt
- Används för kategori-dropdown i filtret

#### `filter_auctions(category, min_price, max_price, end_time, show_all)`
- Filtrerar auktioner baserat på flera kriterier:
  - **category**: Filtrerar på kategori
  - **min_price**: Minsta startbud
  - **max_price**: Högsta startbud
  - **end_time**: Auktioner som slutar inom X timmar
  - **show_all**: Visa även avslutade auktioner
- Bygger dynamisk SQL-fråga baserat på aktiva filter

---

### 4. **BidRepository**
Hanterar alla databas-operationer för bud.

**Funktioner:**

#### `create(auction_id, bidder, amount)`
- Skapar ett nytt bud på en auktion
- Sparar budgivarens namn, belopp och tidsstämpel
- Använder ISO-format för datum/tid

#### `get_top_two(auction_id)`
- Hämtar de två högsta buden för en auktion
- Sorterar efter belopp i fallande ordning

#### `count_for_auction(auction_id)`
- Räknar antalet bud på en specifik auktion
- Returnerar ett heltal

#### `get_highest(auction_id)`
- Hämtar det högsta budbeloppet för en auktion
- Returnerar null om inga bud finns

#### `get_all_for_auction(auction_id)`
- Hämtar alla bud för en auktion
- Sorterar efter belopp (högst först) och sedan efter tid

#### `delete(bid_id)`
- Tar bort ett specifikt bud från databasen
- Används av administratörer

---

## Routes (auctions_routes.py)

### 5. **Allmänna Routes**

#### `@auctions_bp.route("/")`  - `index()`
**Huvudsida som visar auktioner**

**Funktionalitet:**
- Tar emot query-parametrar för sökning och filtrering
- Hanterar tre olika visningslägen:
  1. **Sökning**: Om `q` parameter finns, söker efter matchande auktioner
  2. **Filtrering**: Om filter-parametrar finns, filtrerar auktioner
  3. **Standard**: Visar pågående eller alla auktioner beroende på `show_all`
- Hämtar alla kategorier för filter-dropdown
- Renderar `auction_list.html` med alla auktioner och filterinställningar

**Query-parametrar:**
- `q`: Sökord
- `show_all`: Visa alla auktioner (inklusive avslutade)
- `category`: Kategori-filter
- `min_price`: Minimum startbud
- `max_price`: Maximum startbud
- `end_time`: Auktioner som slutar inom X timmar

#### `@auctions_bp.route("/auction/<int:id>")` - `detail(id)`
**Detaljsida för en specifik auktion**

**Funktionalitet:**
- Hämtar auktionsdetaljer
- Hämtar alla bud för auktionen
- Räknar antalet bud
- Hämtar högsta budet
- Renderar `auction_detail.html`

#### `@auctions_bp.route("/auction/<int:id>/bid")` - `bid(id)`
**Lägga bud på en auktion (POST)**

**Funktionalitet:**
- Tar emot budgivare och belopp från formulär
- Skapar nytt bud i databasen
- Visar bekräftelsemeddelande
- Omdirigerar tillbaka till auktionsdetaljsidan

#### `@auctions_bp.route("/auction/<int:id>/like")` - `like(id)`
**Like-funktion för auktion**

**Funktionalitet:**
- Ökar likes-räknaren för auktionen
- Omdirigerar tillbaka till detaljsidan

#### `@auctions_bp.route("/auction/<int:id>/dislike")` - `dislike(id)`
**Dislike-funktion för auktion**

**Funktionalitet:**
- Ökar dislikes-räknaren för auktionen
- Omdirigerar tillbaka till detaljsidan

#### `@auctions_bp.route("/completed")` - `completed()`
**Visa avslutade auktioner**

**Funktionalitet:**
- Hämtar alla avslutade auktioner som har bud
- Renderar `completed_auctions.html`

---

### 6. **Autentisering**

#### `login_required(f)` - Decorator
**Skyddar routes som kräver inloggning**

**Funktionalitet:**
- Kontrollerar om användaren är inloggad via session
- Om inte inloggad: visar meddelande och omdirigerar till login
- Om inloggad: tillåter åtkomst till funktionen

#### `@auctions_bp.route("/login")` - `login()`
**Login-sida för administratörer**

**Funktionalitet:**
- **GET**: Visar login-formulär
- **POST**: 
  - Validerar användarnamn och lösenord
  - Hårdkodat: `admin` / `admin123` (bör flyttas till databas i produktion)
  - Skapar session med användarnamn och inloggningsstatus
  - Omdirigerar till startsidan vid lyckad inloggning

#### `@auctions_bp.route("/logout")` - `logout()`
**Logga ut**

**Funktionalitet:**
- Rensar sessionen
- Visar bekräftelsemeddelande
- Omdirigerar till startsidan

---

### 7. **Admin-funktioner**

#### `@auctions_bp.route("/admin/create")` - `admin_create()`
**Skapa ny auktion (kräver inloggning)**

**Funktionalitet:**
- **GET**: Visar formulär för att skapa auktion
- **POST**: 
  - Tar emot auktionsdata från formulär
  - Skapar ny auktion i databasen
  - Visar bekräftelsemeddelande
  - Omdirigerar till startsidan
- Innehåller fördefinierad lista med kategorier

**Kategorier:**
- Elektronik
- Fordon
- Hem & Trädgård
- Kläder & Accessoarer
- Sport & Fritid
- Samlarprylar
- Övrigt

#### `@auctions_bp.route("/admin/delete/<int:id>")` - `admin_delete(id)`
**Ta bort auktion (kräver inloggning)**

**Funktionalitet:**
- Tar bort auktionen från databasen
- Visar bekräftelsemeddelande
- Omdirigerar till startsidan

#### `@auctions_bp.route("/admin/edit/<int:id>")` - `admin_edit(id)`
**Redigera auktion (kräver inloggning)**

**Funktionalitet:**
- **GET**: 
  - Hämtar befintlig auktion
  - Visar formulär ifyllt med nuvarande värden
- **POST**: 
  - Uppdaterar auktionen med nya värden
  - Visar bekräftelsemeddelande
  - Omdirigerar till auktionsdetaljsidan

#### `@auctions_bp.route("/admin/bid/delete/<int:bid_id>/<int:auction_id>")` - `admin_delete_bid()`
**Ta bort bud (kräver inloggning)**

**Funktionalitet:**
- Tar bort ett specifikt bud
- Visar bekräftelsemeddelande
- Omdirigerar tillbaka till auktionsdetaljsidan

---

## Dataflöde

### Användarscenario 1: Visa auktioner
1. Användare besöker startsidan `/`
2. `index()` anropas
3. Pågående auktioner hämtas via `AuctionRepository.get_active()`
4. Kategorier hämtas för filtret
5. Data skickas till template `auction_list.html`
6. Sidan renderas med auktioner

### Användarscenario 2: Söka auktioner
1. Användare skriver sökord och klickar "Sök"
2. `index()` anropas med query-parameter `q`
3. `AuctionRepository.search(keyword)` körs
4. Matchande auktioner returneras
5. Resultat visas i `auction_list.html`

### Användarscenario 3: Lägga bud
1. Användare fyller i budformulär och skickar
2. POST till `/auction/<id>/bid`
3. `bid(id)` anropas
4. `BidRepository.create()` skapar bud i databasen
5. Flash-meddelande visas
6. Omdirigering till auktionsdetaljsidan

### Admin-scenario: Skapa auktion
1. Admin loggar in via `/login`
2. Session skapas
3. Admin navigerar till `/admin/create`
4. Fyller i formulär och skickar
5. `admin_create()` anropas
6. `AuctionRepository.create()` skapar auktion
7. Omdirigering till startsidan

---

## Säkerhetsaspekter

### Aktuella implementationer:
- **Session-baserad autentisering**: Endast inloggade användare kan skapa/redigera/ta bort auktioner
- **Decorator `@login_required`**: Skyddar admin-routes

### Förbättringsområden:
- **Lösenordshantering**: För närvarande hårdkodat, bör flyttas till databas med hashning
- **SQL Injection**: Skyddad genom parameteriserade frågor
- **CSRF-skydd**: Bör implementeras för formulär
- **XSS-skydd**: Flask's Jinja2 escaper automatiskt HTML

---

## Framtida förbättringar
1. **Användarhantering**: Databas för användare med hashade lösenord
2. **Bildupp ladding**: Stöd för produktbilder
3. **E-postnotifieringar**: Vid nya bud eller när auktion slutar
4. **Realtidsuppdateringar**: WebSocket för live-budgivning
5. **Betalningsintegration**: Hantera betalningar för vunna auktioner
6. **Användarrecensioner**: Betygsättning av säljare och köpare
7. **Budhistorik**: Detaljerad historik över alla bud
8. **Automatisk stängning**: Schemalagd process som stänger avslutade auktioner

---

## Teknisk stack
- **Backend**: Flask (Python)
- **Databas**: SQLite
- **Frontend**: Jinja2 templates, HTML, CSS
- **Session-hantering**: Flask sessions med secret key

---

**Dokumentet skapad**: 2026-01-05
**Version**: 1.0
