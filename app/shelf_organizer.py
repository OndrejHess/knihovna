import re
import unicodedata
from typing import List, Dict, Any, Tuple, Optional

def normalize_text(text: str) -> str:
    """Normalize text for matching: lowercase, strip accents, strip punctuation."""
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    return text.lower().strip()

def get_author_sort_key(author_str: str) -> str:
    """
    Extract author's surname for sorting (e.g. 'Karel Čapek' -> 'capek, karel').
    """
    if not author_str:
        return ""
    norm = normalize_text(author_str)
    # Remove honorifics, initials, (p)
    norm = re.sub(r'\(.*?\)', '', norm).strip()
    parts = norm.split()
    if len(parts) > 1:
        # Surname is usually the last word
        surname = parts[-1]
        firstnames = " ".join(parts[:-1])
        return f"{surname}, {firstnames}"
    return norm

# Thematic rules with priority weights and keywords
SHELF_THEMES = [
    {
        "id": 1,
        "name": "Police 1: Sci-Fi & Kyberpunk",
        "theme": "Sci-Fi",
        "keywords": [
            "sci-fi", "scifi", "science fiction", "kyberpunk", "cyberpunk",
            "vesmir", "dystopie", "postapo", "postapokalypt", "umele inteligence",
            "roboti", "mimozemstan", "galaxie", "asimov", "arthur c. clarke",
            "philip k. dick", "stanislaw lem", "glukhovsky", "herbert", "duna"
        ]
    },
    {
        "id": 2,
        "name": "Police 2: Fantasy & Mytologie",
        "theme": "Fantasy",
        "keywords": [
            "fantasy", "mytologie", "myty", "carodej", "kouzla", "magie",
            "draci", "elf", "tolkien", "sapkowski", "sanderson", "george r. r. martin",
            "rowling", "zaklinac", "pan prstenu", "hobbit", "hobbita", "pratchett",
            "zemeplocha", "epik"
        ]
    },
    {
        "id": 3,
        "name": "Police 3: Detektivky & Thrillery",
        "theme": "Detektivky a Thrillery",
        "keywords": [
            "detektiv", "detektivka", "krimi", "kriminalka", "thriller",
            "vrazda", "vrah", "policie", "vysetrovatel", "spion", "zahada",
            "agatha christie", "arthur conan doyle", "jo nesbo", "robert bryndza",
            "larsson", "kepler", "dan brown", "sherlock"
        ]
    },
    {
        "id": 4,
        "name": "Police 4: Horory & Mystika",
        "theme": "Horor a Mystika",
        "keywords": [
            "horor", "horror", "mystika", "nadprirozeno", "strasideln",
            "duch", "upir", "vlkodlak", "zombie", "temno", "lovecraft",
            "stephen king", "poe", "bram stoker", "dracula", "frankenstein"
        ]
    },
    {
        "id": 5,
        "name": "Police 5: Světová beletrie (A–M)",
        "theme": "Světová beletrie A-M",
        "keywords": [
            "beletrie", "svetova literatura", "roman", "spolecensky roman", "klasika"
        ]
    },
    {
        "id": 6,
        "name": "Police 6: Světová beletrie (N–Z)",
        "theme": "Světová beletrie N-Z",
        "keywords": [
            "beletrie", "svetova literatura", "roman", "spolecensky roman", "klasika"
        ]
    },
    {
        "id": 7,
        "name": "Police 7: Česká a slovenská literatura",
        "theme": "Česká a slovenská literatura",
        "keywords": [
            "ceska literatura", "ceska beletrie", "cesky autor", "slovenska literatura",
            "capek", "karel capek", "kundera", "milan kundera", "hrabal", "bohumil hrabal",
            "nemcova", "bozena nemcova", "hasek", "jaroslav hasek", "skvorecky",
            "viewegh", "mornstajnova", "tuckova", "patrik hartl", "radka trestikova",
            "polacek", "neruda", "vanbura", "lustig", "fuks", "erben", "macha"
        ]
    },
    {
        "id": 8,
        "name": "Police 8: Historické romány & Válečná próza",
        "theme": "Historické romány",
        "keywords": [
            "historicky roman", "valecna beletrie", "valecny roman", "stredovek",
            "antika", "rimsky", "krizaci", "valka", "druha svetova valka",
            "mika waltari", "ken follett", "bernard cornwell", "remarque",
            "egyptan sinuhet", "pilire zeme"
        ]
    },
    {
        "id": 9,
        "name": "Police 9: Historie, Biografie & Fakta",
        "theme": "Historie a Biografie",
        "keywords": [
            "historie", "dejiny", "biografie", "zivotopis", "memoary", "pameti",
            "literatura faktu", "dokument", "monografie", "holokaust", "druha svetova",
            "prvni svetova", "komunismus", "stalin", "hitler", "churchill", "havel"
        ]
    },
    {
        "id": 10,
        "name": "Police 10: Věda, Technologie & Příroda",
        "theme": "Věda a Příroda",
        "keywords": [
            "veda", "popularne naucna", "technologie", "priroda", "fyzika",
            "astronomie", "biologie", "chemie", "matematika", "it", "pocitace",
            "programovani", "vesmir", "evoluce", "ekologie", "stephen hawking",
            "carl sagan", "richard dawkins", "harari", "sapiens"
        ]
    },
    {
        "id": 11,
        "name": "Police 11: Filozofie, Psychologie & Rozvoj",
        "theme": "Filozofie a Psychologie",
        "keywords": [
            "filozofie", "psychologie", "osobni rozvoj", "seberozvoj", "motivace",
            "mysleni", "sociologie", "etika", "stoicismus", "meditace", "spiritualita",
            "kahneman", "peterson", "freud", "jung", "nietzsche", "platon", "marcus aurelius"
        ]
    },
    {
        "id": 12,
        "name": "Police 12: Umění, Architektura & Design",
        "theme": "Umění a Architektura",
        "keywords": [
            "umeni", "architektura", "design", "fotografie", "malirstvi",
            "socharstvi", "film", "hudba", "divadlo", "vytvarne umeni", "dejiny umeni"
        ]
    },
    {
        "id": 13,
        "name": "Police 13: Cestování & Zeměpis",
        "theme": "Cestování a Geografie",
        "keywords": [
            "cestovani", "cestopis", "pruvodce", "geografie", "zemepis",
            "expedice", "hory", "dobrodruzstvi", "zikmund a hanzelka", "lonely planet",
            "national geographic", "atlas"
        ]
    },
    {
        "id": 14,
        "name": "Police 14: Kuchařky, Zahrada & Hobby",
        "theme": "Hobby a Kuchařky",
        "keywords": [
            "kucharka", "vareni", "recepty", "gastronomie", "peceni", "zahrada",
            "zahradniceni", "kutilstvi", "hobby", "sport", "rybareni", "fitness",
            "zdravi a zivotni styl", "domacnost"
        ]
    },
    {
        "id": 15,
        "name": "Police 15: Komiksy, Manga & Young Adult",
        "theme": "Komiksy a YA",
        "keywords": [
            "komiks", "komiksy", "manga", "graficky roman", "young adult",
            "pro mladez", "teenager", "marvel", "dc", "anime", "komix"
        ]
    },
    {
        "id": 16,
        "name": "Police 16: Dětská literatura & Pohádky",
        "theme": "Dětská literatura",
        "keywords": [
            "pro deti", "detska literatura", "pohadka", "pohadky", "vecernicek",
            "ilustrovana", "leporelo", "foglar", "krtek", "cvrcek", "broucci",
            "pro nejmensi", "prvni cteni"
        ]
    }
]

def score_book_for_shelf(book: Dict[str, Any], shelf: Dict[str, Any]) -> int:
    """
    Computes matching score between a book and a shelf.
    """
    shelf_id = shelf["id"]
    keywords = shelf["keywords"]
    
    # Text to match against
    genres_text = ""
    if book.get("genres_list"):
        genres_text = " ".join(book["genres_list"])
    elif book.get("genres"):
        genres_text = str(book["genres"])
        
    author_text = book.get("author", "")
    title_text = book.get("title", "")
    desc_text = book.get("description", "")
    
    combined_norm = normalize_text(f"{genres_text} {author_text} {title_text} {desc_text}")
    genres_norm = normalize_text(genres_text)
    author_norm = normalize_text(author_text)
    title_norm = normalize_text(title_text)

    score = 0
    
    # Priority for Czech literature shelf (Shelf 7)
    if shelf_id == 7:
        if "ceska" in genres_norm or "slovenska" in genres_norm:
            score += 40
        for kw in keywords:
            if kw in author_norm:
                score += 50
            elif kw in combined_norm:
                score += 15
        return score

    # Priority for Children books (Shelf 16) vs Young Adult (Shelf 15)
    if shelf_id == 16:
        if "pro deti" in genres_norm or "pohadk" in genres_norm:
            score += 35
    if shelf_id == 15:
        if "komiks" in genres_norm or "manga" in genres_norm or "young adult" in genres_norm:
            score += 35

    # Check keyword occurrences
    for kw in keywords:
        if kw in genres_norm:
            score += 20
        elif kw in title_norm:
            score += 10
        elif kw in combined_norm:
            score += 5
            
    # Shelf 5 & 6 are World Fiction A-M and N-Z fallback
    if shelf_id in (5, 6):
        sort_key = get_author_sort_key(author_text)
        first_letter = sort_key[0].upper() if sort_key else "A"
        is_a_m = 'A' <= first_letter <= 'M'
        
        if (shelf_id == 5 and is_a_m) or (shelf_id == 6 and not is_a_m):
            score += 8
            if any(g in genres_norm for g in ["svetova", "beletrie", "roman", "proza"]):
                score += 25

    return score

def determine_best_shelf(book: Dict[str, Any]) -> int:
    """
    Finds best matching shelf (1..16) for a given single book.
    """
    # Special check for Czech literature
    author_norm = normalize_text(book.get("author", ""))
    genres_norm = normalize_text(" ".join(book.get("genres_list", [])) if book.get("genres_list") else str(book.get("genres", "")))
    
    # If genre explicitly contains Czech/Slovak lit
    if "ceska" in genres_norm or "slovenska" in genres_norm:
        return 7
        
    best_shelf_id = 5
    best_score = -1
    
    for shelf in SHELF_THEMES:
        score = score_book_for_shelf(book, shelf)
        if score > best_score:
            best_score = score
            best_shelf_id = shelf["id"]
            
    # Fallback if no specific theme matched with high confidence (score <= 5)
    if best_score <= 5:
        sort_key = get_author_sort_key(book.get("author", ""))
        first_letter = sort_key[0].upper() if sort_key else "A"
        return 5 if 'A' <= first_letter <= 'M' else 6
        
    return best_shelf_id

def organize_bookshelf(books: List[Dict[str, Any]], target_capacity: int = 35, max_capacity: int = 40) -> Dict[str, Any]:
    """
    Organizes all books into the 16 shelves thematically, respecting capacity 30-40 books.
    Returns:
    {
        "shelves_distribution": { shelf_id: [books] },
        "assignments": [ {"id": book_id, "shelf_id": shelf_id, "shelf_position": pos} ],
        "stats": { ... },
        "summary": "..."
    }
    """
    # Step 1: Initial thematic grouping
    shelf_buckets: Dict[int, List[Dict[str, Any]]] = {i: [] for i in range(1, 17)}
    
    for book in books:
        shelf_id = determine_best_shelf(book)
        shelf_buckets[shelf_id].append(book)
        
    # Step 2: Sort books inside each bucket by author surname then title
    for s_id in shelf_buckets:
        shelf_buckets[s_id].sort(key=lambda b: (get_author_sort_key(b.get("author", "")), b.get("title", "")))

    # Step 3: Handle Overflow if any shelf exceeds max_capacity (40 books)
    # Natural overflow pairings (e.g. Shelf 1 Sci-Fi overflows to Shelf 2 Fantasy, Shelf 5 A-M to Shelf 6 N-Z, etc.)
    overflow_pairs = {
        1: 2, 2: 1,      # Sci-Fi <-> Fantasy
        3: 4, 4: 3,      # Krimi <-> Horor
        5: 6, 6: 5,      # Beletrie A-M <-> N-Z
        8: 9, 9: 8,      # Hist. romány <-> Historie/Biografie
        10: 11, 11: 10,  # Věda <-> Filozofie
        15: 16, 16: 15   # Komiksy <-> Dětská
    }
    
    overflow_events = []
    
    for s_id in range(1, 17):
        if len(shelf_buckets[s_id]) > max_capacity:
            excess_count = len(shelf_buckets[s_id]) - target_capacity
            overflow_books = shelf_buckets[s_id][target_capacity:]
            shelf_buckets[s_id] = shelf_buckets[s_id][:target_capacity]
            
            # Destination shelf
            partner_id = overflow_pairs.get(s_id)
            dest_id = None
            
            # Check if partner shelf has capacity
            if partner_id and len(shelf_buckets[partner_id]) + len(overflow_books) <= max_capacity:
                dest_id = partner_id
            else:
                # Find the shelf with lowest book count
                dest_id = min(shelf_buckets.keys(), key=lambda k: len(shelf_buckets[k]))
                
            shelf_buckets[dest_id].extend(overflow_books)
            shelf_buckets[dest_id].sort(key=lambda b: (get_author_sort_key(b.get("author", "")), b.get("title", "")))
            
            overflow_events.append({
                "from_shelf": s_id,
                "to_shelf": dest_id,
                "count": len(overflow_books)
            })

    # Step 4: Construct database update assignments with positions
    assignments = []
    distribution = {}
    shelf_stats = []
    
    for s_id in range(1, 17):
        b_list = shelf_buckets[s_id]
        distribution[s_id] = b_list
        count = len(b_list)
        status = "ideální"
        if count == 0:
            status = "prázdná"
        elif count < 30:
            status = "volná (doporučená kapacita 30-40)"
        elif count <= 38:
            status = "optimálně zaplněná"
        elif count <= 40:
            status = "téměř plná"
        else:
            status = "přeplněná"
            
        shelf_stats.append({
            "shelf_id": s_id,
            "book_count": count,
            "target_capacity": target_capacity,
            "max_capacity": max_capacity,
            "utilization_pct": round((count / target_capacity) * 100, 1),
            "status": status
        })
        
        for pos, b in enumerate(b_list):
            assignments.append({
                "id": b["id"],
                "shelf_id": s_id,
                "shelf_position": pos + 1
            })
            
    summary = f"Celkem {len(books)} knih bylo uspořádáno do 16 tématických poliček."
    if overflow_events:
        summary += f" Pro {len(overflow_events)} poliček s vysokým počtem knih bylo provedeno vyvážení do partnerských polic."
        
    return {
        "assignments": assignments,
        "distribution": distribution,
        "shelf_stats": shelf_stats,
        "overflow_events": overflow_events,
        "summary": summary
    }
