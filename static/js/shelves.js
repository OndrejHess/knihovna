/**
 * Knihovna - Správa a vizualizace 16 poliček
 */

const Shelves = {
  shelvesData: [],
  currentShelfId: null,

  async loadShelves() {
    try {
      this.shelvesData = await API.getShelves();
      this.renderGrid();
      this.updateTotalStats();
    } catch (err) {
      App.showToast('Chyba při načítání polic: ' + err.message, 'error');
    }
  },

  updateTotalStats() {
    let totalBooks = 0;
    let totalCapacity = 0;

    this.shelvesData.forEach(s => {
      totalBooks += s.book_count || 0;
      totalCapacity += s.capacity_max || 40;
    });

    const statBooksEl = document.getElementById('stat-total-books');
    const statCapEl = document.getElementById('stat-total-capacity');
    const statOccEl = document.getElementById('stat-occupancy-rate');

    if (statBooksEl) statBooksEl.textContent = totalBooks;
    if (statCapEl) statCapEl.textContent = totalCapacity;
    if (statOccEl) {
      const pct = totalCapacity > 0 ? Math.round((totalBooks / totalCapacity) * 100) : 0;
      statOccEl.textContent = `${pct} %`;
    }
  },

  renderGrid() {
    const gridContainer = document.getElementById('shelves-grid-container');
    if (!gridContainer) return;

    if (!this.shelvesData || this.shelvesData.length === 0) {
      gridContainer.innerHTML = '<div class="empty-state">Žádné police k zobrazení.</div>';
      return;
    }

    gridContainer.innerHTML = this.shelvesData.map(shelf => {
      const count = shelf.book_count || 0;
      const maxCap = shelf.capacity_max || 40;
      const minCap = shelf.capacity_min || 30;
      const pct = Math.min(100, Math.round((count / maxCap) * 100));

      let badgeClass = 'badge-gray';
      let fillClass = '';
      if (count === 0) {
        badgeClass = 'badge-gray';
      } else if (count < minCap) {
        badgeClass = 'badge-emerald';
      } else if (count <= maxCap) {
        badgeClass = 'badge-amber';
      } else {
        badgeClass = 'badge-rose';
        fillClass = 'status-rose';
      }

      // Vizuální hřbety knih v náhledu (až 20 zmenšených proužků)
      let spinesHtml = '';
      if (count > 0) {
        const spineCount = Math.min(count, 28);
        for (let i = 0; i < spineCount; i++) {
          const heightPct = 65 + ((i * 7) % 35);
          spinesHtml += `<div class="book-spine-mini" style="height: ${heightPct}%; background-color: ${shelf.color || 'var(--primary)'};"></div>`;
        }
      } else {
        spinesHtml = `<div class="shelf-empty-hint">Police je zatím prázdná</div>`;
      }

      return `
        <div class="shelf-card" id="shelf-card-${shelf.id}" style="--shelf-color: ${shelf.color || '#6366f1'};" onclick="Shelves.openShelfDetail(${shelf.id})">
          <div class="shelf-header">
            <div class="shelf-title-wrap">
              <div class="shelf-icon-badge">${shelf.icon || '📚'}</div>
              <div class="shelf-info">
                <h3>${shelf.name}</h3>
                <span class="shelf-theme">${shelf.theme}</span>
              </div>
            </div>
            <span class="shelf-number-badge">#${shelf.id}</span>
          </div>

          <div class="shelf-books-preview">
            ${spinesHtml}
          </div>

          <div class="shelf-capacity">
            <div class="capacity-labels">
              <span class="capacity-count">${count} / ${maxCap} knih</span>
              <span class="capacity-badge ${badgeClass}">${shelf.status_badge || `${count} knih`}</span>
            </div>
            <div class="progress-track">
              <div class="progress-fill ${fillClass}" style="width: ${pct}%;"></div>
            </div>
          </div>
        </div>
      `;
    }).join('');
  },

  async openShelfDetail(shelfId) {
    this.currentShelfId = shelfId;
    try {
      const shelf = await API.getShelf(shelfId);
      const viewContainer = document.getElementById('shelf-detail-view');
      const gridContainer = document.getElementById('shelves-grid-container');
      const controlsPanel = document.getElementById('controls-panel');

      if (!viewContainer) return;

      gridContainer.style.display = 'none';
      if (controlsPanel) controlsPanel.style.display = 'none';
      viewContainer.style.display = 'flex';

      const books = shelf.books || [];
      const booksHtml = books.length > 0 ? books.map(b => {
        const cover = b.cover_url ? `<img src="${b.cover_url}" alt="${b.title}" class="book-cover-img" loading="lazy">` : `<span class="book-cover-placeholder">📖</span>`;
        const genres = (b.genres_list || []).slice(0, 3).map(g => `<span class="genre-tag">${g}</span>`).join('');
        const rating = b.rating ? `<span class="rating-badge">★ ${b.rating.toFixed(1)}</span>` : '';

        return `
          <div class="book-card" id="book-card-${b.id}" onclick="Books.openBookDetail(${b.id})">
            <div class="book-cover-wrap">
              ${cover}
            </div>
            <div class="book-meta">
              <h4>${b.title}</h4>
              <p class="book-author">${b.author}</p>
            </div>
            <div class="book-badges">
              ${rating}
              ${genres}
            </div>
          </div>
        `;
      }).join('') : '<div class="empty-state" style="grid-column: 1 / -1; padding: 3rem; text-align: center; color: var(--text-muted);">V této polici zatím nejsou žádné knihy. Přidejte knihu pomocí skeneru nebo tlačítka "Přidat knihu".</div>';

      viewContainer.innerHTML = `
        <div class="shelf-detail-header" style="border-left: 5px solid ${shelf.color || 'var(--primary)'};">
          <div class="shelf-detail-title">
            <div class="shelf-icon-badge" style="font-size: 1.8rem; width: 48px; height: 48px;">${shelf.icon || '📚'}</div>
            <div>
              <h2 style="font-size: 1.4rem; color: #fff;">${shelf.name}</h2>
              <p style="color: var(--text-muted); font-size: 0.9rem;">${shelf.notes || shelf.theme} • <strong>${books.length} / ${shelf.capacity_max} knih</strong></p>
            </div>
          </div>
          <div class="shelf-detail-actions">
            <button class="btn btn-secondary" onclick="Shelves.openShelfEditModal(${shelf.id})">⚙️ Upravit polici</button>
            <button class="btn btn-primary" onclick="Shelves.closeShelfDetail()">← Zpět na přehled knihovny</button>
          </div>
        </div>

        <div class="shelf-books-grid">
          ${booksHtml}
        </div>
      `;

      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      App.showToast('Chyba při načítání detailu police: ' + err.message, 'error');
    }
  },

  closeShelfDetail() {
    this.currentShelfId = null;
    const viewContainer = document.getElementById('shelf-detail-view');
    const gridContainer = document.getElementById('shelves-grid-container');
    const controlsPanel = document.getElementById('controls-panel');

    if (viewContainer) viewContainer.style.display = 'none';
    if (gridContainer) gridContainer.style.display = 'grid';
    if (controlsPanel) controlsPanel.style.display = 'flex';
    this.loadShelves();
  },

  openShelfEditModal(shelfId) {
    const shelf = this.shelvesData.find(s => s.id === shelfId);
    if (!shelf) return;

    document.getElementById('edit-shelf-id').value = shelf.id;
    document.getElementById('edit-shelf-name').value = shelf.name;
    document.getElementById('edit-shelf-theme').value = shelf.theme;
    document.getElementById('edit-shelf-icon').value = shelf.icon || '📚';
    document.getElementById('edit-shelf-color').value = shelf.color || '#6366f1';
    document.getElementById('edit-shelf-min').value = shelf.capacity_min || 30;
    document.getElementById('edit-shelf-max').value = shelf.capacity_max || 40;
    document.getElementById('edit-shelf-notes').value = shelf.notes || '';

    App.openModal('modal-shelf-edit');
  },

  async saveShelfEdit() {
    const id = parseInt(document.getElementById('edit-shelf-id').value);
    const data = {
      name: document.getElementById('edit-shelf-name').value.trim(),
      theme: document.getElementById('edit-shelf-theme').value.trim(),
      icon: document.getElementById('edit-shelf-icon').value.trim(),
      color: document.getElementById('edit-shelf-color').value.trim(),
      capacity_min: parseInt(document.getElementById('edit-shelf-min').value) || 30,
      capacity_max: parseInt(document.getElementById('edit-shelf-max').value) || 40,
      notes: document.getElementById('edit-shelf-notes').value.trim()
    };

    try {
      await API.updateShelf(id, data);
      App.closeModal('modal-shelf-edit');
      App.showToast('Police byla úspěšně upravena.', 'success');
      await this.loadShelves();
      if (this.currentShelfId === id) {
        this.openShelfDetail(id);
      }
    } catch (err) {
      App.showToast('Chyba při ukládání police: ' + err.message, 'error');
    }
  }
};
