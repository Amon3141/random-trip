// scripts.js

function goToOptionScreen() {
    window.location.href = "/option_screen/";
}

function beginFinding() {
    var number = document.getElementById('numberInput').value;
    if (number === "") {
        alert("Please enter a number.");
        return;
    }

    // Redirect or process the number as needed
    alert("You entered: " + number);
    // Example: window.location.href = "/some_other_page/?number=" + number;
}