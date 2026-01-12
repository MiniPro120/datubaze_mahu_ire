Cipherots parole masinuire123

Auto nomas datubāzes lietotne
Apraksts

Šis projekts ir vienkārša auto nomas datubāzes lietotne. Lietotne ļauj uzglabāt un apstrādāt informāciju par klientiem, automašīnām, īrēm un papildaprīkojumu, izmantojot SQLite datubāzi un Python programmēšanas valodu.

Projekta mērķis ir parādīt datubāzes projektēšanas pamatus, Entītiju–Relāciju (ER) modeļa izveidi un CRUD (Create, Read, Update, Delete) darbību realizāciju.

Izmantotās tehnoloģijas

Python 3

SQLite

DB Browser (SQLite) – datubāzes izveidei un pārbaudei

diagrams.net (Draw.io) – ER diagrammas izveidei

Sistēmas funkcionalitāte

Lietotne nodrošina šādas iespējas:

pievienot klientus, automašīnas, īres un papildaprīkojumu;

apskatīt datubāzes datus atsevišķās tabulās un apvienotā skatā (JOIN);

labot esošos ierakstus;

dzēst ierakstus no datubāzes.

Datu bāzes struktūra
Tabulas

Klients – informācija par klientiem (vārds, telefons, e-pasts);

Auto – informācija par automašīnām (marka, modelis, numurzīme, cena dienā, statuss);

Īre – informācija par auto īri (klients, auto, īres datumi, kopējā cena);

Papildaprīkojums – papildpakalpojumi (piemēram, GPS, bērnu sēdeklis);

ĪrePapild – savienojuma tabula starp īri un papildaprīkojumu.

Relācijas

Klients – Īre (1:N)
Viens klients var veikt vairākas īres.

Auto – Īre (1:N)
Vienu automašīnu var iznomāt vairākas reizes dažādos laika periodos.

Īre – Papildaprīkojums (M:N)
Vienai īrei var pievienot vairākus papildaprīkojuma veidus. Šī relācija realizēta ar tabulu ĪrePapild.

Lietotnes palaišana

Pārliecinies, ka datorā ir uzstādīts Python 3.

Lejupielādē projekta failus (Python skriptu un SQL failu).

Atver termināli projekta mapē.

Palaid lietotni ar komandu:

python auto_noma_app.py


Konsolē parādīsies izvēlne, kurā var veikt CRUD darbības.

CRUD darbības

Create – jaunu ierakstu pievienošana visās tabulās;

Read – datu attēlošana no datubāzes (arī ar JOIN vaicājumiem);

Update – esošo ierakstu labošana;

Delete – ierakstu dzēšana no datubāzes.

Secinājums

Auto nomas datubāzes lietotne demonstrē, kā ar relāciju datubāzi un Python iespējams izveidot vienkāršu, bet funkcionālu informācijas sistēmu. Projekts palīdz apgūt datubāzes struktūras plānošanu, relāciju veidošanu un datu apstrādi programmēšanas valodā.
