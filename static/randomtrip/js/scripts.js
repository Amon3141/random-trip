function showLoader() {
    document.getElementById('loader').style.display = 'flex';
  }
  
  function hideLoader() {
    document.getElementById('loader').style.display = 'none';
  }
  
function spinRoulette(radius) {
    const nextURL = document.querySelector("#spin-roulette").dataset.url;
    showLoader();
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
    
            fetch('/api/get-random-site/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ latitude: latitude, longitude: longitude, radius: radius})
            })
            .then(response => response.json())
            .then(data => {
                sessionStorage.setItem('randomSiteData', JSON.stringify(data));
                let showHomepage = true;
                if (data.homepage == '') showHomepage = false;

                const modifiedURL = new URL(nextURL, window.location.origin);
                modifiedURL.searchParams.set('show_homepage', showHomepage);

                window.location.href = modifiedURL.toString();
            })
            .catch(error => {
                hideLoader();
                console.error('Error:', error);
                alert("An error occurred. Please try again.");
            });
        }, error => {
            hideLoader();
            console.error('Geolocation error:', error);
            alert("Unable to get your location. Please ensure location services are enabled.");
        });
    } else {
        hideLoader();
        console.error('Geolocation is not supported by this browser.');
        alert("Geolocation is not supported by your browser. Please use a different browser.");
    }
}

function displayRandomSite() {
    const root = document.querySelector(':root');
    const siteData = JSON.parse(sessionStorage.getItem('randomSiteData'));
    if (siteData) {
        const site_name = document.querySelector(".next-destination-text");
        const site_address = document.querySelector(".next-destination-address");
        const site_description = document.querySelector(".next-destination-description");
        const go_to_homepage = document.querySelector(".go-to-homepage-button");
        const google_destination = document.querySelector(".google-destination-button");
        const go_to_homepage_link = document.querySelector("#go-to-homepage-link");
        const google_destination_link = document.querySelector("#google-destination-link");

        if (siteData.error) {
            console.error(siteData.error);
            site_name.style.display = "none";
            site_description.style.display = "none";
            site_address.innerText = "An error occurred";
            go_to_homepage.style.display = "non";
            google_destination.style.display = "non";
        } else {
            site_name.innerText = siteData.name;
            site_address.innerText = siteData.address;
            site_description.innerText = siteData.description;
            if (google_destination) google_destination.innerText = `Google "${siteData.name}"`;
            console.log(siteData.homepage)
            if (go_to_homepage_link) go_to_homepage_link.setAttribute('href', siteData.homepage);
            if (google_destination_link) google_destination_link.setAttribute('href', `https://www.google.com/search?q=${siteData.name}`);
        }
    }

    const spin_again_button = document.querySelector(".spin-again-button");
    spin_again_button.addEventListener('click', function(event) {
        event.preventDefault();
        sessionStorage.removeItem('randomSiteData');
        const nextURL = document.querySelector(".spin-again-button").dataset.url;
        window.location.href = nextURL;
    })

    const go_to_this_place_button = document.querySelector(".go-to-this-place-button");
    go_to_this_place_button.addEventListener('click', function(event) {
        event.preventDefault();
        sessionStorage.removeItem('randomSiteData');

        let destination = document.querySelector(".next-destination-text").innerText;
        destination = destination.replace(' ', '+');
        const nextURL = document.querySelector(".go-to-this-place-button").dataset.url;
        const modifiedURL = new URL(nextURL, window.location.origin);
        modifiedURL.searchParams.set('destination', destination);
        window.location.href = modifiedURL.toString();
    })
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

// Setup the roulette button
function setupRouletteButton() {
    const rouletteLink = document.querySelector("#spin-roulette-link");
    const distanceInput = document.querySelector("#distance-input");
    if (rouletteLink) {
        rouletteLink.addEventListener('click', function(event) {
            event.preventDefault();
            const radius = parseInt(distanceInput.value, 30);
            spinRoulette(radius);
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector("#spin-roulette")) {
        setupRouletteButton();
    }
});

window.addEventListener('load', function() {
    console.log("loaded")
    if (document.querySelector(".next-destination-text")) {
        displayRandomSite();
    }
});