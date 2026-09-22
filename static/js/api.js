/**
 * Knihovna API Client
 * Komunikace s FastAPI backendem
 */

const API = {
  baseUrl: '',

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };

    const config = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...(options.headers || {})
      }
    };

    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body);
    }

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        let errDetail = 'Došlo k chybě při komunikaci se serverem.';
        try {
          const errJson = await response.json();
          if (errJson.detail) errDetail = errJson.detail;
        } catch (_) {}
        throw new Error(errDetail);
      }
      return await response.json();
    } catch (error) {
      console.error(`API Error [${endpoint}]:`, error);
      throw error;
    }
  },

  // Síťové informace (LAN IP pro mobil)
  getNetworkInfo() {
    return this.request('/api/network-info');
  },

  // Police
  getShelves() {
    return this.request('/api/shelves');
  },

  getShelf(id) {
    return this.request(`/api/shelves/${id}`);
  },

  updateShelf(id, data) {
    return this.request(`/api/shelves/${id}`, {
      method: 'PUT',
      body: data
    });
  },

  // Knihy
  getBooks(params = {}) {
    const query = new URLSearchParams();
    if (params.search) query.set('search', params.search);
    if (params.shelfId) query.set('shelf_id', params.shelfId);
    if (params.genre) query.set('genre', params.genre);
    if (params.limit) query.set('limit', params.limit);
    if (params.offset) query.set('offset', params.offset);

    const queryString = query.toString() ? `?${query.toString()}` : '';
    return this.request(`/api/books${queryString}`);
  },

  getBook(id) {
    return this.request(`/api/books/${id}`);
  },

  createBook(bookData) {
    return this.request('/api/books', {
      method: 'POST',
      body: bookData
    });
  },

  updateBook(id, bookData) {
    return this.request(`/api/books/${id}`, {
      method: 'PUT',
      body: bookData
    });
  },

  deleteBook(id) {
    return this.request(`/api/books/${id}`, {
      method: 'DELETE'
    });
  },

  // Dohledání ISBN z databází
  lookupISBN(isbn) {
    return this.request(`/api/lookup/${encodeURIComponent(isbn)}`);
  },

  // Automatické vyvážení polic
  autoOrganize() {
    return this.request('/api/shelves/auto-organize', {
      method: 'POST'
    });
  },

  // Re-seed ukázkových dat
  seedData() {
    return this.request('/api/seed', {
      method: 'POST'
    });
  }
};
