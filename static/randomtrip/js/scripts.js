// scripts.js

document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('start-button');
    
    startButton.addEventListener('click', () => {
        // Create a blank screen effect
        document.body.innerHTML = ''; // Clear the current content
        document.body.style.backgroundColor = 'white'; // Set background color to white
    });
});