import numpy as np
import pandas as pd
import random
import os
from django.conf import settings

csv_file_path = os.path.join(settings.BASE_DIR, 'data/site_data.csv')
site_df = pd.read_csv(csv_file_path)

def km_to_degrees_latitude(km):
  return km / 111

def km_to_degrees_longitude(km, latitude):
  latitude_rad = np.deg2rad(latitude)
  return km / (111 * np.cos(latitude_rad))

# point and center are tuples
def is_point_inside_ellipse(point, center, semi_major_axis, semi_minor_axis):
    x, y = point
    p, q = center
    a = semi_major_axis
    b = semi_minor_axis
    inside = ((x - p)**2 / a**2) + ((y - q)**2 / b**2) <= 1
    return inside

def get_random_site(latitude, longitude, radius):
  radius_lat = km_to_degrees_latitude(radius)
  radius_lng = km_to_degrees_longitude(radius, latitude)

  site_candidate = site_df[
    site_df.apply(lambda row: is_point_inside_ellipse(
      (row["Latitude"], row["Longitude"]), 
      (latitude, longitude), 
      radius_lat, 
      radius_lng), 
    axis=1)]
  
  num_candidate = len(site_candidate)
  print(num_candidate)
  if num_candidate > 0:
    random_site_idx = random.randint(0, num_candidate-1)
    random_site = site_candidate.iloc[random_site_idx]
    return random_site["Name"], random_site["Address"], random_site["Description"], random_site["Homepage"]
  else:
    return None, None, None, None

#print(get_random_site(36.9863379, 138.7441532, 100))