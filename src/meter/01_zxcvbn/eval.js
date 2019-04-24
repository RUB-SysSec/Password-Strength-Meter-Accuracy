function checkStrength(password) {
    'use strict';
    var user_inputs = []; // could be the username, email address, service name
    var result = zxcvbn(password, user_inputs);
    document.getElementById("guess_number").innerHTML = result.guesses;
    document.getElementById("score").innerHTML = result.score;
}

$(document).ready(function () {
    'use strict';
    // your function
    var my_func = function (event) {
        event.preventDefault(); // stop default submit action of HTML forms
        // reset the form to be fresh
        document.getElementById("guess_number").innerHTML = "";
        document.getElementById("score").innerHTML = "";
        // get password and check strength / blacklist
        var password = document.getElementById("password").value;
        checkStrength(password);
    };
    // your form
    var form = document.getElementById("myForm");
    // attach event listener
    form.addEventListener("submit", my_func, true);
});
