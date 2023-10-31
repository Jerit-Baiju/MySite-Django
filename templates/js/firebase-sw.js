importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-messaging.js');

firebase.initializeApp({
  apiKey: "AIzaSyAF0ZxYZN1XEztSNPqpV77kAUGObLNc6SQ",
  authDomain: "jerit-in.firebaseapp.com",
  projectId: "jerit-in",
  storageBucket: "jerit-in.appspot.com",
  messagingSenderId: "791070201278",
  appId: "1:791070201278:web:b3a13ecadda6a3533a55ef"
});

const messaging = firebase.messaging();
// messaging.onBackgroundMessage((payload) => {
//   console.log(
//     '[firebase-messaging-sw.js] Received background message ',
//     payload
//   );
//   // Customize notification here
//   const notificationTitle = 'Background Message Title';
//   const notificationOptions = {
//     body: 'Background Message body.',
//     icon: '/firebase-logo.png'
//   };

//   self.registration.showNotification(notificationTitle, notificationOptions);
// });