// Service Worker for W3 PWA
// NOTE: Update CACHE_VERSION whenever you change cached assets (ASSETS_TO_CACHE)
// or make changes that should force clients to refresh their cached content.
const CACHE_VERSION = 'v4';
const CACHE_NAME = `w3-pwa-${CACHE_VERSION}`;
const OFFLINE_URL = 'offline.html';

// Failed cache tracking with retry
// Persist retry state because service workers can be terminated and restarted at any time.
const RETRY_QUEUE_DB_NAME = 'w3-pwa-retry-queue';
const RETRY_QUEUE_STORE_NAME = 'failedCacheQueue';

class PersistentFailedCacheQueue {
  constructor() {
    this.map = new Map(); // url -> { attempts, lastAttempt, request }
    this.dbPromise = this.openDb();
    this.ready = this.loadFromDb();
  }

  openDb() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(RETRY_QUEUE_DB_NAME, 1);
      request.onupgradeneeded = () => {
        const db = request.result;
        if (!db.objectStoreNames.contains(RETRY_QUEUE_STORE_NAME)) {
          db.createObjectStore(RETRY_QUEUE_STORE_NAME, { keyPath: 'url' });
        }
      };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async loadFromDb() {
    try {
      const db = await this.dbPromise;
      await new Promise((resolve, reject) => {
        const tx = db.transaction(RETRY_QUEUE_STORE_NAME, 'readonly');
        const store = tx.objectStore(RETRY_QUEUE_STORE_NAME);
        const request = store.getAll();
        request.onsuccess = () => {
          for (const entry of request.result) {
            this.map.set(entry.url, entry.value);
          }
          resolve();
        };
        request.onerror = () => reject(request.error);
      });
    } catch (error) {
      console.error('[SW] Failed to restore retry queue from IndexedDB:', error);
    }
  }

  async persistEntry(url, value) {
    try {
      const db = await this.dbPromise;
      await new Promise((resolve, reject) => {
        const tx = db.transaction(RETRY_QUEUE_STORE_NAME, 'readwrite');
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
        tx.objectStore(RETRY_QUEUE_STORE_NAME).put({ url, value });
      });
    } catch (error) {
      console.error('[SW] Failed to persist retry queue entry:', error);
    }
  }

  async deleteEntry(url) {
    try {
      const db = await this.dbPromise;
      await new Promise((resolve, reject) => {
        const tx = db.transaction(RETRY_QUEUE_STORE_NAME, 'readwrite');
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
        tx.objectStore(RETRY_QUEUE_STORE_NAME).delete(url);
      });
    } catch (error) {
      console.error('[SW] Failed to delete retry queue entry:', error);
    }
  }
}
