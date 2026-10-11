from typing import List, Dict, Any

SAMPLE_BOOKS: List[Dict[str, Any]] = [
    # 1. Sci-Fi & Kyberpunk
    {
        "isbn": "9788025725658",
        "title": "Duna",
        "author": "Frank Herbert",
        "genres": ["Sci-Fi", "Literatura světová", "Vesmír"],
        "description": "Kultovní román vědecko-fantastické literatury z pouštní planety Arrakis.",
        "cover_url": "https://www.databazeknih.cz/img/books/40_/408543/duna-F90-408543.jpg",
        "publisher": "Baronet",
        "year": 2021,
        "shelf_id": 1,
        "rating": 4.9
    },
    {
        "isbn": "9788025700778",
        "title": "Nadace",
        "author": "Isaac Asimov",
        "genres": ["Sci-Fi", "Literatura světová"],
        "description": "První kniha slavné galaktické ságy o psychohistorii Hariho Seldona.",
        "cover_url": "https://www.databazeknih.cz/img/books/16_/16674/nadace-nadace-16674.jpg",
        "publisher": "Triton",
        "year": 2009,
        "shelf_id": 1,
        "rating": 4.8
    },
    {
        "isbn": "9788025729786",
        "title": "Neuromancer",
        "author": "William Gibson",
        "genres": ["Sci-Fi", "Kyberpunk"],
        "description": "Základní kámen žánru cyberpunk – kyberprostor, hackeři a umělá inteligence.",
        "cover_url": "https://www.databazeknih.cz/img/books/39_/398867/neuromancer-0vS-398867.jpg",
        "publisher": "Laser",
        "year": 2019,
        "shelf_id": 1,
        "rating": 4.5
    },

    # 2. Fantasy & Mytologie
    {
        "isbn": "9788025732106",
        "title": "Pán prstenů: Společenstvo Prstenu",
        "author": "J. R. R. Tolkien",
        "genres": ["Fantasy", "Epická fantasy"],
        "description": "Jeden prsten vládne všem, Jeden jim všem káže. Putování Froda Pytlíka začíná.",
        "cover_url": "https://www.databazeknih.cz/img/books/29_/29859/spolecenstvo-prstenu-29859.jpg",
        "publisher": "Argo",
        "year": 2020,
        "shelf_id": 2,
        "rating": 5.0
    },
    {
        "isbn": "9788085951653",
        "title": "Zaklínač: Poslední přání",
        "author": "Andrzej Sapkowski",
        "genres": ["Fantasy", "Povídky"],
        "description": "První sbírka povídek o Geraltovi z Rivie, mutantovi a profesionálním lovci netvorů.",
        "cover_url": "https://www.databazeknih.cz/img/books/28_/28045/posledni-prani-28045.jpg",
        "publisher": "Leonardo",
        "year": 2011,
        "shelf_id": 2,
        "rating": 4.9
    },
    {
        "isbn": "9788000061917",
        "title": "Harry Potter a Kámen mudrců",
        "author": "J. K. Rowling",
        "genres": ["Fantasy", "Pro děti a mládež"],
        "description": "Až do svých jedenáctých narozenin si o sobě Harry myslel, že je jen obyčejný chlapec.",
        "cover_url": "https://www.databazeknih.cz/img/books/47_/470622/bmid_harry-potter-a-kamen-mudrcu-wxC-470622.jpg",
        "publisher": "Albatros",
        "year": 2021,
        "shelf_id": 2,
        "rating": 4.8
    },

    # 3. Detektivky & Thrillery
    {
        "isbn": "9788024263151",
        "title": "Deset malých černoušků",
        "author": "Agatha Christie",
        "genres": ["Detektivky", "Krimi"],
        "description": "Deset lidí pozvaných na opuštěný ostrov. Jeden po druhém umírají podle dětské říkanky.",
        "cover_url": "https://www.databazeknih.cz/img/books/39_/394236/deset-malych-cernousku-c3B-394236.jpg",
        "publisher": "Knižní klub",
        "year": 2019,
        "shelf_id": 3,
        "rating": 4.9
    },
    {
        "isbn": "9788075775870",
        "title": "Sněhulák",
        "author": "Jo Nesbø",
        "genres": ["Krimi", "Thriller", "Severské krimi"],
        "description": "Harry Hole pátrá po sériovém vrahovi žen v zasněženém Oslu.",
        "cover_url": "https://www.databazeknih.cz/img/books/38_/384664/snehulak-rR0-384664.jpg",
        "publisher": "Kniha Zlín",
        "year": 2018,
        "shelf_id": 3,
        "rating": 4.7
    },
    {
        "isbn": "9788075850935",
        "title": "Dívka v ledu",
        "author": "Robert Bryndza",
        "genres": ["Detektivky", "Krimi"],
        "description": "První případ šéfinspektorky Eriky Fosterové v mrazivém Londýně.",
        "cover_url": "https://www.databazeknih.cz/img/books/30_/302787/divka-v-ledu-aJc-302787.jpg",
        "publisher": "Cosmopolis",
        "year": 2016,
        "shelf_id": 3,
        "rating": 4.6
    },

    # 4. Horory & Mystika
    {
        "isbn": "9788073069124",
        "title": "To",
        "author": "Stephen King",
        "genres": ["Horor", "Thriller"],
        "description": "Městečko Derry v Maine sužuje pradávné monstrum v podobě tančícího klauna Pennywise.",
        "cover_url": "https://www.databazeknih.cz/img/books/33_/332824/to-Q90-332824.jpg",
        "publisher": "Beta-Dobrovský",
        "year": 2017,
        "shelf_id": 4,
        "rating": 4.8
    },
    {
        "isbn": "9788073908959",
        "title": "Dracula",
        "author": "Bram Stoker",
        "genres": ["Horor", "Klasika", "Gotický román"],
        "description": "Nesmrtelný příběh transylvánského hraběte toužícího po čerstvé krvi v Londýně.",
        "cover_url": "https://www.databazeknih.cz/img/books/38_/389279/dracula-bram-stoker-13725.jpg",
        "publisher": "Omega",
        "year": 2018,
        "shelf_id": 4,
        "rating": 4.7
    },

    # 5. Světová beletrie (A–M)
    {
        "isbn": "9788020718501",
        "title": "Cizinec",
        "author": "Albert Camus",
        "genres": ["Světová literatura", "Existencialismus"],
        "description": "Zásadní filozofický román o lhostejnosti a absurditě lidského bytí v Alžírsku.",
        "cover_url": "https://www.databazeknih.cz/img/books/38_/382903/cizinec-o7l-382903.jpg",
        "publisher": "Odeon",
        "year": 2018,
        "shelf_id": 5,
        "rating": 4.6
    },
    {
        "isbn": "9788020718013",
        "title": "Sto roků samoty",
        "author": "Gabriel García Márquez",
        "genres": ["Magický realismus", "Román"],
        "description": "Kronika rodu Buendíů v mýtické vesnici Macondo. Vrchol magického realismu.",
        "cover_url": "https://www.databazeknih.cz/img/books/36_/365113/sto-roku-samoty-bA0-365113.jpg",
        "publisher": "Odeon",
        "year": 2018,
        "shelf_id": 5,
        "rating": 4.8
    },

    # 6. Světová beletrie (N–Z)
    {
        "isbn": "9788025732298",
        "title": "1984",
        "author": "George Orwell",
        "genres": ["Dystopie", "Světová literatura"],
        "description": "Velký bratr tě sleduje. Příběh Winstona Smithe ve světě totalitního superstátu Oceánie.",
        "cover_url": "https://www.databazeknih.cz/img/books/44_/441957/1984-Z7p-441957.jpg",
        "publisher": "Argo",
        "year": 2020,
        "shelf_id": 6,
        "rating": 4.9
    },
    {
        "isbn": "9788075653451",
        "title": "Kde zpívají raci",
        "author": "Delia Owens",
        "genres": ["Světová beletrie", "Román"],
        "description": "Tajemná dívka Kya Clarková vyrůstá sama v močálech v Severní Karolíně.",
        "cover_url": "https://www.databazeknih.cz/img/books/41_/411993/kde-zpivaji-raci-9g1-411993.jpg",
        "publisher": "Jota",
        "year": 2019,
        "shelf_id": 6,
        "rating": 4.7
    },

    # 7. Česká a slovenská literatura
    {
        "isbn": "9788020714855",
        "title": "Válka s Mloky",
        "author": "Karel Čapek",
        "genres": ["Česká literatura", "Sci-Fi", "Satira"],
        "description": "Geniální protifašistická alegorická satira o lidech, kteří vycvičili inteligentní mloky.",
        "cover_url": "https://www.databazeknih.cz/img/books/13_/1334/valka-s-mloky-1334.jpg",
        "publisher": "Odeon",
        "year": 2013,
        "shelf_id": 7,
        "rating": 4.8
    },
    {
        "isbn": "9788071069270",
        "title": "Nesnesitelná lehkost bytí",
        "author": "Milan Kundera",
        "genres": ["Česká literatura", "Filozofický román"],
        "description": "Milostný čtyřúhelník na pozadí Pražského jara 1968 a následné emigrace.",
        "cover_url": "https://www.databazeknih.cz/img/books/30_/3027/nesnesitelna-lehkost-byti-3027.jpg",
        "publisher": "Atlantis",
        "year": 2006,
        "shelf_id": 7,
        "rating": 4.7
    },
    {
        "isbn": "9788027502479",
        "title": "Šikmý kostel",
        "author": "Karin Lednická",
        "genres": ["Česká literatura", "Historický román"],
        "description": "Románová kronika ztraceného města Karvinné z přelomu 19. a 20. století.",
        "cover_url": "https://www.databazeknih.cz/img/books/43_/436034/sikmy-kostel-romanova-kronika-ztraceneho-mesta-leto-1894-leto-1921-6nQ-436034.jpg",
        "publisher": "Bílá vrána",
        "year": 2020,
        "shelf_id": 7,
        "rating": 4.9
    },

    # 8. Historické romány & Válečná próza
    {
        "isbn": "9788020717207",
        "title": "Egypťan Sinuhet",
        "author": "Mika Waltari",
        "genres": ["Historický román", "Klasika"],
        "description": "Příběh královského lékaře za vlády faraona Achnatona ve starověkém Egyptě.",
        "cover_url": "https://www.databazeknih.cz/img/books/13_/1332/egyptan-sinuhet-1332.jpg",
        "publisher": "Odeon",
        "year": 2016,
        "shelf_id": 8,
        "rating": 4.9
    },
    {
        "isbn": "9788024255736",
        "title": "Pilíře země",
        "author": "Ken Follett",
        "genres": ["Historický román"],
        "description": "Monumentální sága o stavbě velkolepé katedrály v Kingsbridge ve 12. století.",
        "cover_url": "https://www.databazeknih.cz/img/books/34_/344154/pilire-zeme-59O-344154.jpg",
        "publisher": "Knižní klub",
        "year": 2017,
        "shelf_id": 8,
        "rating": 4.9
    },

    # 9. Historie, Biografie & Fakta
    {
        "isbn": "9788073355524",
        "title": "Černobyl: Historie jaderné katastrofy",
        "author": "Serhii Plokhy",
        "genres": ["Historie", "Literatura faktu"],
        "description": "Vyčerpávající a mrazivá rekonstrukce nejhorší jaderné havárie lidstva v dubnu 1986.",
        "cover_url": "https://www.databazeknih.cz/img/books/41_/411931/cernobyl-historie-jaderne-katastrofy-c7e-411931.jpg",
        "publisher": "Jota",
        "year": 2019,
        "shelf_id": 9,
        "rating": 4.8
    },
    {
        "isbn": "9788072604081",
        "title": "Steve Jobs",
        "author": "Walter Isaacson",
        "genres": ["Biografie", "Literatura faktu"],
        "description": "Jedinečný a otevřený životopis spoluzakladatele společnosti Apple.",
        "cover_url": "https://www.databazeknih.cz/img/books/99_/99052/steve-jobs-99052.jpg",
        "publisher": "Práh",
        "year": 2015,
        "shelf_id": 9,
        "rating": 4.7
    },

    # 10. Věda, Technologie & Příroda
    {
        "isbn": "9788073635282",
        "title": "Sapiens: Od zvířete k božskému tvoru",
        "author": "Yuval Noah Harari",
        "genres": ["Věda", "Historie", "Antropologie"],
        "description": "Fascinující dějiny lidstva od prvních lidí po revoluce vědy a technologií.",
        "cover_url": "https://www.databazeknih.cz/img/books/21_/215888/sapiens-strucne-dejiny-lidstva-215888.jpg",
        "publisher": "Leda",
        "year": 2014,
        "shelf_id": 10,
        "rating": 4.8
    },
    {
        "isbn": "9788073638481",
        "title": "Stručná historie času",
        "author": "Stephen Hawking",
        "genres": ["Věda", "Fyzika", "Astronomie"],
        "description": "Od velkého třesku k černým dírám – klasický průvodce moderní kosmologií.",
        "cover_url": "https://www.databazeknih.cz/img/books/34_/344155/strucna-historie-casu-344155.jpg",
        "publisher": "Argo",
        "year": 2018,
        "shelf_id": 10,
        "rating": 4.7
    },

    # 11. Filozofie, Psychologie & Rozvoj
    {
        "isbn": "9788087270424",
        "title": "Myšlení, rychlé a pomalé",
        "author": "Daniel Kahneman",
        "genres": ["Psychologie", "Věda"],
        "description": "Nobelista Kahneman odhaluje, jak fungují naše dva systémy myšlení a rozhodování.",
        "cover_url": "https://www.databazeknih.cz/img/books/13_/133989/mysleni-rychle-a-pomale-133989.jpg",
        "publisher": "Jan Melvil Publishing",
        "year": 2012,
        "shelf_id": 11,
        "rating": 4.8
    },
    {
        "isbn": "9788073633639",
        "title": "Hovory k sobě",
        "author": "Marcus Aurelius",
        "genres": ["Filozofie", "Stoicismus", "Klasika"],
        "description": "Osobní zápisky římského císaře a filozofa o povinnosti, klidu mysli a ctnosti.",
        "cover_url": "https://www.databazeknih.cz/img/books/65_/65096/hovory-k-sobe-65096.jpg",
        "publisher": "Argo",
        "year": 2011,
        "shelf_id": 11,
        "rating": 4.9
    },

    # 12. Umění, Architektura & Design
    {
        "isbn": "9788073636531",
        "title": "Příběh umění",
        "author": "Ernst Gombrich",
        "genres": ["Umění", "Dějiny umění"],
        "description": "Nejslavnější a nejčtenější úvod do dějin světového výtvarného umění.",
        "cover_url": "https://www.databazeknih.cz/img/books/14_/14002/pribeh-umeni-14002.jpg",
        "publisher": "Argo",
        "year": 2015,
        "shelf_id": 12,
        "rating": 4.9
    },

    # 13. Cestování & Zeměpis
    {
        "isbn": "9788075651525",
        "title": "Afrika snů a skutečnosti",
        "author": "Jiří Hanzelka, Miroslav Zikmund",
        "genres": ["Cestopis", "Geografie"],
        "description": "Legendární putování napříč africkým kontinentem ve stříbrné Tatře 87.",
        "cover_url": "https://www.databazeknih.cz/img/books/13_/13838/afrika-snu-a-skutecnosti-1-13838.jpg",
        "publisher": "Jota",
        "year": 2017,
        "shelf_id": 13,
        "rating": 4.8
    },

    # 14. Kuchařky, Zahrada & Hobby
    {
        "isbn": "9788088244073",
        "title": "Kuchařka pro dceru",
        "author": "Jana Florentýna Zatloukalová",
        "genres": ["Kuchařka", "Gastronomie"],
        "description": "Základní i pokročilé kuchařské postupy s láskou a srozumitelným vysvětlením.",
        "cover_url": "https://www.databazeknih.cz/img/books/21_/215889/kucharka-pro-dceru-215889.jpg",
        "publisher": "Smart Press",
        "year": 2018,
        "shelf_id": 14,
        "rating": 4.8
    },

    # 15. Komiksy, Manga & Young Adult
    {
        "isbn": "9788074492211",
        "title": "Strážci - Watchmen",
        "author": "Alan Moore, Dave Gibbons",
        "genres": ["Komiks", "Grafický román"],
        "description": "Kdo stráží ty, kteří stráží nás? Vrcholný komiksový román dvacátého století.",
        "cover_url": "https://www.databazeknih.cz/img/books/13_/13725/strazci-watchmen-13725.jpg",
        "publisher": "BB/art",
        "year": 2013,
        "shelf_id": 15,
        "rating": 5.0
    },

    # 16. Dětská literatura & Pohádky
    {
        "isbn": "9788000035888",
        "title": "Malý princ",
        "author": "Antoine de Saint-Exupéry",
        "genres": ["Dětská literatura", "Filozofie", "Pohádka"],
        "description": "Správně vidíme jen srdcem. Co je důležité, je očím neviditelné.",
        "cover_url": "https://www.databazeknih.cz/img/books/13_/1338/maly-princ-1338.jpg",
        "publisher": "Albatros",
        "year": 2014,
        "shelf_id": 16,
        "rating": 5.0
    },
    {
        "isbn": "9788000045894",
        "title": "Povídání o pejskovi a kočičce",
        "author": "Josef Čapek",
        "genres": ["Dětská literatura", "Pohádky"],
        "description": "Jak pejsek a kočička myli podlahu, pekli dort a dělali ještě spoustu dalších věcí.",
        "cover_url": "https://www.databazeknih.cz/img/books/13_/1340/povidani-o-pejskovi-a-kocicce-1340.jpg",
        "publisher": "Albatros",
        "year": 2016,
        "shelf_id": 16,
        "rating": 4.9
    }
]

def seed_sample_books():
    """Inserts sample books into the database if empty."""
    from app.database import get_db, add_book
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM books")
    count = cursor.fetchone()["count"]
    conn.close()
    
    if count == 0:
        for b in SAMPLE_BOOKS:
            add_book(b)
        print(f"Successfully seeded {len(SAMPLE_BOOKS)} sample books.")
