// Service Worker for W3 PWA
// NOTE: Update CACHE_VERSION whenever you change cached assets (ASSETS_TO_CACHE)
// or make changes that should force clients to refresh their cached content.
const CACHE_VERSION = 'v1';
const CACHE_NAME = `w3-pwa-${CACHE_VERSION}`;
const OFFLINE_URL = 'offline.html';

// Failed cache tracking with retry
const failedCacheQueue = new Map(); // url -> { attempts, lastAttempt, request }
const MAX_RETRY_ATTEMPTS = 3;
const RETRY_BASE_DELAY_MS = 2000; // 2 seconds base
let retryTimerId = null;

// Assets to cache on install
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './offline.html',
  './icons/icon-192.png',
  './icons/icon-512.png'
];

// Install event - cache assets
self.addEventListener('install', (event) => {
  console.log('[SW] Installing service worker...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Caching app shell');
        return cache.addAll(ASSETS_TO_CACHE);
      })
      .then(() => {
        console.log('[SW] Service worker installed successfully');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[SW] Cache failed:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((cacheName) => {
            return cacheName !== CACHE_NAME;
          })
          .map((cacheName) => {
            console.log('[SW] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          })
      );
    }).then(() => {
      console.log('[SW] Service worker activated');
      return self.clients.claim();
    })
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') return;

  // Skip chrome extensions and other protocols
  if (!event.request.url.startsWith('http')) return;

  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        // Cache first strategy for app assets
        if (cachedResponse) {
          console.log('[SW] Serving from cache:', event.request.url);
          return cachedResponse;
        }

        // Network first strategy for everything else
        return fetch(event.request)
          .then((response) => {
            // Don't cache non-successful or opaque responses
            if (!response || !response.ok || response.type === 'opaque') {
              return response;
            }

            // Clone the response
            const responseToCache = response.clone();
            const requestClone = event.request.clone();

            // Cache successful responses with retry on failure
            caches.open(CACHE_NAME)
              .then((cache) => {
                return cache.put(requestClone, responseToCache);
              })
              .then(() => {
                console.log('[SW] Cached successfully:', event.request.url);
              })
              .catch((error) => {
                console.error('[SW] Cache put failed:', error.message || error);
                // Add to retry queue (will be processed later)
                if (!failedCacheQueue.has(event.request.url)) {
                  failedCacheQueue.set(event.request.url, {
                    attempts: 0,
                    lastAttempt: Date.now(),
                    request: requestClone
                  });
                  console.log('[SW] Added to retry queue:', event.request.url);
                  // Schedule retry processing
                  scheduleRetryProcessing();
                }
              });

            return response;
          })
          .catch((error) => {
            console.error('[SW] Fetch failed:', error);
            
            // Return offline page for navigation requests
            if (event.request.mode === 'navigate') {
              return caches.match(OFFLINE_URL).then((cachedOffline) => {
                if (cachedOffline) {
                  return cachedOffline;
                }
                // Fallback if offline page is not in cache
                return new Response('คุณกำลังออฟไลน์และไม่สามารถโหลดหน้านี้ได้ในขณะนี้', {
                  status: 503,
                  headers: { 'Content-Type': 'text/plain; charset=utf-8' }
                });
              });
            }

            // For other requests, just fail
            return new Response('Network error', {
              status: 408,
              headers: { 'Content-Type': 'text/plain' }
            });
          });
      })
  );
});

// Listen for messages from the client
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// Schedule retry processing (avoids continuous setInterval)
function scheduleRetryProcessing() {
  if (retryTimerId) return; // Already scheduled
  
  if (failedCacheQueue.size === 0) {
    retryTimerId = null;
    return;
  }

  // Calculate minimum delay needed based on queue items
  let minDelay = RETRY_BASE_DELAY_MS;
  const now = Date.now();
  
  failedCacheQueue.forEach((item) => {
    const timeSinceLastAttempt = now - item.lastAttempt;
    const requiredDelay = RETRY_BASE_DELAY_MS * Math.pow(2, item.attempts);
    const remainingDelay = Math.max(0, requiredDelay - timeSinceLastAttempt);
    minDelay = Math.min(minDelay, remainingDelay || RETRY_BASE_DELAY_MS);
  });

  retryTimerId = setTimeout(() => {
    processFailedCacheQueue();
    retryTimerId = null;
    // Reschedule if there are still items
    if (failedCacheQueue.size > 0) {
      scheduleRetryProcessing();
    }
  }, minDelay);
}

// Process failed cache queue with exponential backoff
function processFailedCacheQueue() {
  if (failedCacheQueue.size === 0) return;

  console.log('[SW] Processing retry queue:', failedCacheQueue.size, 'items');
  const now = Date.now();
// Process failed cache queue with exponential backoff
async function processFailedCacheQueue() {
  if (failedCacheQueue.size === 0) return;

  console.log('[SW] Processing retry queue:', failedCacheQueue.size, 'items');
  const now = Date.now();
  
  // Convert to array to avoid iterator issues during async operations
  const entries = Array.from(failedCacheQueue.entries());
  
  // Process each item sequentially or use Promise.all for parallel processing
  for (const [url, item] of entries) {
    const timeSinceLastAttempt = now - item.lastAttempt;
    const requiredDelay = RETRY_BASE_DELAY_MS * Math.pow(2, item.attempts);
    
    if (timeSinceLastAttempt < requiredDelay) {
      continue;
    }
    
    if (item.attempts >= MAX_RETRY_ATTEMPTS) {
      console.warn('[SW] Max retry attempts reached, removing:', url);
      failedCacheQueue.delete(url);
      continue;
    }
    
    console.log('[SW] Retrying cache (attempt ' + (item.attempts + 1) + '):', url);
    
    try {
      const response = await fetch(item.request.clone());
      if (response && response.ok) {
        const cache = await caches.open(CACHE_NAME);
        await cache.put(item.request.clone(), response);
        console.log('[SW] Retry cache successful:', url);
        failedCacheQueue.delete(url);
      } else {
        throw new Error('Response not OK: ' + response.status);
      }
    } catch (error) {
      console.error('[SW] Retry failed:', url, error.message);
      item.attempts += 1;
      item.lastAttempt = Date.now();
      
      if (item.attempts >= MAX_RETRY_ATTEMPTS) {
        console.warn('[SW] Max attempts reached, removing:', url);
        failedCacheQueue.delete(url);
      }
    }
  }
}
}

