importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js')

const CACHE = "jerit-baiju";
const assets = [
  "/stats",
  // icons
  "/static/favicon.png",
  "/static/images/icons/404.png",
  "/static/images/icons/offline.png",
  // fonts
  "/static/fonts/comforter.ttf",
  "/static/fonts/source_code.ttf",
  // footer
  "/static/images/footer/call.png",
  "/static/images/footer/email.png",
  "/static/images/footer/github.png",
  "/static/images/footer/whatsapp.png",
  "/static/images/footer/instagram.png",
  // cdns
  "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css",
  "https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.7/dist/umd/popper.min.js",
  "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.min.js"
];

const offlinePage = '/offline.html';

self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then(function (cache) {
        cache.addAll(assets)
      })
  );
});

if (workbox.navigationPreload.isSupported()) {
  workbox.navigationPreload.enable();
}

self.addEventListener('fetch', (event) => {
  if (event.request.mode === 'navigate') {
    event.respondWith((async () => {
      try {
        const preloadResp = await event.preloadResponse;

        if (preloadResp) {
          return preloadResp;
        }

        const networkResp = await fetch(event.request);
        return networkResp;
      } catch (error) {
        const cache = await caches.open(CACHE);
        const cachedResp = await cache.match(offlinePage);
        return cachedResp;
      }
    })());
  }
});