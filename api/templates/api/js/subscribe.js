$(document).ready(function () {
    $("#subscribe").click(function () {
        console.log('Requesting permission...');
        Notification.requestPermission().then((permission) => {
            if (permission === 'granted') {
                const messaging = getMessaging();
                getToken(messaging, { vapidKey: '{{ firebase_key }}' }).then((currentToken) => {
                    if (currentToken) {
                        console.log(currentToken)
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
