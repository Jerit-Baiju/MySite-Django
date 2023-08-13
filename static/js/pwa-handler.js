if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('service-worker.js')
  navigator.serviceWorker.register('firebase-messaging-sw.js')
}
