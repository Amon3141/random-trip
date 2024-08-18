var current_site_name = null;
var current_site_googlemaps = null;

function showLoader() {
    document.querySelector('.loading-overlay').style.display = 'flex';
  }
  
  function hideLoader() {
    document.querySelector('.loading-overlay').style.display = 'none';
  }
  
  function spinRoulette(radius) {
    const site_name = document.querySelector(".next-destination-text");
    const site_address = document.querySelector(".next-destination-address");
    const site_description = document.querySelector(".next-destination-description");
    const google_destination = document.querySelector(".google-destination-button");
    const go_to_homepage = document.querySelector(".go-to-homepage-button");

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
          hideLoader();
          if (data.error) {
            console.error(data.error);
            site_name.style.display = "none";
            site_description.style.display = "none";
            go_to_homepage.style.display = "none";
            google_destination.style.display = "none";
            site_address.innerText = "An error occured";
          } else {
            current_site_name = data.get("name");
            site_name.innerText = data.get("name");
            site_address.innerText = data.get("address");
            site_description.innerText = data.get("description");
            if (data.get("homepage")) {
                go_to_homepage.style.display = "block"
                google_destination.style.display = "none"
            } else {
                go_to_homepage.style.display = "none";
                google_destination.style.display = "block";
            }
            current_site_googlemaps = data.get("google_maps_url");
          }
        })
        .catch(error => {
          hideLoader();
          console.error('Error:', error);
          site_name.style.display = "none";
          site_description.style.display = "none";
          go_to_homepage.style.display = "none";
          google_destination.style.display = "none";
          site_address.innerText = "An error occured";
        });
      }, error => {
        hideLoader();
        console.error('Geolocation error:', error);
        site_name.style.display = "none";
        site_description.style.display = "none";
        go_to_homepage.style.display = "none";
        google_destination.style.display = "none";
        site_address.innerText = "An error occured";
      });
    } else {
        hideLoader();
        console.error('Geolocation is not supported by this browser.');
        site_name.style.display = "none";
        site_description.style.display = "none";
        go_to_homepage.style.display = "none";
        google_destination.style.display = "none";
        site_address.innerText = "An error occured";
    }
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

function setupRouletteButton() {
    const spinRouletteButton = document.querySelector(".spin-roulette");
    spinRouletteButton.addEventListener('click', function() {
        window.location.href = "{% url 'randomtrip:next-destination' %}";
        document.addEventListener("DOMContentLoaded", spinRoulette());
    })
}

function main() {
    setupRouletteButton();
}

document.addEventListener('DOMContentLoaded', function() {
    main();
})