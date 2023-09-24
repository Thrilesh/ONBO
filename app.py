from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
conn = sqlite3.connect('climate_data.db')
cursor = conn.cursor()

# Create a table to store climate data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS climate_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        climate TEXT,
        area_code INTEGER,
        temperature REAL,
        humidity REAL,
        chances_of_rain REAL
    )
''')
conn.commit()
conn.close()


@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()

    # Validate payload
    valid_climates = ['hot', 'humid', 'rainy', 'cold']
    if (
        'climate' not in data or
        'area_code' not in data or
        'temperature' not in data or
        'humidity' not in data or
        'chances_of_rain' not in data or
        data['climate'] not in valid_climates or
        not (100 <= data['area_code'] <= 1000)
    ):
        return jsonify({"success": False, "error": "Invalid payload"}), 400

    # Save data to the database
    conn = sqlite3.connect('climate_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO climate_data (climate, area_code, temperature, humidity, chances_of_rain)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['climate'], data['area_code'], data['temperature'], data['humidity'], data['chances_of_rain']))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "error": None, "data": {"id": "any_random_unique_id"}})


@app.route('/fetch_all_records', methods=['GET'])
def fetch_all_records():
    conn = sqlite3.connect('climate_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM climate_data')
    records = cursor.fetchall()
    conn.close()

    data = [{"id": record[0], "climate": record[1], "area_code": record[2], "temperature": record[3],
             "humidity": record[4], "chances_of_rain": record[5]} for record in records]

    return jsonify(data)


@app.route('/fetch_records_by_area/<int:area_code>', methods=['GET'])
def fetch_records_by_area(area_code):
    conn = sqlite3.connect('climate_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM climate_data WHERE area_code = ?', (area_code,))
    records = cursor.fetchall()
    conn.close()

    if not records:
        return jsonify({"success": False, "error": "No records found for the specified area_code"}), 404

    data = [{"id": record[0], "climate": record[1], "area_code": record[2], "temperature": record[3],
             "humidity": record[4], "chances_of_rain": record[5]} for record in records]

    return jsonify(data)


@app.route('/fetch_records_by_climate/<int:area_code>/<string:climate>', methods=['GET'])
def fetch_records_by_climate(area_code, climate):
    conn = sqlite3.connect('climate_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM climate_data WHERE area_code = ? AND climate = ?', (area_code, climate))
    records = cursor.fetchall()
    conn.close()

    if not records:
        return jsonify({"success": False, "error": "No records found for the specified area_code and climate"}), 404

    data = [{"id": record[0], "climate": record[1], "area_code": record[2], "temperature": record[3],
             "humidity": record[4], "chances_of_rain": record[5]} for record in records]

    return jsonify(data)


@app.route('/calculate_climate_change', methods=['POST'])
def calculate_climate_change():
    data = request.get_json()

    from_climate = data['from_climate']
    to_climate = data['to_climate']
    area_code = data['area_code']

    conn = sqlite3.connect('climate_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT temperature, humidity, chances_of_rain FROM climate_data WHERE area_code = ? AND climate = ?',
                   (area_code, from_climate))
    from_records = cursor.fetchall()

    cursor.execute('SELECT temperature, humidity, chances_of_rain FROM climate_data WHERE area_code = ? AND climate = ?',
                   (area_code, to_climate))
    to_records = cursor.fetchall()

    conn.close()

    if not from_records or not to_records:
        return jsonify({"success": False, "error": "Records not found for the specified climates and area_code"}), 404

    # Calculate deltas
    temperature_delta = (
            sum(record[0] for record in to_records) - sum(record[0] for record in from_records)) / len(from_records)
    humidity_delta = (
            sum(record[1] for record in to_records) - sum(record[1] for record in from_records)) / len(from_records)
    rain_chances_delta = (
            sum(record[2] for record in to_records) - sum(record[2] for record in from_records)) / len(from_records)

    climate_delta = f"{from_climate} -> {to_climate}"

    climate_change_index = (temperature_delta * humidity_delta) / rain_chances_delta

    result = {
        "climate_delta": climate_delta,
        "temperature_delta": temperature_delta,
        "humidity_delta": humidity_delta,
        "rain_chances_delta": rain_chances_delta,
        "climate_change_index": climate_change_index
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
