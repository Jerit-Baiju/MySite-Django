import { initializeApp } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-analytics.js";
import { getMessaging, getToken, onMessage } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-messaging.js";

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

$(document).ready(function () {
    $("#subscribe").click(function () {
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
                        alert(currentToken)
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
        
    })
})

onMessage(messaging, (payload) => {
    console.log('Message received. ', payload);
    // ...
});