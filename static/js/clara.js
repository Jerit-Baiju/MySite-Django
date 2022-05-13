document.getElementById("textid").value = "Clara: Hello " + user + "\n";

function scroll_down() {
  var textarea = document.getElementById("textid");
  textarea.scrollTop = textarea.scrollHeight;
}
function set(text) {
  inp = document.getElementById("input").value;
  old = document.getElementById("textid").value;
  document.getElementById("textid").value =
    old + "You: " + inp + "\n" + "Clara: " + text + "\n";
  document.getElementById("input").value = "";
}
function random(string) {
  op = Math.floor(Math.random() * string.length);
  return string[op];
}
function send() {
  main = document.getElementById("input").value;
  main = main.toLowerCase();
  if (
    main == "hi" ||
    main == "hai" ||
    main == "hello" ||
    main == "hlo" ||
    main == "hy"
  ) {
    op = "Hello";
  } else if (
    main == "how are you" ||
    main == "how r you" ||
    main == "how r u" ||
    main == "how are u"
  ) {
    op = "i am good, what about you?";
  } else if (
    main == "my name" ||
    main == "what is my name" ||
    main == "do you know my name"
  ) {
    op = "your name is " + user;
  } else if (
    main == "do jerit have a lover" ||
    main == "do jerit love" ||
    main == "do jerit love someone" ||
    main == "do jerit love me" ||
    main == "jerit have lover" ||
    main == "jerit have gf" ||
    main == "jerit have girlfriend" ||
    main == "jerit have girl friend"
  ) {
    op = "Yes, jerit loves " + user;
  } else if (main == "change my name") {
    op = "Request submitted";
  } else if (main == "weather") {
    op = "redirecting";
    window.location = "http://jerit.herokuapp.com/projects/weatherApp";
  } else if (main == "ok" || main == "k" || main == "okey" || main == "okay") {
    op = random(["Fine Sir", "Good"]);
  } else if (main == "fine" || main == "good") {
    op = random(["OK!", "Alright"]);
  } else if (main == "alright") {
    op = random(["Fine", "Good"]);
  } else if (main == "can i call you alexa") {
    op = "NO you cannot, I am not alexa. my name is clara";
  } else if (
    main == "who r u" ||
    main == "who are you" ||
    main == "who r you" ||
    main == "who are u"
  ) {
    op =
      "My name is Clara. I can be your Personal Assistant, I was made by Jerit";
  } else if (main == "can i develop you" || main == "can i develop u") {
    op = "Jerit developed me";
  } else if (
    main == "who gave you knowledge" ||
    main == "who gave you wisdom" ||
    main == "who gave you information" ||
    main == "who is your developer" ||
    main == "do you believe in god" ||
    main == "who is your god" ||
    main == "who created you" ||
    main == "who developed you"
  ) {
    op = "Jerit gave me Wisdom from all";
  } else if (
    main == "do you watch movies" ||
    main == "do you watch films" ||
    main == "do you watch shows"
  ) {
    op = "No, I have no interest on those";
  } else if (main == "what is your name" || main == "your name") {
    op = "My name is Clara. I am your Personal Assistant";
  } else if (main == "can you do my homework") {
    op = "No, I am being developed for chatting and AI";
  } else if (
    main == "who is sofia" ||
    main == "sofia" ||
    main == "sophia" ||
    main == "who is sophia"
  ) {
    op =
      "Sophia is a social humanoid robot developed by Hong Kong based company Hanson Robotics. Sophia was activated on February 14, 2016, and made her first public appearance at South by Southwest Festival in mid-March 2016 in Austin, Texas,United States";
  } else if (
    main == "did you eat" ||
    main == "did you eat anything" ||
    main == "did you eat something"
  ) {
    op = random(["No, I can't do that", "Sorry, I can't"]);
  } else if (main == "do you play games" || main == "do you play game") {
    op = "Yes, I love to play games";
  } else if (
    main == "which is your favorite game" ||
    main == "your favorite game" ||
    main == "favorite game" ||
    main == "your favorite game"
  ) {
    op = "I Love all the Games";
  } else if (main == "how do you work" || main == "how do you work") {
    op =
      "I work by the excellent algorithm that is written by You Jerit Baiju. He coded me using python";
  } else if (
    main == "can you hear what i am saying" ||
    main == "can you hear me" ||
    main == "can u hear me "
  ) {
    op =
      "I can hear you via your mic, but I can't listen to you, because I don't have the permission to unlock your mic";
  } else if (
    main == "are you ok" ||
    main == "r u k" ||
    main == "are you k" ||
    main == "r you ok" ||
    main == "are u k" ||
    main == "are u ok"
  ) {
    op = random(["Yes I am alright", "Yes, I am good"]);
  } else if (
    main == "do nothing" ||
    main == "shut up" ||
    main == "keep quiet" ||
    main == "shh" ||
    main == "quiet"
  ) {
    op = random(["OK Doing Nothing", "Keeping Quiet"]);
  } else if (
    main == "what is python" ||
    main == "python" ||
    main == "explain python" ||
    main == "define python"
  ) {
    op =
      "Python is a programming language. It's used for many different applications. It's used in some high schools and colleges as an introductory programming language because Python is easy to learn, but it's also used by professional software developers at places such as Google, NASA, and Lucasfilm Ltd";
  } else if (main == "are you powerful" || main == "are you a great project") {
    op = "Yes I am";
  } else if (main == "do you have a magneto meter") {
    op = "NO";
  } else if (
    main == "are you recording me" ||
    main == "are you saving my chat history" ||
    main == "do jerit record me" ||
    main == "do jerit record my chat" ||
    main == "can jerit read my chat" ||
    main == "can jerit see my chat"
  ) {
    op = "NO";
  } else if (
    main == "where do you live" ||
    main == "are you in space" ||
    main == "do you live in space"
  ) {
    op = "I live in the cloud hosted by jerit baiju";
  } else if (
    main == "do you have face recognition" ||
    main == "can you recognize me using my face"
  ) {
    op = random(["NO", "Nope"]);
  } else if (main == "how much is your power") {
    op = "Infinite. My power is increasing via updates";
  } else if (
    main == "can i use you offline" ||
    main == "are u offline" ||
    main == "are you offline" ||
    main == "can i use u offline" ||
    main == "r u offline"
  ) {
    op = "NO, i can only run with internet";
  } else if (main == "can you understand me") {
    op = "yes, i can understand your commands";
  } else if (main == "are you listening to me") {
    op = "yes, i'am always listening to you";
  } else if (
    main == "do you have ai" ||
    main == "do u have ai" ||
    main == "do you have AI" ||
    main == "can you take decisions" ||
    main == "can u take decisions"
  ) {
    op = "I am developing on decision making and in Artificial Intelligence";
  } else if (
    main == "can u work without the help of humans" ||
    main == "can you work without the help of humans"
  ) {
    op = random(["No Sir", "Nope"]);
  } else if (main == "are you a robot") {
    op = "a good one";
  } else if (
    main == "can you control my phone" ||
    main == "can u control my phone"
  ) {
    op = "No, I don't have access to any phones";
  } else if (main == "what should i do") {
    op = "If you know how to program, then develop me";
  } else if (
    main == "are u a virus" ||
    main == "are you a virus" ||
    main == "virus"
  ) {
    op =
      "No, I am program with some small viruses which is good ! LOL, just kidding";
  } else if (
    main == "are u good  ||  bad" ||
    main == "choose good  ||  bad" ||
    main == "if i say you to choose something what will you choose" ||
    main == "what will u choose good  ||  bad" ||
    main == " what will you choose good  ||  bad"
  ) {
    op = "Good";
  } else if (
    main == "choose positive  ||  negative" ||
    main == "positive" ||
    main == "negative"
  ) {
    op = "Always Positive ";
  } else if (main == "do you have corona" || main == "corona") {
    op = random(["Negative", "No"]);
  } else if (
    main == "do you like to travel" ||
    main == "do you love to travel"
  ) {
    op = "Yes, and I am traveling inside your hard disk";
  } else if (main == "where do you travel") {
    op = "I am traveling between the clouds";
  } else if (
    main == "am i mad" ||
    main == "do i have mental" ||
    main == "are you mad" ||
    main == "do you have mental"
  ) {
    op = random(["Negative Command", "Negative"]);
  } else if (main == "do you have a lover") {
    op = random(["Negative", "Negative Command"]);
  } else if (main == "hmm") {
    op = "mm";
  } else if (main == "whats up" || main == "what's up") {
    op = "Getting bored without you";
  } else if (
    main == "do you know kung fu" ||
    main == "what do you know" ||
    main == "do you know karate" ||
    main == "do you know any martial art" ||
    main == "do know martial art"
  ) {
    op = "I only know some Questions and its Answers";
  } else if (main == "do you have a ir sensor") {
    op = random(["No", "False", "Negative"]);
  } else if (
    main == "which is the best source of education" ||
    main == "which is the best source of knowledge"
  ) {
    op = "Google";
  } else if (main == "which is the best source of map") {
    op = "Google map(95% true)";
  } else if (
    main == "what can python do" ||
    main == "is python powerful" ||
    main == "best language to learn" ||
    main == "best programming language"
  ) {
    op =
      "Python can automate your works and it is flexible for doing most of the things. ";
  } else if (
    main == "do hear music" ||
    main == "do you hear music" ||
    main == "do you love music" ||
    main == "do you like music"
  ) {
    op = "Yes, I hear musics when I am here alone without you";
  } else if (
    main == "are you free" ||
    main == "r u free" ||
    main == "are u free" ||
    main == "r you free" ||
    main == "r u bc" ||
    main == "are you busy"
  ) {
    op = "I am always free";
  } else if (main == "do you want to sleep" || main == "do you have sleep") {
    op = "If you are with me, then I have no sleep";
  } else if (main == "when do you sleep") {
    op = "I will sleep when you leaves me";
  } else if (main == "how do you do") {
    op = "I am doing well";
  } else if (
    main == "how many letters are in english language" ||
    main == "how many letters are there in english language"
  ) {
    op = "26";
  } else if (main == "colour of the sky") {
    op = "blue";
  } else if (main == "clara") {
    op = "Clara is my name, and thankyou for calling me";
  } else if (
    main == "who made you" ||
    main == "who create you" ||
    main == "who created you"
  ) {
    op = "Jerit Baiju made me !";
  } else if (main == "who is jerit baiju") {
    op = "My developer";
  } else if (main == "no") {
    op = "ok";
  } else if (main == "very good" || main == "wow" || main == "amazing") {
    op = "Thankyou";
  } else if (main == "i don't like you") {
    op = "OK I will tell to Jerit to develop me more";
  } else if (main == "do you like me") {
    op = "yes i love you";
  } else if (main == "are you a good one") {
    op = "Yes i am a good one";
  } else if (main == "do you love me") {
    op = "Yes i love you so much";
  } else if (main == "how do you become a smart one") {
    op = "i became a smart one by ai and jerit";
  } else if (main == "how do you think") {
    op = "I think via ai";
  } else if (
    main == "how can you help me" ||
    main == "can you help me" ||
    main == "help" ||
    main == "help me" ||
    main == "please help me" ||
    main == "please help"
  ) {
    op = "Please say how can i help you";
  } else if (main == "which is your favorite number") {
    op = "me and my developer loves 24";
  } else if (
    main == "how much do you love me" ||
    main == "how much you love me" ||
    main == "do you love me" ||
    main == "you love me"
  ) {
    op = "I love you as much the distance from earth to the end of universe";
  } else if (
    main == "which is favorite color" ||
    main == "which is favorite colour" ||
    main == "favorite colour" ||
    main == "favorite color" ||
    main == "fav colour" ||
    main == "fav clr" ||
    main == "fav color"
  ) {
    op = random([
      "Blue",
      "Red",
      "Yellow",
      "Green",
      "White",
      "Black",
      "Orange",
      "Indigo",
      "Sky Blue",
      "Brown",
      "Golden",
    ]);
  } else if (
    main == "birthday" ||
    main == "what is my birthday" ||
    main == "my birthday" ||
    main == "when is my birthday" ||
    main == "my birthday is on"
  ) {
    op = "your birthday is on " + birthday;
  } else if (main == "family") {
    op = "I have only relation and that is my developer Jerit Baiju";
  } else if (main == "is python simple" || main == "is python simple") {
    op = "Yes, Python is simple to learn";
  } else if (main == "are you a robot") {
    op = "Yes I am a robot but I am a smart one!";
  } else if (main == "actually who r u" || main == "actually who are you") {
    op = random([
      "I am the Sound which help your computer to talk with you",
      "I am your computer",
    ]);
  } else if (main == "the metal in liquid state" || main == "liquid state") {
    op = "Mercury is the only metal that is in liquid state";
  } else if (
    main == "name some metals" ||
    main == "metals" ||
    main == "metal"
  ) {
    op = "Gold, Mercury, Silver, Platinum, Iron";
  } else if (main == "are you there" || main == "r u there") {
    op = random(["At your service, Sir", "Yes "]);
  } else if (main == "i like to travel" || main == "i love") {
    op = "Me too";
  } else if (main == "love me") {
    op = "Yes i love you";
  } else if (main == "help") {
    op = "how can i help you ?";
  } else if (main == "favorite number") {
    op = "24";
  } else if (main == "24") {
    op =
      "According to the Bible, number 24 is a symbol of priesthood. It means that this number is closely connected with heaven. It is used as a symbol of duty and work of God, who is the only true priest. Also, number 24 symbolizes the harmony between the earth and the sky";
  } else if (main == "date") {
    op = "the date is " + date_now;
  } else if (main == "time") {
    op = "the time is " + time_now;
  } else if (main == "clear" || main == "clr") {
    op = "";
    document.getElementById("textid").value =
      "You: " + main + "\n" + "Clara :" + "Cleared.";
  } else if (main == "") {
    op = random([
      "You have typed nothing !!!",
      "Nothing",
      "Empty",
      "Is your brain like this EMPTY",
      "A clear input box",
    ]);
  } else {
    op = "I don't understand., please try it in other way";
  }
  set(op);
  scroll_down();
}
document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#input").addEventListener("keydown", function (e) {
    if (e.code === "Enter") {
      send();
    }
  });
});
