# Auckland Waze Police Feed
 Waze Police Feed that sends data to discourse instance

# Auckland Police Feed README.md

## Overview
Auckland Police Feed is a Python script that monitors and logs police coordinates using data from Waze and Mapbox. The script is designed to alert users when police are detected within the specified coordinates. It can also send alerts to a discourse webhook URL.

## Features
- Retrieves police coordinates from Waze.
- Resolves coordinates to a location using Mapbox API.
- Logs the locations to a file.
- Sends alerts through a webhook.
- Continuously runs and checks for updates every 10 seconds.

## Dependencies
- Python 3
- `requests`

## How to Run
1. Ensure that you have Python 3 installed.
2. Install the necessary package:
   ```sh
   pip install requests
   ```
3. Clone the repository or download the Python script.
4. Run the script using Python 3:
   ```sh
   python3 police_detect.py
   ```

## Configuration
- **Webhook URL**: Modify the `webhook_url` in the `send_data` function to your desired endpoint.
- **Mapbox Access Token**: The Mapbox Access Token is hardcoded in the `get_location_mapbox` function. Change it if you have a different access token.
- **Headers & Waze URL**: The headers and Waze URL in `get_police_coordinates_from_waze` can be modified if needed.

## How It Works
1. The script gets police coordinates from Waze by sending a GET request to Waze's TGeoRSS endpoint with the specified coordinates and filters.
2. It resolves these coordinates to an address using the Mapbox API.
3. The addresses are written to a log file named `police_coordinates.log`.
4. If there is a difference in content between runs, the script calculates the added and removed items and prints them to the console.
5. Optionally, the script can also send this data as an alert to a specified webhook URL.
6. The script runs indefinitely, checking for updates every 10 seconds.

## Notes
- The script currently prints detected police locations and removed detections to the console. To enable sending this data as alerts to a webhook, uncomment the corresponding lines in the script.

## License
This project is open-source and available to everyone. Please use it responsibly and ethically. Keep in mind the terms of service of the utilized APIs.

## Author
- ezy