#Climate Change POC

This is a Proof of Concept (POC) project for tracking climate data and performing climate change calculations.

**Table of Contents**
Introduction
Getting Started
Prerequisites
Installation
Usage
Running the Server
API Endpoints
Contributing
License

**Introduction**
This project is a backend system that allows users to save climate data, retrieve saved records, and calculate climate change statistics. It provides a set of API endpoints for interacting with the data.

**Getting Started**
**Prerequisites**
Before you begin, ensure you have met the following requirements:

Python 3.x installed
Flask framework installed (pip install Flask)
SQLite database set up

**Installation**
Clone this repository: git clone https://github.com/your-username/climate-change-poc.git
Navigate to the project directory: cd ONBO

Install project dependencies: pip install -r requirements.txt

**Usage**
**Running the Server**
To run the server, execute the following command: python app.py
The server will start, and you can access it at http://127.0.0.1:5000 in your web browser or through API requests.
  
**API Endpoints**
**Save Climate Data:**
URL: /save_data
Method: POST
Payload: JSON data containing climate information (climate, area_code, temperature, humidity, chances_of_rain).
Response: JSON response indicating success or failure.

**Fetch All Records:**
URL: /fetch_all_records
Method: GET
Response: JSON array containing all saved climate records.

**Fetch Records by Area:**
URL: /fetch_records_by_area/<int:area_code>
Method: GET
Response: JSON array containing climate records for the specified area code.

****Fetch Records by Climate and Area:
URL: /fetch_records_by_climate/<int:area_code>/<string:climate>
Method: GET
Response: JSON array containing climate records for the specified area code and climate.

**Calculate Climate Change:**
URL: /calculate_climate_change
Method: POST
Payload: JSON data specifying from_climate, to_climate, and area_code.
Response: JSON with climate change calculations (climate_delta, temperature_delta, humidity_delta, rain_chances_delta, climate_change_index).

**Contributing**
Contributions are welcome! Feel free to open issues or submit pull requests to help improve this project.

**License**
This project is licensed under the MIT License - see the LICENSE file for details.

