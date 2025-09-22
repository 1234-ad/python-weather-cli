#!/usr/bin/env python3
"""
Weather CLI Tool
A command-line application to get current weather and forecasts using OpenWeatherMap API
"""

import requests
import json
import argparse
import sys
from datetime import datetime
import os

class WeatherCLI:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        if not self.api_key:
            print("⚠️  Warning: No API key provided. Using demo mode with sample data.")
            print("   To use real data, get a free API key from https://openweathermap.org/api")
            print("   Then set OPENWEATHER_API_KEY environment variable or use --api-key option")
    
    def get_current_weather(self, city, units='metric'):
        """Get current weather for a city"""
        if not self.api_key:
            return self._get_demo_weather(city)
        
        url = f"{self.base_url}/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': f"API request failed: {str(e)}"}
    
    def get_forecast(self, city, units='metric', days=5):
        """Get weather forecast for a city"""
        if not self.api_key:
            return self._get_demo_forecast(city)
        
        url = f"{self.base_url}/forecast"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units,
            'cnt': days * 8  # 8 forecasts per day (every 3 hours)
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': f"API request failed: {str(e)}"}
    
    def _get_demo_weather(self, city):
        """Return demo weather data when no API key is available"""
        return {
            'name': city.title(),
            'main': {
                'temp': 22.5,
                'feels_like': 24.1,
                'humidity': 65,
                'pressure': 1013
            },
            'weather': [{
                'main': 'Clear',
                'description': 'clear sky',
                'icon': '01d'
            }],
            'wind': {
                'speed': 3.2,
                'deg': 180
            },
            'visibility': 10000,
            'sys': {
                'country': 'DEMO'
            },
            'demo': True
        }
    
    def _get_demo_forecast(self, city):
        """Return demo forecast data when no API key is available"""
        return {
            'city': {
                'name': city.title(),
                'country': 'DEMO'
            },
            'list': [
                {
                    'dt': 1695398400,
                    'main': {
                        'temp': 25.0,
                        'humidity': 60
                    },
                    'weather': [{
                        'main': 'Sunny',
                        'description': 'sunny'
                    }],
                    'dt_txt': '2024-09-22 12:00:00'
                },
                {
                    'dt': 1695484800,
                    'main': {
                        'temp': 23.0,
                        'humidity': 70
                    },
                    'weather': [{
                        'main': 'Clouds',
                        'description': 'partly cloudy'
                    }],
                    'dt_txt': '2024-09-23 12:00:00'
                }
            ],
            'demo': True
        }
    
    def format_current_weather(self, data, units='metric'):
        """Format current weather data for display"""
        if 'error' in data:
            return f"❌ Error: {data['error']}"
        
        temp_unit = '°C' if units == 'metric' else '°F'
        speed_unit = 'm/s' if units == 'metric' else 'mph'
        
        demo_note = "\n🔧 DEMO MODE - Using sample data" if data.get('demo') else ""
        
        output = f"""
🌤️  Current Weather for {data['name']}, {data.get('sys', {}).get('country', 'N/A')}
{'='*50}
🌡️  Temperature: {data['main']['temp']}{temp_unit} (feels like {data['main']['feels_like']}{temp_unit})
☁️  Condition: {data['weather'][0]['description'].title()}
💧 Humidity: {data['main']['humidity']}%
🔽 Pressure: {data['main']['pressure']} hPa
💨 Wind: {data['wind']['speed']} {speed_unit}
👁️  Visibility: {data.get('visibility', 'N/A')} meters{demo_note}
"""
        return output
    
    def format_forecast(self, data, units='metric'):
        """Format forecast data for display"""
        if 'error' in data:
            return f"❌ Error: {data['error']}"
        
        temp_unit = '°C' if units == 'metric' else '°F'
        demo_note = "\n🔧 DEMO MODE - Using sample data" if data.get('demo') else ""
        
        output = f"""
📅 5-Day Weather Forecast for {data['city']['name']}, {data['city'].get('country', 'N/A')}
{'='*60}{demo_note}
"""
        
        # Group forecasts by date
        daily_forecasts = {}
        for item in data['list'][:40]:  # Limit to 5 days
            date = item['dt_txt'].split(' ')[0]
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(item)
        
        for date, forecasts in list(daily_forecasts.items())[:5]:
            # Get midday forecast or first available
            midday_forecast = next((f for f in forecasts if '12:00:00' in f['dt_txt']), forecasts[0])
            
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            day_name = date_obj.strftime('%A')
            
            output += f"""
📆 {day_name}, {date}
   🌡️  {midday_forecast['main']['temp']}{temp_unit}
   ☁️  {midday_forecast['weather'][0]['description'].title()}
   💧 {midday_forecast['main']['humidity']}% humidity
"""
        
        return output

def main():
    parser = argparse.ArgumentParser(
        description='Get weather information from the command line',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python weather_cli.py London
  python weather_cli.py "New York" --forecast
  python weather_cli.py Tokyo --units imperial
  python weather_cli.py Paris --api-key YOUR_API_KEY
        """
    )
    
    parser.add_argument('city', help='City name to get weather for')
    parser.add_argument('--forecast', '-f', action='store_true', 
                       help='Show 5-day forecast instead of current weather')
    parser.add_argument('--units', '-u', choices=['metric', 'imperial'], 
                       default='metric', help='Temperature units (default: metric)')
    parser.add_argument('--api-key', '-k', help='OpenWeatherMap API key')
    
    args = parser.parse_args()
    
    # Initialize weather CLI
    weather = WeatherCLI(api_key=args.api_key)
    
    try:
        if args.forecast:
            data = weather.get_forecast(args.city, args.units)
            output = weather.format_forecast(data, args.units)
        else:
            data = weather.get_current_weather(args.city, args.units)
            output = weather.format_current_weather(data, args.units)
        
        print(output)
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()