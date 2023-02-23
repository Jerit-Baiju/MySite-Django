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

self.addEventListener('push', function (event) {
  const data = event.data.json()
  event.waitUntil(
    self.ServiceWorkerRegistration.showNotification(data.head, {
      body: body.data,
      icon: data.icon,
      data: { url: data.url }
    })
  )
})

const initializeState = (reg) => {
  if (!reg.showNotification) {
    showNotAllowed('Showing notifications isn\'t supported ☹️😢');
    return
  }
  if (Notification.permission === 'denied') {
    showNotAllowed('You prevented us from showing notifications ☹️🤔');
    return
  }
  if (!'PushManager' in window) {
    showNotAllowed("Push isn't allowed in your browser 🤔");
    return
  }
  subscribe(reg);
}

const showNotAllowed = (message) => {
  const button = document.querySelector('form>button');
  button.innerHTML = `${message}`;
  button.setAttribute('disabled', 'true');
};


function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  const outputData = outputArray.map((output, index) => rawData.charCodeAt(index));

  return outputData;
}

const subscribe = async (reg) => {
  const subscription = await reg.pushManager.getSubscription();
  if (subscription) {
    sendSubData(subscription);
    return;
  }

  const vapidMeta = document.querySelector('meta[name="vapid-key"]');
  const key = vapidMeta.content;
  const options = {
    userVisibleOnly: true,
    // if key exists, create applicationServerKey property
    ...(key && { applicationServerKey: urlB64ToUint8Array(key) })
  };

  const sub = await reg.pushManager.subscribe(options);
  sendSubData(sub)
};