function goToOptionScreen() {
    window.location.href = "/option_screen/";
}

function setupActivityButton() {
    activityButton = document.querySelector("#add-activity");
    if (!activityButton) return;

    const newActivityData = {
        'title': 'New Activity 1',
        'type': 'Tourism'
    }

    activityButton.addEventListener('click', function() {
        console.log("clicked");
        fetch('/add-new-activity/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify(newActivityData),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
}

function getCsrfToken() {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [name, value] = cookie.split('=');
        if (name.trim() === 'csrftoken') {
            return value;
        }
    }
    return '';
  }

function main() {
    setupActivityButton();
}

document.addEventListener('DOMContentLoaded', function() {
    main();
})