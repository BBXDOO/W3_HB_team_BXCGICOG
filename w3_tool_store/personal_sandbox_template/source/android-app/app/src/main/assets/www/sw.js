const CACHE = 'w3-personal-shell-v32';
const SHELL = ['./', './manifest.json', './icon.svg'];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(async cache => {
    await cache.addAll(SHELL);
    const page = await fetch('./');
    const html = await page.text();
    const urls = [...html.matchAll(/(?:src|href)="(\.\/assets\/[^\"]+|\/assets\/[^\"]+)"/g)]
      .map(match => new URL(match[1], self.registration.scope).href);
    await cache.addAll(urls);
    await self.skipWaiting();
  }));
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key.startsWith('w3-personal-shell-') && key !== CACHE).map(key => caches.delete(key)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin) return;
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    if (request.mode === 'navigate') {
      try { return await fetch(request); }
      catch { return await cache.match('./') || Response.error(); }
    }
    return await cache.match(request) || await fetch(request).then(response => {
      if (response.ok) cache.put(request, response.clone());
      return response;
    });
  })());
});
