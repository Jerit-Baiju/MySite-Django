/* global importScripts, firebase */
importScripts('https://www.gstatic.com/firebasejs/8.0.0/firebase-app.js')
importScripts('https://www.gstatic.com/firebasejs/8.0.0/firebase-messaging.js')

firebase.initializeApp({
    apiKey: "AIzaSyDnllf521t5GPwIGE9xgp9xn709Qto4lq0",
    authDomain: "jerit-ml.firebaseapp.com",
    projectId: "jerit-ml",
    storageBucket: "jerit-ml.appspot.com",
    messagingSenderId: "31137066487",
    appId: "1:31137066487:web:31a7ead9dd2a081dcf92f2",
    measurementId: "G-W0EZ7CVXGR"
});

const messaging = firebase.messaging();
messaging.onBackgroundMessage((payload) => {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  // Customize notification here
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    image: payload.notification.image
  };

  self.registration.showNotification(notificationTitle,
    notificationOptions);
});