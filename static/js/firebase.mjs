// Import the functions you need from the SDKs you need
import { initializeApp } from "./node_modules/firebase/app";
import { getAnalytics } from "./node_modules/firebase/analytics";
import { getMessaging, getToken, onMessage } from "./node_modules/firebase/messaging"
import { onBackgroundMessage } from "./node_modules/firebase/messaging/sw"

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyDnllf521t5GPwIGE9xgp9xn709Qto4lq0",
    authDomain: "jerit-ml.firebaseapp.com",
    projectId: "jerit-ml",
    storageBucket: "jerit-ml.appspot.com",
    messagingSenderId: "31137066487",
    appId: "1:31137066487:web:31a7ead9dd2a081dcf92f2",
    measurementId: "G-W0EZ7CVXGR"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const messaging = getMessaging(app)

console.log('Requesting permission...');
Notification.requestPermission().then((permission) => {
    if (permission === 'granted') {
        console.log('Notification permission granted.');
        // Get registration token. Initially this makes a network call, once retrieved
        // subsequent calls to getToken will return from cache.
        const messaging = getMessaging();
        getToken(messaging, { vapidKey: 'BC2fdyMeF44rKN5jlNybS4Z-9EhurCkUNTqbWs80OlTwwDuDuNYiXMbOv4t2-NK2ZXl57a-z17UqtcqCskskYbo' }).then((currentToken) => {
            if (currentToken) {
                console.log(currentToken)
                // Send the token to your server and update the UI if necessary
                // ...
            } else {
                // Show permission request UI
                console.log('No registration token available. Request permission to generate one.');
                // ...
            }
        }).catch((err) => {
            console.log('An error occurred while retrieving token. ', err);
            // ...
        });
    }
})

onMessage(messaging, (payload) => {
    console.log('Message received. ', payload);
    // ...
});


onBackgroundMessage(messaging, (payload) => {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);
    // Customize notification here
    const notificationTitle = 'Background Message Title';
    const notificationOptions = {
        body: 'Background Message body.',
        icon: '/firebase-logo.png'
    };

    self.registration.showNotification(notificationTitle,
        notificationOptions);
});
