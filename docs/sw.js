const CACHE_NAME = 'w3-cache-v1';
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/manifest.json'
];

self.addEventListener('install', event => {
  console.log('[SW] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_URLS))
      .catch(err => console.error('[SW] Pre-cache failed:', err))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  console.log('[SW] Activating...');
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      ))
      .then(() => self.clients.claim())
      .catch(err => console.error('[SW] Activate failed:', err))
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;

      return fetch(event.request)
        .then(response => {
          const copy = response.clone();
          caches.open(CACHE_NAME)
            .then(cache => cache.put(event.request, copy))
            .catch(err => console.error('[SW] Cache put failed:', err));
          return response;
        })
        .catch(err => {
          console.error('[SW] Fetch failed:', event.request.url, err);
          return new Response(
            '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Offline</title></head>' +
            '<body><h1>You are offline</h1><p>Please check your connection and try again.</p></body></html>',
            { status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8' } }
          );
        });
    })
  );
});
