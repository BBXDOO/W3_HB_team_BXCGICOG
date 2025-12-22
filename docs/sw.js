const CACHE_NAME='w3hb-pwa-v1';
const PRECACHE_URLS=[
  '/W3_HB_team_BXCGICOG/',
  '/W3_HB_team_BXCGICOG/index.html',
  '/W3_HB_team_BXCGICOG/offline.html',
  '/W3_HB_team_BXCGICOG/manifest.json',
  '/W3_HB_team_BXCGICOG/icons/icon-192.png',
  '/W3_HB_team_BXCGICOG/icons/icon-512.png'
];
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE_NAME).then(cache=>cache.addAll(PRECACHE_URLS)).then(self.skipWaiting()));});
self.addEventListener('activate',event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.map(key=>{if(key!==CACHE_NAME) return caches.delete(key)}))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',event=>{if(event.request.mode==='navigate' || (event.request.method==='GET' && event.request.headers.get('accept')?.includes('text/html'))){event.respondWith(fetch(event.request).then(res=>{const copy=res.clone();caches.open(CACHE_NAME).then(cache=>cache.put(event.request,copy));return res}).catch(()=>caches.match('/W3_HB_team_BXCGICOG/offline.html')));return;}event.respondWith(caches.match(event.request).then(resp=>resp||fetch(event.request).catch(()=>{})));});
