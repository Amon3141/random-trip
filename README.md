# RandomTrip

A Django web application to guide a fun, randomized trip in Japan. The app selects random tourism sites within a specified distance and provides relevant information (descriptions, homepage URLs, Google Maps integration).

**Note:** Currently optimized for Japanese tourism sites. Select "All" if you are outside of Japan.

<img width="400" alt="RandomTrip demo 1" src="https://github.com/user-attachments/assets/b15ad3f1-a569-4686-882a-47e1eb3ba31c" />
<img width="400" alt="RandomTrip demo 2" src="https://github.com/user-attachments/assets/23734a9f-96b1-4307-964c-8903eda34348" />
<img width="400" alt="RandomTrip demo 3" src="https://github.com/user-attachments/assets/7b8ae669-cb78-49c4-8100-5f945efc31bf" />
<img width="400" alt="RandomTrip demo 4" src="https://github.com/user-attachments/assets/880c0f72-a05d-46d6-85b0-a749e1c45d1b" />

## Features

- Random tourism site selection within specified radius
- User authentication and trip management
- Activity categorization (Tourism, Food, Lodging)
- Geographic coordinate-based site filtering
- Web scraping for tourism data collection

## Prerequisites

- Python 3.8 or higher
- Chrome browser (for web scraping functionality)
- Git

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd random-trip
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

## Running the Application

1. **Start the development server**
   ```bash
   python manage.py runserver
   ```

2. **Open your browser and navigate to**
   ```
   http://127.0.0.1:8000/
   ```

## Usage

1. **Register/Login**: Create an account or log in to manage your trips
2. **Set Location**: Enter your current location coordinates
3. **Choose Radius**: Select the search radius in kilometers
4. **Get Random Site**: Click the roulette to get a random tourism site
5. **Manage Trips**: Create and organize your trips with activities

## Common Issues and Solutions

#### 1. **"DisallowedHost" Error**
**Problem**: Django blocks requests from 127.0.0.1:8000.

**Solution**: 
- Add `'127.0.0.1'` to `ALLOWED_HOSTS` in `config/settings.py`

#### 2. **"Location unavailable" Error**
**Problem**: Geolocation fails with error code 2.

**Solution**:
- **macOS**: System Preferences → Security & Privacy → Privacy → Location Services
  - Enable Location Services
  - Allow your browser to access location
- **Browser Settings**: Allow location access for localhost
- **Manual Fallback**: Enter coordinates manually when GPS fails

### Manual Location Coordinates

When GPS fails, you can enter coordinates manually:

- **Tokyo**: 35.6762, 139.6503
- **Osaka**: 34.6937, 135.5023
- **Kyoto**: 35.0116, 135.7681
- **Yokohama**: 35.4437, 139.6380
- **Nagoya**: 35.1815, 136.9066

## Project Structure

```
random-trip/
├── accounts/          # User authentication app
├── config/           # Django project settings
├── randomtrip/       # Main application
│   ├── python_functions/  # Data processing utilities
│   └── ...
├── static/           # Static files (CSS, JS)
├── templates/        # HTML templates
├── data/            # CSV data files
└── manage.py        # Django management script
```

## Dependencies

- **Django**: Web framework
- **Selenium**: Web scraping and browser automation
- **BeautifulSoup**: HTML parsing
- **Pandas**: Data manipulation
- **Geopy/Geocoder**: Geographic coordinate services
- **NumPy**: Numerical computations
