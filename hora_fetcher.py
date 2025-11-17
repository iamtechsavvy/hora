#!/usr/bin/env python3
"""
Daily Hora Timings Fetcher
Fetches hora timings from Free Astrology API daily
"""

import os
import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any


class HoraFetcher:
    """Fetches hora timings from the astrology API"""
    
    def __init__(self, api_key: Optional[str] = None, latitude: float = 30.2672, 
                 longitude: float = -97.7431, timezone: int = -6):
        """
        Initialize the HoraFetcher
        
        Args:
            api_key: API key for authentication (defaults to environment variable)
            latitude: Latitude coordinate (default: Austin, TX)
            longitude: Longitude coordinate (default: Austin, TX)
            timezone: Timezone offset (default: -6 for Austin, TX CST)
        """
        self.api_key = api_key or os.environ.get('ASTROLOGY_API_KEY')
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.endpoint = 'https://json.freeastrologyapi.com/hora-timings'
    
    def fetch_hora(self, year: Optional[int] = None, month: Optional[int] = None, 
                   date: Optional[int] = None, hours: int = 12, 
                   minutes: int = 0, seconds: int = 0) -> Dict[str, Any]:
        """
        Fetch hora timings for a specific date/time
        
        Args:
            year: Year (defaults to current year)
            month: Month (defaults to current month)
            date: Date (defaults to current date)
            hours: Hour of the day (default: 12)
            minutes: Minute (default: 0)
            seconds: Second (default: 0)
            
        Returns:
            dict: API response with hora timings
        """
        if not self.api_key:
            raise ValueError("API key not provided. Set ASTROLOGY_API_KEY environment variable or pass it to constructor.")
        
        # Use current date if not specified
        now = datetime.now()
        year = year or now.year
        month = month or now.month
        date = date or now.day
        
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        
        payload = {
            'year': year,
            'month': month,
            'date': date,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'timezone': self.timezone,
            'config': {
                'observation_point': 'geocentric',
                'ayanamsha': 'lahiri'
            }
        }
        
        try:
            response = requests.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching hora timings: {e}")
            raise
    
    def fetch_and_save(self, output_file: str = 'hora_results.json'):
        """
        Fetch hora timings and save to file
        
        Args:
            output_file: Path to save the results
        """
        print(f"Fetching hora timings for {datetime.now().strftime('%Y-%m-%d')}...")
        
        try:
            result = self.fetch_hora()
            
            # Add timestamp to result
            result['fetched_at'] = datetime.now().isoformat()
            
            # Save to file
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"✓ Successfully fetched and saved hora timings to {output_file}")
            return result
            
        except Exception as e:
            print(f"✗ Failed to fetch hora timings: {e}")
            raise


def main():
    """Main function to run the hora fetcher"""
    # Initialize with coordinates (can be overridden via environment variables)
    latitude = float(os.environ.get('LATITUDE', '30.2672'))
    longitude = float(os.environ.get('LONGITUDE', '-97.7431'))
    timezone = int(os.environ.get('TIMEZONE', '-6'))
    
    fetcher = HoraFetcher(
        latitude=latitude,
        longitude=longitude,
        timezone=timezone
    )
    
    # Fetch and save
    fetcher.fetch_and_save()


if __name__ == '__main__':
    main()
