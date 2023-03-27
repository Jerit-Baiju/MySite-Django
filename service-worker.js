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

function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

const applicationServerKey = 'your-application-server-key';
const convertedKey = urlBase64ToUint8Array(applicationServerKey);


if ('Notification' in window && 'serviceWorker' in navigator) {
  // push notifications are supported
  console.log("push notifications are supported")
} else {
  // push notifications are not supported
  console.log("push notifications are not supported")
}


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
      applicationServerKey: urlBase64ToUint8Array("BC2fdyMeF44rKN5jlNybS4Z-9EhurCkUNTqbWs80OlTwwDuDuNYiXMbOv4t2-NK2ZXl57a-z17UqtcqCskskYbo")
    }).then(subscription => {
      console.log('User is subscribed with endpoint:', subscription.endpoint);
      console.log('User is subscribed with key:', subscription.getKey('p256dh'));
      console.log('User is subscribed with auth secret:', subscription.getKey('auth'));
      // Send the subscription to the server
      fetch('/subscribe/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCookie('csrftoken') // add this line if you're using CSRF protection
        },
        body: `registration_token=${subscription.endpoint}`
      }).then(response => {
        if (response.ok) {
          console.log('Subscription saved to server');
        } else {
          console.error('Failed to save subscription to server');
        }
      }).catch(error => {
        console.error('Failed to save subscription to server:', error);
      });
    }).catch(error => {
      console.error('Failed to subscribe user:', error);
    });
  });
}

