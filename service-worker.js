importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

const CACHE = "jerit-baiju";

const assets = [
  // pages
  "/",
  "/stats",
  "/offline.html",
  // icons
  "/static/images/icons/404.png",
  "/static/images/icons/offline.png",
  // footer
  "/static/images/footer/call.png",
  "/static/images/footer/email.png",
  "/static/images/footer/github.png",
  "/static/images/footer/whatsapp.png",
  "/static/images/footer/instagram.png",
  // cdns
  "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
  "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js",
]

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
        const cachedResp = await cache.match(assets);
        return cachedResp;
      }
    })());
  }
});

if (Notification.permission !== 'granted') {
  Notification.requestPermission().then(permission => {
    if (permission === 'granted') {
      console.log('Notification permission granted');
      // TODO: subscribe the user to push notifications
    }
  });
}


if (Notification.permission === 'granted') {
  navigator.serviceWorker.ready.then(registration => {
    registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(applicationServerKey)
    }).then(subscription => {
      console.log('User is subscribed with endpoint:', subscription.endpoint);
      console.log('User is subscribed with key:', subscription.getKey('p256dh'));
      console.log('User is subscribed with auth secret:', subscription.getKey('auth'));
      // Send the registration token to the server
      fetch('/api/subscribe/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          registration_token: subscription.endpoint
        })
      });
    }).catch(error => {
      console.error('Failed to subscribe user:', error);
    });
  });
}
