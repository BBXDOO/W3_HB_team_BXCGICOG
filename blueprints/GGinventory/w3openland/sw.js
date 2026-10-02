
const CACHE_NAME = 'w3-v1-stable';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  'https://cdn.tailwindcss.com',
  'https://fonts.googleapis.com/css2?family=Anuphan:wght@300;400;500;600;700&display=swap'
];

// ขั้นตอนการติดตั้ง: เก็บไฟล์หลักลงแคชทันที
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return Promise.allSettled(ASSETS.map(url => cache.add(url)));
    })
  );
});

// ขั้นตอนการล้างแคชเก่า
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

// กลยุทธ์การดึงข้อมูล: Stale-While-Revalidate
// แสดงผลจากแคชทันทีเพื่อให้แอป "เปิดติด" เร็วที่สุด แล้วค่อยไปดึงข้อมูลใหม่มาอัปเดตในแคช
self.addEventListener('fetch', (event) => {
  // ข้ามคำขอที่ไม่ใช่ GET หรือเป็น Chrome Extensions
  if (event.request.method !== 'GET' || !event.request.url.startsWith('http')) return;

  event.respondWith(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.match(event.request).then((cachedResponse) => {
        const fetchPromise = fetch(event.request).then((networkResponse) => {
          if (networkResponse.ok) {
            cache.put(event.request, networkResponse.clone());
          }
          return networkResponse;
        }).catch(() => {
          // ถ้าเน็ตหลุดจริงๆ ให้คืนค่าจากแคช (ถ้ามี)
          return cachedResponse;
        });

        return cachedResponse || fetchPromise;
      });
    })
  );
});
