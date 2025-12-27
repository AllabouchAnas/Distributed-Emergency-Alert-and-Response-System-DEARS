"""
Distance calculation utilities for proximity-based unit assignment.
Uses the Haversine formula to calculate distances between geographic coordinates.
"""
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points on Earth.
    
    Args:
        lat1 (float): Latitude of point 1 in decimal degrees
        lon1 (float): Longitude of point 1 in decimal degrees
        lat2 (float): Latitude of point 2 in decimal degrees
        lon2 (float): Longitude of point 2 in decimal degrees
    
    Returns:
        float: Distance in kilometers
    """
    if None in (lat1, lon1, lat2, lon2):
        return float('inf')  # Return infinity if any coordinate is missing
    
    # Convert decimal degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Earth's radius in kilometers
    earth_radius_km = 6371.0
    
    distance = earth_radius_km * c
    return distance


def parse_coordinates_from_location(location_string):
    """
    Extract latitude and longitude from a location string if present.
    Format expected: "Address (lat, lon)" or just coordinates "lat, lon"
    
    Args:
        location_string (str): Location string that may contain coordinates
    
    Returns:
        tuple: (latitude, longitude) or (None, None) if not found
    """
    if not location_string:
        return None, None
    
    try:
        # Try to extract coordinates from parentheses: "Address (lat, lon)"
        if '(' in location_string and ')' in location_string:
            coords_str = location_string[location_string.find('(')+1:location_string.find(')')]
            parts = coords_str.split(',')
            if len(parts) == 2:
                lat = float(parts[0].strip())
                lon = float(parts[1].strip())
                return lat, lon
        
        # Try parsing as direct coordinates "lat, lon"
        parts = location_string.split(',')
        if len(parts) == 2:
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            return lat, lon
    except (ValueError, IndexError):
        pass
    
    return None, None
