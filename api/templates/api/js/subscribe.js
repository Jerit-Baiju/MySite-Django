import {
    getMessaging,
    getToken
} from "https://www.gstatic.com/firebasejs/9.18.0/firebase-messaging.js";
import {
    initializeApp
} from "https://www.gstatic.com/firebasejs/9.18.0/firebase-app.js";

const firebaseConfig = {
    apiKey: "AIzaSyAF0ZxYZN1XEztSNPqpV77kAUGObLNc6SQ",
    authDomain: "jerit-in.firebaseapp.com",
    projectId: "jerit-in",
    storageBucket: "jerit-in.appspot.com",
    messagingSenderId: "791070201278",
    appId: "1:791070201278:web:b3a13ecadda6a3533a55ef"
};

const app = initializeApp(firebaseConfig);

$(document).ready(function () {
    $("#subscribe").click(function () {
        console.log('Requesting permission...');
        Notification.requestPermission().then((permission) => {
            if (permission === 'granted') {
                const messaging = getMessaging();
                getToken(messaging, { vapidKey: '{{ firebase_key }}' }).then((currentToken) => {
                    if (currentToken) {
                        $.ajax({
                            type: "POST",
                            url: "{% url 'subscribe' %}",
                            data: {
                                token: currentToken
                            },
                            success: function (response) {
                                alert(response['status'])
                            }
                        });
                    } else {
                        console.log('No registration token available. Request permission to generate one.');
                    }
                }).catch((err) => {
                    console.log('An error occurred while retrieving token. ', err);
                });
            }
        })
    })
})
