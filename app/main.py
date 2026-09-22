import os
import socket
import json
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import BaseModel

from app.database import (
    init_db, get_all_shelves, get_shelf, update_shelf,
    get_all_books, get_book, add_book, update_book, delete_book,
    batch_update_shelf_assignments
)
from app.lookup import lookup_book_by_isbn, clean_isbn
from app.shelf_organizer import determine_best_shelf, organize_bookshelf
from app.seed_data import seed_sample_books

# Initialize DB and Seed Data
init_db()
seed_sample_books()

app = FastAPI(title="Knihovna - Správa a uspořádání do 16 poliček", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_lan_ip() -> str:
    """Find local network IP address for mobile scanning."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# Models
class BookCreate(BaseModel):
    isbn: Optional[str] = ""
    title: str
    author: str
    genres: Optional[List[str]] = []
    description: Optional[str] = ""
    cover_url: Optional[str] = ""
    publisher: Optional[str] = ""
    year: Optional[int] = None
    page_count: Optional[int] = None
    shelf_id: Optional[int] = None
    shelf_position: Optional[int] = 0
    rating: Optional[float] = 0.0
    notes: Optional[str] = ""

class BookUpdate(BaseModel):
    isbn: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    genres: Optional[List[str]] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
    publisher: Optional[str] = None
    year: Optional[int] = None
    page_count: Optional[int] = None
    shelf_id: Optional[int] = None
    shelf_position: Optional[int] = None
    rating: Optional[float] = None
    notes: Optional[str] = None

class ShelfUpdate(BaseModel):
    name: Optional[str] = None
    theme: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    capacity_min: Optional[int] = None
    capacity_max: Optional[int] = None
    notes: Optional[str] = None

# API Routes
@app.get("/api/network-info")
def get_network_info():
    ip = get_lan_ip()
    port = int(os.environ.get("PORT", 8000))
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    has_ssl = os.path.exists(os.path.join(base_dir, "cert.pem")) and os.path.exists(os.path.join(base_dir, "key.pem"))
    return {
        "lan_ip": ip,
        "port": port,
        "url": f"http://{ip}:{port}",
        "https_url": f"https://{ip}:8443" if has_ssl else None,
        "local_url": f"http://localhost:{port}",
        "is_ssl_available": has_ssl
    }


@app.get("/api/shelves")
def list_shelves():
    shelves = get_all_shelves()
    for s in shelves:
        # Calculate status and percentage
        count = s.get("book_count", 0)
        target = s.get("capacity_min", 30)
        max_cap = s.get("capacity_max", 40)
        s["utilization_pct"] = round((count / max_cap) * 100, 1)
        if count == 0:
            s["status_badge"] = "prázdná"
            s["status_color"] = "gray"
        elif count < target:
            s["status_badge"] = f"{count}/{max_cap} knih"
            s["status_color"] = "emerald"
        elif count <= max_cap:
            s["status_badge"] = f"{count}/{max_cap} (optimální)"
            s["status_color"] = "amber"
        else:
            s["status_badge"] = f"{count}/{max_cap} (přeplněno!)"
            s["status_color"] = "rose"
    return shelves

@app.get("/api/shelves/{shelf_id}")
def read_shelf(shelf_id: int):
    shelf = get_shelf(shelf_id)
    if not shelf:
        raise HTTPException(status_code=404, detail="Polička nebyla nalezena")
    books = get_all_books(shelf_id=shelf_id)
    shelf["books"] = books
    return shelf

@app.put("/api/shelves/{shelf_id}")
def modify_shelf(shelf_id: int, payload: ShelfUpdate):
    shelf = update_shelf(shelf_id, payload.model_dump(exclude_unset=True))
    if not shelf:
        raise HTTPException(status_code=404, detail="Polička nebyla nalezena")
    return shelf

@app.get("/api/books")
def list_books(
    search: Optional[str] = None,
    shelf_id: Optional[int] = None,
    genre: Optional[str] = None,
    limit: int = 1000,
    offset: int = 0
):
    return get_all_books(search=search, shelf_id=shelf_id, genre=genre, limit=limit, offset=offset)

@app.get("/api/books/{book_id}")
def read_book(book_id: int):
    book = get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Kniha nebyla nalezena")
    return book

@app.post("/api/books")
def create_book(payload: BookCreate):
    data = payload.model_dump()
    # If shelf_id is not specified, auto-determine the best shelf (1..16)
    if not data.get("shelf_id"):
        data["shelf_id"] = determine_best_shelf(data)
    created = add_book(data)
    return created

@app.put("/api/books/{book_id}")
def modify_book(book_id: int, payload: BookUpdate):
    updated = update_book(book_id, payload.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Kniha nebyla nalezena")
    return updated

@app.delete("/api/books/{book_id}")
def remove_book(book_id: int):
    success = delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Kniha nebyla nalezena")
    return {"success": True, "message": "Kniha byla úspěšně smazána"}

@app.get("/api/lookup/{isbn}")
def lookup_book(isbn: str):
    cleaned = clean_isbn(isbn)
    if not cleaned:
        raise HTTPException(status_code=400, detail="Neplatný formát ISBN/EAN")
    
    result = lookup_book_by_isbn(cleaned)
    if not result:
        raise HTTPException(status_code=404, detail=f"Kniha s ISBN {cleaned} nebyla v databázích nalezena. Můžete ji zadat ručně.")
        
    # Suggest best shelf
    suggested_shelf_id = determine_best_shelf(result)
    result["suggested_shelf_id"] = suggested_shelf_id
    shelf = get_shelf(suggested_shelf_id)
    result["suggested_shelf_name"] = shelf["name"] if shelf else f"Police {suggested_shelf_id}"
    result["suggested_shelf_color"] = shelf["color"] if shelf else "#3b82f6"
    return result

@app.post("/api/shelves/auto-organize")
def auto_organize():
    all_books = get_all_books(limit=5000)
    if not all_books:
        return {"message": "V knihovně nejsou žádné knihy k uspořádání.", "stats": []}
        
    result = organize_bookshelf(all_books, target_capacity=35, max_capacity=40)
    batch_update_shelf_assignments(result["assignments"])
    
    # Return updated shelves state
    updated_shelves = get_all_shelves()
    return {
        "success": True,
        "summary": result["summary"],
        "shelf_stats": result["shelf_stats"],
        "overflow_events": result["overflow_events"],
        "shelves": updated_shelves
    }

@app.get("/api/export")
def export_database(format: str = "json"):
    books = get_all_books(limit=10000)
    if format == "csv":
        import csv
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "ISBN", "Název", "Autor", "Žánry", "Police ID", "Police Název", "Rok", "Vydavatel", "Hodnocení"])
        for b in books:
            genres_str = ", ".join(b.get("genres_list", []))
            writer.writerow([
                b.get("id"), b.get("isbn"), b.get("title"), b.get("author"),
                genres_str, b.get("shelf_id"), b.get("shelf_name"),
                b.get("year"), b.get("publisher"), b.get("rating")
            ])
        return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=knihovna.csv"})
    return JSONResponse(content=books)

@app.post("/api/seed")
def seed_data():
    seed_sample_books()
    return {"success": True, "message": "Ukázkové knihy byly načteny."}

# Mount Static Files
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Knihovna backend běží. Pro otevření rozhraní vytvořte index.html."}
