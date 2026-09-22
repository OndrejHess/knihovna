import re
import json
import urllib.request
import urllib.parse
import ssl
from typing import Optional, Dict, Any, List

def clean_isbn(isbn_str: str) -> str:
    """Removes dashes, spaces, and non-alphanumeric characters except X."""
    cleaned = re.sub(r'[^0-9Xx]', '', isbn_str.strip())
    return cleaned

def fetch_from_databazeknih(isbn: str) -> Optional[Dict[str, Any]]:
    """
    Search Databazeknih.cz by ISBN.
    Returns parsed metadata dict or None.
    """
    url = f"https://www.databazeknih.cz/search?q={urllib.parse.quote(isbn)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "cs,en;q=0.9"
    }
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=6, context=ctx) as resp:
            final_url = resp.geturl()
            html_text = resp.read().decode("utf-8", errors="ignore")
            
        # If redirected to a search list instead of direct book overview
        if "prehled-knihy" not in final_url:
            match = re.search(r'href=[\"\'](prehled-knihy/[^\"\']+)[\"\']', html_text)
            if match:
                book_rel_url = match.group(1)
                book_url = f"https://www.databazeknih.cz/{book_rel_url}"
                req2 = urllib.request.Request(book_url, headers=headers)
                with urllib.request.urlopen(req2, timeout=6, context=ctx) as resp2:
                    html_text = resp2.read().decode("utf-8", errors="ignore")
                    final_url = resp2.geturl()
            else:
                return None
                
        # Parse JSON-LD if available (very structured & reliable)
        ld_scripts = re.findall(r'<script type=[\"\']application/ld\+json[\"\']>(.*?)</script>', html_text, re.DOTALL)
        for s in ld_scripts:
            try:
                data = json.loads(s)
                if isinstance(data, dict) and data.get("@type") == "Book":
                    # Extract authors
                    authors_raw = data.get("author", [])
                    if isinstance(authors_raw, list):
                        authors = [a.get("name", "") for a in authors_raw if isinstance(a, dict) and a.get("name")]
                    elif isinstance(authors_raw, dict):
                        authors = [authors_raw.get("name", "")]
                    elif isinstance(authors_raw, str):
                        authors = [authors_raw]
                    else:
                        authors = []
                    author_str = ", ".join(filter(None, authors))
                    
                    # Extract genres
                    genres_raw = data.get("genre", [])
                    if isinstance(genres_raw, str):
                        genres = [genres_raw]
                    elif isinstance(genres_raw, list):
                        genres = genres_raw
                    else:
                        genres = []
                        
                    # Publisher
                    pub_raw = data.get("publisher", {})
                    publisher = pub_raw.get("name", "") if isinstance(pub_raw, dict) else str(pub_raw or "")
                    
                    # Year
                    date_pub = data.get("datePublished", "")
                    year = None
                    if date_pub:
                        y_match = re.search(r'\b(19\d\d|20\d\d)\b', str(date_pub))
                        if y_match:
                            year = int(y_match.group(1))
                            
                    # Rating
                    rating = 0.0
                    if data.get("aggregateRating") and isinstance(data["aggregateRating"], dict):
                        try:
                            rating = float(data["aggregateRating"].get("ratingValue", 0))
                        except (ValueError, TypeError):
                            rating = 0.0
                            
                    return {
                        "isbn": isbn,
                        "title": data.get("name", "").strip(),
                        "author": author_str.strip(),
                        "genres": genres,
                        "description": data.get("description", "").strip(),
                        "cover_url": data.get("image", ""),
                        "publisher": publisher.strip(),
                        "year": year,
                        "rating": rating,
                        "source": "databazeknih.cz"
                    }
            except Exception:
                continue

        # HTML Regex Fallback if JSON-LD wasn't present
        title_m = re.search(r'<h1[^>]*>(.*?)</h1>', html_text, re.DOTALL)
        title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else ""
        
        # Author
        author_m = re.search(r'<a[^>]*href=[\"\'][^\"\']*autori/[^\"\']*[\"\'][^>]*>(.*?)</a>', html_text)
        author = re.sub(r'<[^>]+>', '', author_m.group(1)).strip() if author_m else ""
        
        # Image
        img_m = re.search(r'<img[^>]*src=[\"\'](https://www\.databazeknih\.cz/img/books/[^\"\']+)[\"\']', html_text)
        cover_url = img_m.group(1) if img_m else ""
        
        # Genres
        genres = re.findall(r'<a[^>]*href=[\"\']/zanry/[^\"\']*[\"\'][^>]*>([^<]+)</a>', html_text)
        
        if title:
            return {
                "isbn": isbn,
                "title": title,
                "author": author,
                "genres": genres,
                "description": "",
                "cover_url": cover_url,
                "publisher": "",
                "year": None,
                "rating": 0.0,
                "source": "databazeknih.cz"
            }
    except Exception as e:
        print(f"Error fetching from Databazeknih: {e}")
        
    return None

def fetch_from_openlibrary(isbn: str) -> Optional[Dict[str, Any]]:
    """
    Search OpenLibrary by ISBN.
    """
    headers = {
        "User-Agent": "KnihovnaScanner/1.0 (https://github.com/lachtan/Knihovna)"
    }
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    # Try OpenLibrary ISBN JSON first
    try:
        url = f"https://openlibrary.org/isbn/{isbn}.json"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            
            title = data.get("title", "")
            if not title:
                return None
                
            # Authors in isbn.json are keys like {'key': '/authors/OL23919A'}
            authors = []
            if "authors" in data and isinstance(data["authors"], list):
                for a in data["authors"]:
                    if isinstance(a, dict) and "key" in a:
                        try:
                            a_url = f"https://openlibrary.org{a['key']}.json"
                            a_req = urllib.request.Request(a_url, headers=headers)
                            with urllib.request.urlopen(a_req, timeout=3, context=ctx) as a_resp:
                                a_data = json.loads(a_resp.read().decode("utf-8"))
                                if "name" in a_data:
                                    authors.append(a_data["name"])
                        except Exception:
                            pass
                            
            # Publishers
            publishers = data.get("publishers", [])
            publisher = publishers[0] if publishers else ""
            
            # Publish year
            pub_date = data.get("publish_date", "")
            year = None
            if pub_date:
                m = re.search(r'\b(19\d\d|20\d\d)\b', pub_date)
                if m:
                    year = int(m.group(1))
                    
            # Cover URL
            cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
            
            # Description
            desc = data.get("description", "")
            if isinstance(desc, dict):
                desc = desc.get("value", "")
                
            return {
                "isbn": isbn,
                "title": title,
                "author": ", ".join(authors),
                "genres": data.get("subjects", [])[:4],
                "description": desc,
                "cover_url": cover_url,
                "publisher": publisher,
                "year": year,
                "rating": 0.0,
                "source": "openlibrary.org"
            }
    except Exception:
        pass
        
    # Search endpoint fallback
    try:
        url = f"https://openlibrary.org/search.json?q={isbn}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            docs = data.get("docs", [])
            if docs:
                doc = docs[0]
                return {
                    "isbn": isbn,
                    "title": doc.get("title", ""),
                    "author": ", ".join(doc.get("author_name", [])),
                    "genres": doc.get("subject", [])[:4],
                    "description": "",
                    "cover_url": f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg",
                    "publisher": doc.get("publisher", [""])[0] if doc.get("publisher") else "",
                    "year": doc.get("first_publish_year"),
                    "rating": float(doc.get("ratings_average", 0) or 0),
                    "source": "openlibrary.org"
                }
    except Exception as e:
        print(f"Error fetching from OpenLibrary: {e}")
        
    return None

def lookup_book_by_isbn(isbn_input: str) -> Optional[Dict[str, Any]]:
    """
    Master lookup function:
    1. Databazeknih.cz (for Czech books and rich metadata)
    2. OpenLibrary fallback (for international books)
    """
    isbn = clean_isbn(isbn_input)
    if not isbn:
        return None
        
    # 1. Databáze knih
    book = fetch_from_databazeknih(isbn)
    if book and book.get("title"):
        return book
        
    # 2. Open Library
    book = fetch_from_openlibrary(isbn)
    if book and book.get("title"):
        return book
        
    return None
