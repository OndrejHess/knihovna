/**
 * Knihovna - Hlavní řídicí modul aplikace
 */

const App = {
  currentTab: 'shelves',

  async init() {
    console.log('Inicializuji aplikaci Knihovna...');

    // Inicializace podmodulů
    Books.initSearch();
    this.bindEvents();

    // Načtení dat polic
    await Shelves.loadShelves();
    await this.fetchNetworkInfo();
  },

  bindEvents() {
    // Klávesové zkratky (Escape pro zavření modálů)
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.closeAllModals();
      }
    });

    // Zavření modálu klikem na podklad
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
          this.closeModal(overlay.id);
        }
      });
    });

    // Formulář pro přidání knihy
    const addForm = document.getElementById('add-book-form');
    if (addForm) {
      addForm.addEventListener('submit', (e) => Books.saveNewBook(e));
    }

    // Formulář pro editaci police
    const shelfForm = document.getElementById('shelf-edit-form');
    if (shelfForm) {
      shelfForm.addEventListener('submit', (e) => {
        e.preventDefault();
        Shelves.saveShelfEdit();
      });
    }

    // Tlačítko skenování v manuálním ISBN poli
    const manualBtn = document.getElementById('btn-manual-lookup');
    const manualInput = document.getElementById('manual-isbn-input');
    if (manualBtn && manualInput) {
      manualBtn.addEventListener('click', () => {
        Scanner.processISBN(manualInput.value);
      });
      manualInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          Scanner.processISBN(manualInput.value);
        }
      });
    }
  },

  switchTab(tabName) {
    this.currentTab = tabName;

    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    const shelvesGrid = document.getElementById('shelves-grid-container');
    const shelfDetail = document.getElementById('shelf-detail-view');
    const catalogView = document.getElementById('catalog-view-container');

    if (tabName === 'shelves') {
      if (Shelves.currentShelfId) {
        shelfDetail.style.display = 'flex';
        shelvesGrid.style.display = 'none';
      } else {
        shelfDetail.style.display = 'none';
        shelvesGrid.style.display = 'grid';
      }
      catalogView.style.display = 'none';
    } else if (tabName === 'catalog') {
      shelvesGrid.style.display = 'none';
      shelfDetail.style.display = 'none';
      catalogView.style.display = 'block';
      Books.loadCatalog();
    }
  },

  openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.add('active');
    }
  },

  closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.remove('active');
    }
    if (modalId === 'modal-scanner') {
      Scanner.stopScanner();
    }
  },

  closeAllModals() {
    document.querySelectorAll('.modal-overlay').forEach(modal => {
      modal.classList.remove('active');
    });
    Scanner.stopScanner();
  },

  openScannerModal() {
    this.openModal('modal-scanner');
    Scanner.startScanner('reader');
  },

  async fetchNetworkInfo() {
    try {
      const net = await API.getNetworkInfo();
      const mobileBtn = document.getElementById('btn-mobile-connect');
      if (mobileBtn && net.lan_ip) {
        mobileBtn.title = `Mobilní přístup: ${net.url}`;
      }
      this.networkInfo = net;
    } catch (_) {}
  },

  currentMobileMode: 'http',

  openMobileConnectModal() {
    if (!this.networkInfo) {
      this.showToast('Nelze načíst síťové informace.', 'error');
      return;
    }
    this.showMobileUrlMode(this.currentMobileMode || 'http');
    this.openModal('modal-mobile-connect');
  },

  showMobileUrlMode(mode) {
    this.currentMobileMode = mode;
    const httpBtn = document.getElementById('tab-connect-http');
    const httpsBtn = document.getElementById('tab-connect-https');
    const urlDisplay = document.getElementById('lan-url-text');
    const qrContainer = document.getElementById('lan-qr-canvas');
    const expl = document.getElementById('lan-mode-expl');

    if (httpBtn) httpBtn.classList.toggle('active', mode === 'http');
    if (httpsBtn) httpsBtn.classList.toggle('active', mode === 'https');

    const targetUrl = (mode === 'https' && this.networkInfo.https_url) 
      ? this.networkInfo.https_url 
      : this.networkInfo.url;

    if (urlDisplay) urlDisplay.textContent = targetUrl;

    if (expl) {
      if (mode === 'http') {
        expl.innerHTML = '⚡ <strong>Na HTTP:</strong> Otevře se ihned bez varování. Ve skeneru použijte tlačítko <em>„📸 Vyfotit kód fotoaparátem“</em>.';
      } else {
        expl.innerHTML = '🔒 <strong>Na HTTPS:</strong> Umožňuje nepřetržité živé video. V prohlížeči telefonu stačí potvrdit <em>„Pokročilé → Přesto pokračovat“</em> (pro vlastní certifikát).';
      }
    }

    // Generování QR kódu
    if (qrContainer) {
      qrContainer.innerHTML = '';
      if (typeof QRCode !== 'undefined') {
        new QRCode(qrContainer, {
          text: targetUrl,
          width: 180,
          height: 180,
          colorDark: "#0f172a",
          colorLight: "#ffffff",
          correctLevel: QRCode.CorrectLevel.M
        });
      } else {
        qrContainer.innerHTML = `<img src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=${encodeURIComponent(targetUrl)}" alt="QR kód" width="180" height="180">`;
      }
    }
  },

  copyMobileUrl() {
    const targetUrl = (this.currentMobileMode === 'https' && this.networkInfo.https_url)
      ? this.networkInfo.https_url
      : (this.networkInfo ? this.networkInfo.url : '');

    if (targetUrl) {
      navigator.clipboard.writeText(targetUrl).then(() => {
        this.showToast('Odkaz zkopírován do schránky!', 'success');
      });
    }
  },

  async runAutoOrganize() {
    if (!confirm('Spustit inteligentní vyvážení knihovny?\n\nKnihy budou optimálně rozděleny do 16 polic podle žánrů, autorů a abecedy tak, aby žádná police nebyla přeplněna (cíl ~35 knih, max 40).')) {
      return;
    }

    this.showToast('Provádím organizaci a vyvažování polic...', 'info');

    try {
      const res = await API.autoOrganize();
      this.showToast(res.summary || 'Knihovna byla úspěšně uspořádána!', 'success');
      await Shelves.loadShelves();

      // Zobrazit report v modálu
      const reportContent = document.getElementById('organize-report-content');
      if (reportContent && res.shelf_stats) {
        reportContent.innerHTML = `
          <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid var(--success); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1rem; color: #a7f3d0;">
            <strong>Výsledek:</strong> ${res.summary}
          </div>
          <h4 style="margin-bottom: 0.75rem; color: #fff;">Přehled zaplnění po optimalizaci:</h4>
          <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 0.75rem;">
            ${res.shelf_stats.map(s => `
              <div style="background: var(--bg-card); padding: 0.75rem; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
                <div style="font-weight: 600; font-size: 0.85rem; color: #fff;">${s.shelf_name}</div>
                <div style="font-size: 0.8rem; color: var(--text-muted);">${s.book_count} knih (${s.status})</div>
              </div>
            `).join('')}
          </div>
        `;
        this.openModal('modal-organize-report');
      }
    } catch (err) {
      this.showToast('Chyba při automatickém uspořádání: ' + err.message, 'error');
    }
  },

  exportData(format) {
    window.location.href = `/api/export?format=${format}`;
  },

  async seedSampleData() {
    if (!confirm('Chcete načíst ukázkovou sadu knih pro demonstraci všech 16 polic?')) return;
    try {
      await API.seedData();
      this.showToast('Ukázkové knihy byly načteny!', 'success');
      await Shelves.loadShelves();
    } catch (err) {
      this.showToast('Chyba: ' + err.message, 'error');
    }
  },

  showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    if (type === 'error') icon = '⚠️';

    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }
};

// Spuštění při načtení stránky
document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
