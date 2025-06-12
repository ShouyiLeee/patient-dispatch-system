import math
from typing import Dict, Tuple, List, Optional


def haversine_distance(coord1: Dict[str, float], coord2: Dict[str, float]) -> float:
    """
    Calculate the great-circle distance between two points on Earth.
    
    Args:
        coord1: Dictionary with 'latitude' and 'longitude' keys
        coord2: Dictionary with 'latitude' and 'longitude' keys
        
    Returns:
        Distance in kilometers
    """
    # Extract coordinates
    lat1 = coord1.get('latitude', 0)
    lon1 = coord1.get('longitude', 0)
    lat2 = coord2.get('latitude', 0)
    lon2 = coord2.get('longitude', 0)
    
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Earth radius in kilometers
    r = 6371
    
    # Calculate distance
    return r * c


def estimate_travel_time(
    distance_km: float, 
    avg_speed_kmh: float = 50, 
    traffic_factor: float = 1.0
) -> int:
    """
    Estimate travel time based on distance and average speed.
    
    Args:
        distance_km: Distance in kilometers
        avg_speed_kmh: Average speed in kilometers per hour
        traffic_factor: Multiplier for traffic conditions (1.0 = normal, 2.0 = heavy traffic)
        
    Returns:
        Estimated travel time in minutes
    """
    # Calculate time in hours, adjusted for traffic
    time_hours = (distance_km / avg_speed_kmh) * traffic_factor
    
    # Convert to minutes and round to integer
    return round(time_hours * 60)


def find_nearest_locations(
    origin: Dict[str, float],
    locations: List[Dict],
    max_distance: Optional[float] = None,
    max_results: Optional[int] = None,
    location_key: str = 'location'
) -> List[Tuple[Dict, float]]:
    """
    Find nearest locations from a list of locations.
    
    Args:
        origin: Dictionary with 'latitude' and 'longitude' keys
        locations: List of dictionaries containing location data
        max_distance: Optional maximum distance in kilometers
        max_results: Optional maximum number of results to return
        location_key: Key in location dictionaries containing coordinates
        
    Returns:
        List of tuples (location, distance_km) sorted by distance
    """
    results = []
    
    for location in locations:
        # Skip locations without coordinates
        if location_key not in location:
            continue
        
        coords = location[location_key]
        
        # Calculate distance
        distance = haversine_distance(origin, coords)
        
        # Apply distance filter if specified
        if max_distance is not None and distance > max_distance:
            continue
        
        results.append((location, distance))
    
    # Sort by distance
    results.sort(key=lambda x: x[1])
    
    # Apply limit if specified
    if max_results is not None:
        results = results[:max_results]
    
    return results