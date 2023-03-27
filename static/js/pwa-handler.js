if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('service-worker.js')

}

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

const applicationServerKey = 'BC2fdyMeF44rKN5jlNybS4Z-9EhurCkUNTqbWs80OlTwwDuDuNYiXMbOv4t2-NK2ZXl57a-z17UqtcqCskskYbo';
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
      applicationServerKey: urlBase64ToUint8Array(applicationServerKey)
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
