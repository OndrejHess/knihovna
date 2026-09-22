import sqlite3
import os
import json
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "library.db")

DEFAULT_SHELVES = [
    {
        "id": 1,
        "name": "Police 1: Sci-Fi & Kyberpunk",
        "theme": "Sci-Fi",
        "icon": "🚀",
        "color": "#38bdf8",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Vesmírné opery, kyberpunk, dystopie a vědecká fantastika."
    },
    {
        "id": 2,
        "name": "Police 2: Fantasy & Mytologie",
        "theme": "Fantasy",
        "icon": "🐉",
        "color": "#a855f7",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Epická fantasy, meč a magie, urban fantasy a mýty."
    },
    {
        "id": 3,
        "name": "Police 3: Detektivky & Thrillery",
        "theme": "Detektivky a Thrillery",
        "icon": "🔍",
        "color": "#eab308",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Severské krimi, psychologické thrillery a klasické detektivky."
    },
    {
        "id": 4,
        "name": "Police 4: Horory & Mystika",
        "theme": "Horor a Mystika",
        "icon": "🦇",
        "color": "#ef4444",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Hororová literatura, nadpřirozeno, temné napětí a gotické příběhy."
    },
    {
        "id": 5,
        "name": "Police 5: Světová beletrie (A–M)",
        "theme": "Světová beletrie A-M",
        "icon": "📖",
        "color": "#06b6d4",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Světové romány, moderní próza a klasická díla autorů A až M."
    },
    {
        "id": 6,
        "name": "Police 6: Světová beletrie (N–Z)",
        "theme": "Světová beletrie N-Z",
        "icon": "📚",
        "color": "#14b8a6",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Světové romány, moderní próza a klasická díla autorů N až Z."
    },
    {
        "id": 7,
        "name": "Police 7: Česká a slovenská literatura",
        "theme": "Česká a slovenská literatura",
        "icon": "🇨🇿",
        "color": "#3b82f6",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Domácí beletrie, čeští klasici i současná česká tvorba."
    },
    {
        "id": 8,
        "name": "Police 8: Historické romány & Válečná próza",
        "theme": "Historické romány",
        "icon": "⚔️",
        "color": "#f97316",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Historické ságy, rytířské romány a válečné osudy."
    },
    {
        "id": 9,
        "name": "Police 9: Historie, Biografie & Fakta",
        "theme": "Historie a Biografie",
        "icon": "🏛️",
        "color": "#d97706",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Literatura faktu, dějiny, memoáry a životopisy slavných osobností."
    },
    {
        "id": 10,
        "name": "Police 10: Věda, Technologie & Příroda",
        "theme": "Věda a Příroda",
        "icon": "🔬",
        "color": "#10b981",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Populárně naučná věda, IT, astronomie, biologie a fyzika."
    },
    {
        "id": 11,
        "name": "Police 11: Filozofie, Psychologie & Rozvoj",
        "theme": "Filozofie a Psychologie",
        "icon": "🧠",
        "color": "#8b5cf6",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Hluboké myšlení, psychologická díla, sociologie a seberozvoj."
    },
    {
        "id": 12,
        "name": "Police 12: Umění, Architektura & Design",
        "theme": "Umění a Architektura",
        "icon": "🎨",
        "color": "#ec4899",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Dějiny umění, fotografie, grafika, architektura a film."
    },
    {
        "id": 13,
        "name": "Police 13: Cestování & Zeměpis",
        "theme": "Cestování a Geografie",
        "icon": "🧭",
        "color": "#0ea5e9",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Cestopisy, průvodce, expedice, geografie a atlasy."
    },
    {
        "id": 14,
        "name": "Police 14: Kuchařky, Zahrada & Hobby",
        "theme": "Hobby a Kuchařky",
        "icon": "🍳",
        "color": "#84cc16",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Gastronomie, pěstování, kutilství, sport a volný čas."
    },
    {
        "id": 15,
        "name": "Police 15: Komiksy, Manga & Young Adult",
        "theme": "Komiksy a YA",
        "icon": "💥",
        "color": "#f43f5e",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Grafické romány, komiksové série, manga a literatura pro mládež."
    },
    {
        "id": 16,
        "name": "Police 16: Dětská literatura & Pohádky",
        "theme": "Dětská literatura",
        "icon": "🧸",
        "color": "#f59e0b",
        "capacity_min": 30,
        "capacity_max": 40,
        "notes": "Ilustrované knížky, bajky, pohádky a první čtení pro děti."
    }
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Create shelves table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shelves (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        theme TEXT NOT NULL,
        icon TEXT,
        color TEXT,
        capacity_min INTEGER DEFAULT 30,
        capacity_max INTEGER DEFAULT 40,
        notes TEXT
    )
    """)

    # Create books table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isbn TEXT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genres TEXT,
        description TEXT,
        cover_url TEXT,
        publisher TEXT,
        year INTEGER,
        page_count INTEGER,
        shelf_id INTEGER REFERENCES shelves(id),
        shelf_position INTEGER DEFAULT 0,
        rating REAL DEFAULT 0,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

    # Seed default 16 shelves if not present
    cursor.execute("SELECT COUNT(*) as count FROM shelves")
    if cursor.fetchone()["count"] == 0:
        for s in DEFAULT_SHELVES:
            cursor.execute("""
            INSERT INTO shelves (id, name, theme, icon, color, capacity_min, capacity_max, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                s["id"], s["name"], s["theme"], s["icon"], s["color"],
                s["capacity_min"], s["capacity_max"], s["notes"]
            ))
        conn.commit()

    conn.close()

def get_all_shelves() -> List[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT s.*, 
           COUNT(b.id) as book_count
    FROM shelves s
    LEFT JOIN books b ON s.id = b.shelf_id
    GROUP BY s.id
    ORDER BY s.id ASC
    """)
    rows = cursor.fetchall()
    shelves = [dict(row) for row in rows]
    conn.close()
    return shelves

def get_shelf(shelf_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT s.*, COUNT(b.id) as book_count
    FROM shelves s
    LEFT JOIN books b ON s.id = b.shelf_id
    WHERE s.id = ?
    GROUP BY s.id
    """, (shelf_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_shelf(shelf_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    fields = []
    values = []
    for k in ["name", "theme", "icon", "color", "capacity_min", "capacity_max", "notes"]:
        if k in data:
            fields.append(f"{k} = ?")
            values.append(data[k])
    if not fields:
        conn.close()
        return get_shelf(shelf_id)
    values.append(shelf_id)
    cursor.execute(f"UPDATE shelves SET {', '.join(fields)} WHERE id = ?", tuple(values))
    conn.commit()
    conn.close()
    return get_shelf(shelf_id)

def get_all_books(
    search: Optional[str] = None,
    shelf_id: Optional[int] = None,
    genre: Optional[str] = None,
    limit: int = 1000,
    offset: int = 0
) -> List[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    
    query = """
    SELECT b.*, s.name as shelf_name, s.theme as shelf_theme, s.color as shelf_color, s.icon as shelf_icon
    FROM books b
    LEFT JOIN shelves s ON b.shelf_id = s.id
    WHERE 1=1
    """
    params = []

    if search:
        s_clean = f"%{search.strip()}%"
        query += " AND (b.title LIKE ? OR b.author LIKE ? OR b.isbn LIKE ? OR b.genres LIKE ?)"
        params.extend([s_clean, s_clean, s_clean, s_clean])
    
    if shelf_id is not None:
        query += " AND b.shelf_id = ?"
        params.append(shelf_id)

    if genre:
        query += " AND b.genres LIKE ?"
        params.append(f"%{genre}%")

    query += " ORDER BY b.shelf_id ASC, b.shelf_position ASC, b.author ASC, b.title ASC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    books = []
    for r in rows:
        d = dict(r)
        if d.get("genres"):
            try:
                d["genres_list"] = json.loads(d["genres"]) if d["genres"].startswith("[") else [g.strip() for g in d["genres"].split(",") if g.strip()]
            except Exception:
                d["genres_list"] = [d["genres"]]
        else:
            d["genres_list"] = []
        books.append(d)
    conn.close()
    return books

def get_book(book_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT b.*, s.name as shelf_name, s.theme as shelf_theme, s.color as shelf_color, s.icon as shelf_icon
    FROM books b
    LEFT JOIN shelves s ON b.shelf_id = s.id
    WHERE b.id = ?
    """, (book_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    if d.get("genres"):
        try:
            d["genres_list"] = json.loads(d["genres"]) if d["genres"].startswith("[") else [g.strip() for g in d["genres"].split(",") if g.strip()]
        except Exception:
            d["genres_list"] = [d["genres"]]
    else:
        d["genres_list"] = []
    return d

def add_book(book_data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_db()
    cursor = conn.cursor()
    
    # If genres is list, store as JSON
    genres_val = book_data.get("genres")
    if isinstance(genres_val, list):
        genres_val = json.dumps(genres_val, ensure_ascii=False)

    cursor.execute("""
    INSERT INTO books (
        isbn, title, author, genres, description, cover_url,
        publisher, year, page_count, shelf_id, shelf_position, rating, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        book_data.get("isbn", "").strip(),
        book_data.get("title", "").strip(),
        book_data.get("author", "").strip(),
        genres_val,
        book_data.get("description", ""),
        book_data.get("cover_url", ""),
        book_data.get("publisher", ""),
        book_data.get("year"),
        book_data.get("page_count"),
        book_data.get("shelf_id", 1),
        book_data.get("shelf_position", 0),
        book_data.get("rating", 0.0),
        book_data.get("notes", "")
    ))
    book_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return get_book(book_id)

def update_book(book_id: int, book_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    fields = []
    values = []
    
    allowed = ["isbn", "title", "author", "genres", "description", "cover_url",
               "publisher", "year", "page_count", "shelf_id", "shelf_position", "rating", "notes"]
    
    for key in allowed:
        if key in book_data:
            val = book_data[key]
            if key == "genres" and isinstance(val, list):
                val = json.dumps(val, ensure_ascii=False)
            fields.append(f"{key} = ?")
            values.append(val)
            
    if not fields:
        conn.close()
        return get_book(book_id)
        
    values.append(book_id)
    cursor.execute(f"UPDATE books SET {', '.join(fields)} WHERE id = ?", tuple(values))
    conn.commit()
    conn.close()
    return get_book(book_id)

def delete_book(book_id: int) -> bool:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def batch_update_shelf_assignments(assignments: List[Dict[str, int]]):
    """
    assignments: [{"id": book_id, "shelf_id": shelf_id, "shelf_position": pos}]
    """
    conn = get_db()
    cursor = conn.cursor()
    for item in assignments:
        cursor.execute(
            "UPDATE books SET shelf_id = ?, shelf_position = ? WHERE id = ?",
            (item["shelf_id"], item.get("shelf_position", 0), item["id"])
        )
    conn.commit()
    conn.close()
