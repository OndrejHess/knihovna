#!/bin/bash
# ============================================================
# start.sh – Spuštění aplikace Knihovna
# ============================================================
# Použití:
#   ./start.sh          → HTTP :8000 + HTTPS :8443 (pokud cert.pem existuje)
#   ./start.sh --http   → pouze HTTP :8000
#   ./start.sh --https  → pouze HTTPS :8443
#   ./start.sh --stop   → zastaví všechny instance
# ============================================================

set -euo pipefail
cd "$(dirname "$0")"

HTTP_PORT=8000
HTTPS_PORT=8443
LOG_FILE="/tmp/knihovna.log"

# --- Barevný výstup ------------------------------------------------
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

info()  { echo -e "${CYAN}ℹ${NC}  $*"; }
ok()    { echo -e "${GREEN}✅${NC} $*"; }
warn()  { echo -e "${YELLOW}⚠${NC}  $*"; }
fail()  { echo -e "${RED}❌${NC} $*"; exit 1; }

# --- Stop ----------------------------------------------------------
if [[ "${1:-}" == "--stop" ]]; then
    info "Zastavuji všechny instance uvicorn (Knihovna)..."
    pkill -f "uvicorn app.main:app" 2>/dev/null && ok "Zastaveno." || warn "Žádný běžící server nenalezen."
    exit 0
fi

# --- Kontrola virtualenv -------------------------------------------
if [ ! -f ".venv/bin/activate" ]; then
    fail "Virtuální prostředí .venv neexistuje. Spusťte:\n  python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
fi
source .venv/bin/activate

# --- Zastavení starých instancí ------------------------------------
pkill -f "uvicorn app.main:app" 2>/dev/null || true
sleep 1

# --- Zjistit LAN IP ------------------------------------------------
LAN_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
[ -z "$LAN_IP" ] && LAN_IP="127.0.0.1"

# --- SSL dostupnost ------------------------------------------------
HAS_SSL=false
if [ -f "cert.pem" ] && [ -f "key.pem" ]; then
    HAS_SSL=true
fi

# --- Rozhodnutí o režimu -------------------------------------------
MODE="${1:---both}"

START_HTTP=false
START_HTTPS=false

case "$MODE" in
    --http)   START_HTTP=true ;;
    --https)  START_HTTPS=true ;;
    *)        START_HTTP=true; START_HTTPS=true ;;
esac

# Pokud není SSL certifikát, vždy jen HTTP
if [ "$HAS_SSL" = false ]; then
    if [ "$MODE" = "--https" ]; then
        fail "HTTPS požadováno, ale cert.pem nebo key.pem chybí."
    fi
    START_HTTPS=false
    warn "SSL certifikáty nebyly nalezeny – spouštím pouze HTTP."
fi

echo ""
echo -e "${BOLD}📚 Knihovna – správa 16 poliček${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# --- Spuštění HTTP -------------------------------------------------
if [ "$START_HTTP" = true ]; then
    nohup setsid uvicorn app.main:app \
        --host 0.0.0.0 \
        --port "$HTTP_PORT" \
        < /dev/null >> "$LOG_FILE" 2>&1 &
    sleep 1
    ok "HTTP server:  http://localhost:${HTTP_PORT}"
    ok "V síti:       http://${LAN_IP}:${HTTP_PORT}"
fi

# --- Spuštění HTTPS ------------------------------------------------
if [ "$START_HTTPS" = true ]; then
    nohup setsid uvicorn app.main:app \
        --host 0.0.0.0 \
        --port "$HTTPS_PORT" \
        --ssl-keyfile key.pem \
        --ssl-certfile cert.pem \
        < /dev/null >> "$LOG_FILE" 2>&1 &
    sleep 1
    ok "HTTPS server: https://localhost:${HTTPS_PORT}"
    ok "V síti:       https://${LAN_IP}:${HTTPS_PORT}  ← vhodné pro mobilní skener kamery"
fi
disown -a 2>/dev/null || true

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${CYAN}📋${NC} Logy:      tail -f $LOG_FILE"
echo -e "${CYAN}🛑${NC} Zastavení: $0 --stop"
echo ""
