/**
 * Knihovna - Barcode Scanner & ISBN Lookup
 * Obsluha kamery, detekce čárových kódů EAN-13/ISBN, podpora přímého focení a zvukový signál
 */

const Scanner = {
  isScanning: false,
  html5QrCode: null,
  videoStream: null,
  audioCtx: null,
  currentFacingMode: 'environment',

  // Inicializace zvukového syntetizátoru pro pípnutí při naskenování
  playBeep() {
    try {
      if (!this.audioCtx) {
        this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (this.audioCtx.state === 'suspended') {
        this.audioCtx.resume();
      }
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(880, this.audioCtx.currentTime); // Komorní A (880 Hz)
      gain.gain.setValueAtTime(0.15, this.audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, this.audioCtx.currentTime + 0.15);
      osc.connect(gain);
      gain.connect(this.audioCtx.destination);
      osc.start();
      osc.stop(this.audioCtx.currentTime + 0.15);
    } catch (e) {
      console.warn('Zvukový efekt nelze přehrát:', e);
    }
  },

  // Vyvolání nativního fotoaparátu mobilu přes HTML5 file capture
  triggerPhotoCapture() {
    const fileInput = document.getElementById('barcode-file-input');
    if (fileInput) {
      fileInput.value = '';
      fileInput.click();
    }
  },

  // Zpracování vyfoceného snímku z fotoaparátu
  async handlePhotoFile(event) {
    const file = event.target.files && event.target.files[0];
    if (!file) return;

    App.showToast('Analyzuji fotografii čárového kódu...', 'info');

    // 1. Zkusíme Html5Qrcode.scanFile
    try {
      if (!this.html5QrCode) {
        this.html5QrCode = new Html5Qrcode('reader');
      }
      const decodedText = await this.html5QrCode.scanFile(file, true);
      if (decodedText) {
        this.onBarcodeDetected(decodedText);
        return;
      }
    } catch (err) {
      console.warn('Html5Qrcode scanFile selhalo, zkouším BarcodeDetector fallback:', err);
    }

    // 2. Fallback přes nativní BarcodeDetector na ImageBitmap
    if ('BarcodeDetector' in window) {
      try {
        const bitmap = await createImageBitmap(file);
        const detector = new BarcodeDetector({ formats: ['ean_13', 'ean_8', 'code_128', 'upc_a'] });
        const barcodes = await detector.detect(bitmap);
        if (barcodes.length > 0) {
          this.onBarcodeDetected(barcodes[0].rawValue);
          return;
        }
      } catch (err2) {
        console.warn('BarcodeDetector fallback selhal:', err2);
      }
    }

    App.showToast('Čárový kód se nepodařilo rozpoznat. Zkuste vyfotit kód zblízka, ostře a vodorovně.', 'error');
  },

  // Spuštění živého skeneru z kamery
  async startScanner(containerId = 'reader') {
    const container = document.getElementById(containerId);
    if (!container) return;

    const isSecure = window.isSecureContext || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    const httpNotice = document.getElementById('scanner-http-notice');
    const switchBtn = document.getElementById('btn-switch-cam');

    if (!isSecure) {
      // V nezabezpečeném HTTP kontextu mobilní prohlížeče blokují přímý video stream
      if (httpNotice) httpNotice.style.display = 'block';
      if (switchBtn) switchBtn.style.display = 'none';
      console.info('HTTP kontext: pro mobil je doporučeno přímé vyfocení kódu.');
      return;
    }

    if (httpNotice) httpNotice.style.display = 'none';
    if (switchBtn) switchBtn.style.display = 'inline-flex';
    this.isScanning = true;

    // Pokud je k dispozici Html5Qrcode knihovna
    if (typeof Html5Qrcode !== 'undefined') {
      try {
        if (!this.html5QrCode) {
          this.html5QrCode = new Html5Qrcode(containerId);
        }

        const config = {
          fps: 15,
          qrbox: { width: 260, height: 160 },
          aspectRatio: 1.333334,
          formatsToSupport: [
            Html5QrcodeSupportedFormats.EAN_13,
            Html5QrcodeSupportedFormats.EAN_8,
            Html5QrcodeSupportedFormats.CODE_128,
            Html5QrcodeSupportedFormats.UPC_A
          ]
        };

        await this.html5QrCode.start(
          { facingMode: this.currentFacingMode },
          config,
          (decodedText) => {
            this.onBarcodeDetected(decodedText);
          },
          () => {}
        );
        return;
      } catch (err) {
        console.warn('Html5Qrcode live start selhal:', err);
      }
    }

    // Fallback na nativní MediaDevices + BarcodeDetector API
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      try {
        const constraints = {
          video: {
            facingMode: this.currentFacingMode,
            width: { ideal: 1280 },
            height: { ideal: 720 }
          }
        };
        this.videoStream = await navigator.mediaDevices.getUserMedia(constraints);
        const videoEl = document.getElementById('scanner-video');
        if (videoEl) {
          videoEl.srcObject = this.videoStream;
          videoEl.play();
          this.runBarcodeDetectorLoop(videoEl);
        }
      } catch (e) {
        console.warn('Nativní video stream nelze spustit:', e);
        if (httpNotice) httpNotice.style.display = 'block';
      }
    } else {
      if (httpNotice) httpNotice.style.display = 'block';
    }
  },

  // Smyčka pro nativní BarcodeDetector API
  async runBarcodeDetectorLoop(videoEl) {
    if (!('BarcodeDetector' in window)) return;
    try {
      const barcodeDetector = new BarcodeDetector({ formats: ['ean_13', 'ean_8', 'code_128'] });
      const detect = async () => {
        if (!this.isScanning) return;
        try {
          const barcodes = await barcodeDetector.detect(videoEl);
          if (barcodes.length > 0) {
            this.onBarcodeDetected(barcodes[0].rawValue);
            return;
          }
        } catch (_) {}
        requestAnimationFrame(detect);
      };
      requestAnimationFrame(detect);
    } catch (err) {
      console.warn('BarcodeDetector API není podporováno:', err);
    }
  },

  // Zastavení skeneru a uvolnění kamery
  async stopScanner() {
    this.isScanning = false;
    if (this.html5QrCode) {
      try {
        await this.html5QrCode.stop();
      } catch (_) {}
    }
    if (this.videoStream) {
      this.videoStream.getTracks().forEach(track => track.stop());
      this.videoStream = null;
    }
  },

  // Přepnutí přední a zadní kamery
  async switchCamera() {
    this.currentFacingMode = this.currentFacingMode === 'environment' ? 'user' : 'environment';
    await this.stopScanner();
    await this.startScanner();
  },

  // Reakce na úspěšně detekovaný kód
  async onBarcodeDetected(code) {
    this.playBeep();
    App.showToast(`Kód detekován: ${code}`, 'info');

    // Automaticky spustíme vyhledání knihy
    await this.processISBN(code);
  },

  // Zpracování zadaného nebo naskenovaného ISBN
  async processISBN(rawIsbn) {
    const cleanIsbn = rawIsbn.replace(/[^0-9Xx]/g, '').trim();
    if (!cleanIsbn || cleanIsbn.length < 8) {
      App.showToast('Zadejte platné ISBN nebo EAN kód knihy.', 'error');
      return;
    }

    App.showToast('Vyhledávám knihu v databázích...', 'info');

    try {
      const bookData = await API.lookupISBN(cleanIsbn);
      // Zastavíme kameru a zavřeme skener
      await this.stopScanner();
      App.closeModal('modal-scanner');
      // Otevřeme dialog pro potvrzení a přidání knihy
      Books.showAddBookModalWithData(bookData);
      App.showToast(`Nalezena: ${bookData.title}`, 'success');
    } catch (err) {
      App.showToast(`Kniha nebyla v online databázích nalezena. Můžete ji zadat ručně.`, 'error');
      await this.stopScanner();
      App.closeModal('modal-scanner');
      Books.showAddBookModalWithData({
        isbn: cleanIsbn,
        title: '',
        author: '',
        genres: []
      });
    }
  }
};
