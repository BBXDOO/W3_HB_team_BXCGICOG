const CACHE_NAME = 'w3-v0.2';
const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.json',
  './offline.html',
  './icons/icon-192.png',
  './icons/icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
      .catch(err => {
        console.error('Service worker install failed:', err);
      })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      ))
      .then(() => self.clients.claim())
      .catch(err => {
        console.error('Service worker activation failed:', err);
      })
  );
});

self.addEventListener('fetch', event => {
  if (
    event.request.mode === 'navigate' ||
    (event.request.method === 'GET' &&
      event.request.headers.get('accept') &&
      event.request.headers.get('accept').includes('text/html'))
  ) {
    event.respondWith(
      fetch(event.request)
        .then(res => {
          const copy = res.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
          return res;
        })
        .catch(err => {
          console.error('Navigation fetch failed, serving offline page:', err);
          return caches.match('./offline.html');
        })
    );
    return;
  }
  event.respondWith(
    caches.match(event.request).then(resp =>
      resp ||
      fetch(event.request).catch(err => {
        console.error('Fetch failed and no cache entry for:', event.request.url, err);
        return caches.match('./offline.html');
      })
    )
  );
});
