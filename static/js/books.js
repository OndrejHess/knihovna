/**
 * Knihovna - Správa knih, vyhledávání, filtry a formuláře
 */

const Books = {
  booksList: [],
  currentBook: null,
  searchTimeout: null,

  initSearch() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        clearTimeout(this.searchTimeout);
        this.searchTimeout = setTimeout(() => {
          this.handleSearch(e.target.value);
        }, 250);
      });
    }
  },

  async handleSearch(query) {
    const q = query.trim();
    if (!q) {
      // Pokud je prázdné vyhledávání, vrátíme se na aktuální záložku
      if (App.currentTab === 'shelves') {
        document.getElementById('shelves-grid-container').style.display = 'grid';
        document.getElementById('catalog-view-container').style.display = 'none';
      } else {
        this.loadCatalog();
      }
      return;
    }

    // Při vyhledávání přepneme do katalogového zobrazení výsledků
    document.getElementById('shelves-grid-container').style.display = 'none';
    document.getElementById('shelf-detail-view').style.display = 'none';
    const catalogContainer = document.getElementById('catalog-view-container');
    catalogContainer.style.display = 'block';

    try {
      const results = await API.getBooks({ search: q, limit: 100 });
      this.renderCatalog(results, `Výsledky hledání pro: "${q}" (${results.length} nalezeno)`);
    } catch (err) {
      App.showToast('Chyba při vyhledávání: ' + err.message, 'error');
    }
  },

  async loadCatalog() {
    try {
      const books = await API.getBooks({ limit: 500 });
      this.booksList = books;
      this.renderCatalog(books, `Všechny knihy (${books.length})`);
    } catch (err) {
      App.showToast('Chyba při načítání katalogu: ' + err.message, 'error');
    }
  },

  renderCatalog(books, titleText = '') {
    const catalogContainer = document.getElementById('catalog-view-container');
    if (!catalogContainer) return;

    if (books.length === 0) {
      catalogContainer.innerHTML = `
        <div class="empty-state" style="padding: 4rem 2rem; text-align: center; color: var(--text-muted);">
          <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
          <h3>Nebyly nalezeny žádné knihy</h3>
          <p>Zkuste upravit vyhledávaný výraz nebo přidejte novou knihu.</p>
        </div>
      `;
      return;
    }

    const cardsHtml = books.map(b => {
      const cover = b.cover_url ? `<img src="${b.cover_url}" alt="${b.title}" class="book-cover-img" loading="lazy">` : `<span class="book-cover-placeholder">📖</span>`;
      const genres = (b.genres_list || []).slice(0, 2).map(g => `<span class="genre-tag">${g}</span>`).join('');
      const rating = b.rating ? `<span class="rating-badge">★ ${b.rating.toFixed(1)}</span>` : '';
      const shelfName = b.shelf_name ? `<span class="genre-tag" style="background: rgba(99, 102, 241, 0.2); color: #a5b4fc;">${b.shelf_icon || ''} ${b.shelf_name.split(':')[0]}</span>` : '';

      return `
        <div class="book-card" id="catalog-book-${b.id}" onclick="Books.openBookDetail(${b.id})">
          <div class="book-cover-wrap">
            ${cover}
          </div>
          <div class="book-meta">
            <h4>${b.title}</h4>
            <p class="book-author">${b.author}</p>
          </div>
          <div class="book-badges">
            ${rating}
            ${shelfName}
            ${genres}
          </div>
        </div>
      `;
    }).join('');

    catalogContainer.innerHTML = `
      <div style="margin-bottom: 1.25rem; display: flex; justify-content: space-between; align-items: center;">
        <h2 style="font-size: 1.3rem; color: #fff;">${titleText}</h2>
      </div>
      <div class="shelf-books-grid">
        ${cardsHtml}
      </div>
    `;
  },

  populateShelfSelectOptions(selectElementId, selectedId = 1) {
    const select = document.getElementById(selectElementId);
    if (!select) return;

    select.innerHTML = Shelves.shelvesData.map(s => {
      return `<option value="${s.id}" ${s.id === selectedId ? 'selected' : ''}>${s.icon || ''} ${s.name} (${s.book_count || 0}/${s.capacity_max || 40})</option>`;
    }).join('');
  },

  openAddBookModal() {
    this.populateShelfSelectOptions('add-book-shelf', 1);
    document.getElementById('add-book-form').reset();
    document.getElementById('add-book-id').value = '';
    document.getElementById('add-shelf-suggestion').style.display = 'none';
    App.openModal('modal-add-book');
  },

  showAddBookModalWithData(data) {
    this.openAddBookModal();

    document.getElementById('add-book-isbn').value = data.isbn || '';
    document.getElementById('add-book-title').value = data.title || '';
    document.getElementById('add-book-author').value = data.author || '';
    document.getElementById('add-book-publisher').value = data.publisher || '';
    document.getElementById('add-book-year').value = data.year || '';
    document.getElementById('add-book-pages').value = data.page_count || '';
    document.getElementById('add-book-rating').value = data.rating || '';
    document.getElementById('add-book-cover').value = data.cover_url || '';
    document.getElementById('add-book-desc').value = data.description || '';

    const genresStr = Array.isArray(data.genres) ? data.genres.join(', ') : (data.genres || '');
    document.getElementById('add-book-genres').value = genresStr;

    // Doporučená police
    const suggestionEl = document.getElementById('add-shelf-suggestion');
    if (data.suggested_shelf_id) {
      this.populateShelfSelectOptions('add-book-shelf', data.suggested_shelf_id);
      suggestionEl.style.display = 'inline-flex';
      suggestionEl.innerHTML = `✨ Doporučená police: <strong>${data.suggested_shelf_name || `Police ${data.suggested_shelf_id}`}</strong>`;
    } else {
      suggestionEl.style.display = 'none';
    }
  },

  async saveNewBook(e) {
    e.preventDefault();

    const genresRaw = document.getElementById('add-book-genres').value;
    const genres = genresRaw ? genresRaw.split(',').map(g => g.trim()).filter(Boolean) : [];

    const payload = {
      isbn: document.getElementById('add-book-isbn').value.trim(),
      title: document.getElementById('add-book-title').value.trim(),
      author: document.getElementById('add-book-author').value.trim(),
      genres: genres,
      description: document.getElementById('add-book-desc').value.trim(),
      cover_url: document.getElementById('add-book-cover').value.trim(),
      publisher: document.getElementById('add-book-publisher').value.trim(),
      year: parseInt(document.getElementById('add-book-year').value) || null,
      page_count: parseInt(document.getElementById('add-book-pages').value) || null,
      rating: parseFloat(document.getElementById('add-book-rating').value) || 0.0,
      shelf_id: parseInt(document.getElementById('add-book-shelf').value) || 1,
      notes: document.getElementById('add-book-notes').value.trim()
    };

    if (!payload.title || !payload.author) {
      App.showToast('Vyplňte prosím alespoň název a autora knihy.', 'error');
      return;
    }

    try {
      const created = await API.createBook(payload);
      App.closeModal('modal-add-book');
      App.showToast(`Kniha "${created.title}" byla uložena do ${created.shelf_name || 'police'}!`, 'success');
      await Shelves.loadShelves();
      if (Shelves.currentShelfId) {
        Shelves.openShelfDetail(Shelves.currentShelfId);
      }
    } catch (err) {
      App.showToast('Chyba při ukládání knihy: ' + err.message, 'error');
    }
  },

  async openBookDetail(bookId) {
    try {
      const book = await API.getBook(bookId);
      this.currentBook = book;

      document.getElementById('detail-book-title').textContent = book.title;
      document.getElementById('detail-book-author').textContent = book.author;
      document.getElementById('detail-book-isbn').textContent = book.isbn || 'Neuvedeno';
      document.getElementById('detail-book-publisher').textContent = book.publisher || 'Neuvedeno';
      document.getElementById('detail-book-year').textContent = book.year || 'Neuvedeno';
      document.getElementById('detail-book-pages').textContent = book.page_count ? `${book.page_count} stran` : 'Neuvedeno';
      document.getElementById('detail-book-desc').textContent = book.description || 'Bez popisu.';

      const coverContainer = document.getElementById('detail-book-cover');
      if (book.cover_url) {
        coverContainer.innerHTML = `<img src="${book.cover_url}" alt="${book.title}">`;
      } else {
        coverContainer.innerHTML = `<span style="font-size: 4rem;">📖</span>`;
      }

      const genresContainer = document.getElementById('detail-book-genres');
      genresContainer.innerHTML = (book.genres_list || []).map(g => `<span class="genre-tag">${g}</span>`).join('') || '<span class="genre-tag">Bez žánru</span>';

      const ratingContainer = document.getElementById('detail-book-rating');
      if (book.rating) {
        ratingContainer.innerHTML = `★ <strong>${book.rating.toFixed(1)}</strong> / 5.0`;
      } else {
        ratingContainer.textContent = 'Nehodnoceno';
      }

      // Výběr police pro přesun
      this.populateShelfSelectOptions('detail-book-shelf-select', book.shelf_id);

      App.openModal('modal-book-detail');
    } catch (err) {
      App.showToast('Chyba při načítání knihy: ' + err.message, 'error');
    }
  },

  async moveCurrentBookShelf() {
    if (!this.currentBook) return;
    const newShelfId = parseInt(document.getElementById('detail-book-shelf-select').value);
    if (newShelfId === this.currentBook.shelf_id) {
      App.showToast('Kniha se již v této polici nachází.', 'info');
      return;
    }

    try {
      await API.updateBook(this.currentBook.id, { shelf_id: newShelfId });
      App.showToast(`Kniha přesunuta do police #${newShelfId}`, 'success');
      App.closeModal('modal-book-detail');
      await Shelves.loadShelves();
      if (Shelves.currentShelfId) {
        Shelves.openShelfDetail(Shelves.currentShelfId);
      }
    } catch (err) {
      App.showToast('Chyba při přesunu knihy: ' + err.message, 'error');
    }
  },

  async deleteCurrentBook() {
    if (!this.currentBook) return;
    if (!confirm(`Opravdu si přejete smazat knihu "${this.currentBook.title}"?`)) return;

    try {
      await API.deleteBook(this.currentBook.id);
      App.closeModal('modal-book-detail');
      App.showToast('Kniha byla úspěšně smazána.', 'success');
      await Shelves.loadShelves();
      if (Shelves.currentShelfId) {
        Shelves.openShelfDetail(Shelves.currentShelfId);
      } else if (App.currentTab === 'catalog') {
        this.loadCatalog();
      }
    } catch (err) {
      App.showToast('Chyba při mazání knihy: ' + err.message, 'error');
    }
  }
};
