#!/usr/bin/env python3
"""
Hora Widget - macOS Menu Bar App
Displays current hora timings in your menu bar
"""

import os
import rumps
import json
from datetime import datetime
from hora_fetcher import HoraFetcher
import threading
import time


class HoraWidget(rumps.App):
    """macOS menu bar widget for Hora timings"""
    
    def __init__(self):
        super(HoraWidget, self).__init__("🕉️", quit_button="Quit")
        self.fetcher = HoraFetcher(
            latitude=float(os.environ.get('LATITUDE', '30.2672')),
            longitude=float(os.environ.get('LONGITUDE', '-97.7431')),
            timezone=int(os.environ.get('TIMEZONE', '-6'))
        )
        self.hora_data = None
        self.current_hora = None
        
        # Menu items
        self.menu = [
            rumps.MenuItem("Current Hora: Loading...", callback=None),
            rumps.separator,
            rumps.MenuItem("Today's Horas", callback=self.show_all_horas),
            rumps.MenuItem("Refresh Now", callback=self.refresh_data),
            rumps.separator,
        ]
        
        # Load initial data
        self.load_data()
        
        # Start background update thread
        self.start_update_thread()
    
    def load_data(self):
        """Load hora data from file or fetch new"""
        try:
            # Try to load from file first
            if os.path.exists('hora_results.json'):
                with open('hora_results.json', 'r') as f:
                    data = json.load(f)
                    # Parse the nested JSON string in 'output'
                    if 'output' in data and isinstance(data['output'], str):
                        self.hora_data = json.loads(data['output'])
                    else:
                        self.hora_data = data
                    self.update_current_hora()
            else:
                self.refresh_data(None)
        except Exception as e:
            print(f"Error loading data: {e}")
            rumps.notification("Hora Widget", "Error", f"Failed to load data: {e}")
    
    def refresh_data(self, _):
        """Fetch fresh hora data"""
        try:
            rumps.notification("Hora Widget", "Fetching", "Updating hora timings...")
            result = self.fetcher.fetch_and_save()
            # Parse the nested JSON string in 'output'
            if 'output' in result and isinstance(result['output'], str):
                self.hora_data = json.loads(result['output'])
            else:
                self.hora_data = result
            self.update_current_hora()
            rumps.notification("Hora Widget", "Success", "Hora timings updated!")
        except Exception as e:
            rumps.notification("Hora Widget", "Error", f"Failed to fetch: {e}")
    
    def update_current_hora(self):
        """Update the current hora display"""
        if not self.hora_data:
            return
        
        now = datetime.now()
        
        # Planet emoji mapping
        planet_emoji = {
            'Sun': '☀️',
            'Moon': '🌙',
            'Mars': '♂️',
            'Mercury': '☿️',
            'Jupiter': '♃',
            'Venus': '♀️',
            'Saturn': '♄'
        }
        
        # Find current hora
        for hora_num, hora_info in self.hora_data.items():
            lord = hora_info['lord']
            start = datetime.fromisoformat(hora_info['starts_at'])
            end = datetime.fromisoformat(hora_info['ends_at'])
            
            if start <= now < end:
                self.current_hora = hora_info
                emoji = planet_emoji.get(lord, '🌟')
                self.title = f"{emoji} {lord}"
                self.menu["Current Hora: Loading..."].title = f"Current: {lord} Hora"
                return
        
        self.title = "🕉️"
        self.menu["Current Hora: Loading..."].title = "Current Hora: Unknown"
    
    def show_all_horas(self, _):
        """Show all horas for today"""
        if not self.hora_data:
            rumps.alert("No Data", "Please refresh to fetch hora timings")
            return
        
        message = "Today's Hora Timings:\n\n"
        now = datetime.now()
        
        # Planet emoji mapping
        planet_emoji = {
            'Sun': '☀️',
            'Moon': '🌙',
            'Mars': '♂️',
            'Mercury': '☿️',
            'Jupiter': '♃',
            'Venus': '♀️',
            'Saturn': '♄'
        }
        
        for hora_num, hora_info in self.hora_data.items():
            lord = hora_info['lord']
            start = datetime.fromisoformat(hora_info['starts_at'])
            end = datetime.fromisoformat(hora_info['ends_at'])
            
            # Highlight current hora
            marker = "→ " if start <= now < end else "   "
            emoji = planet_emoji.get(lord, '🌟')
            
            message += f"{marker}{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}: {emoji} {lord}\n"
        
        rumps.alert("Today's Horas", message)
    
    def start_update_thread(self):
        """Start background thread to update current hora"""
        def update_loop():
            while True:
                time.sleep(60)  # Update every minute
                self.update_current_hora()
                
                # Fetch new data at midnight
                if datetime.now().hour == 0 and datetime.now().minute == 0:
                    self.refresh_data(None)
        
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()


if __name__ == "__main__":
    # Load environment variables from .env file if available
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    
    app = HoraWidget()
    app.run()