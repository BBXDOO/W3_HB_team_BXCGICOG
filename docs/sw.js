// Service Worker for W3 PWA
// NOTE: Update CACHE_VERSION whenever you change cached assets (ASSETS_TO_CACHE)
// or make changes that should force clients to refresh their cached content.
const CACHE_VERSION = 'v1';
const CACHE_NAME = `w3-pwa-${CACHE_VERSION}`;
const OFFLINE_URL = 'offline.html';

// Failed cache tracking for retry
const failedCacheQueue = [];
const MAX_RETRY_ATTEMPTS = 3;
const RETRY_DELAY_MS = 5000; // 5 seconds

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

            // Cache successful responses with retry on failure
            caches.open(CACHE_NAME)
              .then((cache) => {
                return cache.put(event.request, responseToCache);
              })
              .then(() => {
                console.log('[SW] Cached successfully:', event.request.url);
              })
              .catch((error) => {
                console.error('[SW] Cache put failed:', error);
                // Add to failed queue for retry
                const failedItem = {
                  url: event.request.url,
                  attempts: 0,
                  timestamp: Date.now()
                };
                failedCacheQueue.push(failedItem);
                console.log('[SW] Added to retry queue:', event.request.url);
                
                // Attempt immediate retry
                retryCacheOperation(event.request, responseToCache, 0);
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

// Retry mechanism for failed cache operations
function retryCacheOperation(request, response, attempts = 0) {
  if (attempts >= MAX_RETRY_ATTEMPTS) {
    console.warn('[SW] Max retry attempts reached for:', request.url);
    return;
  }

  setTimeout(() => {
    caches.open(CACHE_NAME)
      .then((cache) => {
        return cache.put(request, response.clone());
      })
      .then(() => {
        console.log('[SW] Retry cache successful for:', request.url);
        // Remove from failed queue if exists
        const index = failedCacheQueue.findIndex(item => item.url === request.url);
        if (index > -1) {
          failedCacheQueue.splice(index, 1);
        }
      })
      .catch((error) => {
        console.error('[SW] Retry cache failed (attempt ' + (attempts + 1) + '):', error);
        // Retry again with incremented attempts
        retryCacheOperation(request, response, attempts + 1);
      });
  }, RETRY_DELAY_MS * (attempts + 1)); // Exponential backoff
}

// Process failed cache queue periodically
function processFailedCacheQueue() {
  if (failedCacheQueue.length === 0) return;

  console.log('[SW] Processing failed cache queue:', failedCacheQueue.length, 'items');
  
  const queueCopy = [...failedCacheQueue];
  failedCacheQueue.length = 0; // Clear queue
  
  queueCopy.forEach(item => {
    if (item.attempts < MAX_RETRY_ATTEMPTS) {
      fetch(item.url)
        .then(response => {
          if (response && response.ok) {
            return caches.open(CACHE_NAME)
              .then(cache => cache.put(item.url, response))
              .then(() => {
                console.log('[SW] Queue retry successful for:', item.url);
              });
          }
        })
        .catch(error => {
          console.error('[SW] Queue retry failed for:', item.url, error);
          // Re-add to queue with incremented attempts
          if (item.attempts + 1 < MAX_RETRY_ATTEMPTS) {
            failedCacheQueue.push({
              url: item.url,
              attempts: item.attempts + 1,
              timestamp: Date.now()
            });
          }
        });
    }
  });
}

// Run queue processor every 30 seconds
setInterval(processFailedCacheQueue, 30000);

