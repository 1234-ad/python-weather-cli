# Weather CLI Tool 🌤️

A command-line weather application that consumes the OpenWeatherMap API to provide current weather conditions and 5-day forecasts for any city worldwide.

## Features

- 🌡️ **Current Weather**: Get real-time weather conditions
- 📅 **5-Day Forecast**: Extended weather predictions
- 🔧 **Demo Mode**: Works without API key using sample data
- 🌍 **Global Coverage**: Weather for cities worldwide
- ⚖️ **Unit Options**: Metric (°C) or Imperial (°F) units
- 🎨 **Rich Output**: Formatted display with emojis and clear layout
- ⚡ **Fast & Reliable**: Built-in error handling and timeouts

## Installation

### Option 1: Clone and Run
```bash
git clone https://github.com/1234-ad/python-weather-cli.git
cd python-weather-cli
pip install -r requirements.txt
python weather_cli.py --help
```

### Option 2: Install as Package
```bash
git clone https://github.com/1234-ad/python-weather-cli.git
cd python-weather-cli
pip install -e .
weather-cli --help
```

## Usage

### Basic Commands

```bash
# Current weather (demo mode)
python weather_cli.py London

# 5-day forecast
python weather_cli.py "New York" --forecast

# Imperial units
python weather_cli.py Tokyo --units imperial

# With API key
python weather_cli.py Paris --api-key YOUR_API_KEY
```

### Command Line Options

```
positional arguments:
  city                  City name to get weather for

optional arguments:
  -h, --help            show this help message and exit
  --forecast, -f        Show 5-day forecast instead of current weather
  --units {metric,imperial}, -u {metric,imperial}
                        Temperature units (default: metric)
  --api-key API_KEY, -k API_KEY
                        OpenWeatherMap API key
```

## API Key Setup

### Get a Free API Key
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key

### Set API Key (Choose one method)

**Environment Variable (Recommended):**
```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

**Command Line Option:**
```bash
python weather_cli.py London --api-key your_api_key_here
```

## Example Output

### Current Weather
```
🌤️  Current Weather for London, GB
==================================================
🌡️  Temperature: 18.5°C (feels like 17.2°C)
☁️  Condition: Partly Cloudy
💧 Humidity: 72%
🔽 Pressure: 1015 hPa
💨 Wind: 4.1 m/s
👁️  Visibility: 10000 meters
```

### 5-Day Forecast
```
📅 5-Day Weather Forecast for London, GB
============================================================

📆 Monday, 2024-09-23
   🌡️  19.0°C
   ☁️  Light Rain
   💧 75% humidity

📆 Tuesday, 2024-09-24
   🌡️  22.0°C
   ☁️  Partly Cloudy
   💧 65% humidity
```

## Demo Mode

The application includes a demo mode that works without an API key, perfect for:
- Testing the application
- Demonstrating functionality
- Development and learning

Demo mode provides realistic sample weather data for any city you specify.

## Error Handling

The application includes comprehensive error handling for:
- Invalid city names
- Network connectivity issues
- API rate limits
- Invalid API keys
- Timeout scenarios

## Testing

Run the included unit tests:
```bash
python -m pytest test_weather_cli.py -v
```

Or run with unittest:
```bash
python test_weather_cli.py
```

## Technical Details

### Dependencies
- `requests`: HTTP library for API calls
- `argparse`: Command-line argument parsing (built-in)
- `datetime`: Date/time handling (built-in)

### API Endpoints Used
- Current Weather: `http://api.openweathermap.org/data/2.5/weather`
- 5-Day Forecast: `http://api.openweathermap.org/data/2.5/forecast`

### Supported Python Versions
- Python 3.7+
- Cross-platform (Windows, macOS, Linux)

## Project Structure

```
python-weather-cli/
├── weather_cli.py          # Main application
├── requirements.txt        # Dependencies
├── setup.py               # Package installation
├── test_weather_cli.py    # Unit tests
└── README.md              # Documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - feel free to use this project for learning and development.

## Acknowledgments

- Weather data provided by [OpenWeatherMap](https://openweathermap.org/)
- Built as part of Python Developer portfolio project