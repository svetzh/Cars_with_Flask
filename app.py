from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def insert_data(cursor, connection, model, year, engine):
    cursor.execute("INSERT INTO cars (model, year, engine) VALUES (?, ?, ?)", (model, year, engine))
    connection.commit()

def check_car_existence(cursor, model, year, engine):
    cursor.execute("SELECT * FROM cars WHERE model=? AND year=? AND engine=?", (model, year, engine))
    return cursor.fetchone() is not None

def reset_autoincrement(cursor, table_name):
    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")
    cursor.connection.commit()
    cursor.execute("VACUUM")

@app.route('/')
def index():
    # Connect SQL db
    connection = sqlite3.connect("cars.db")
    cursor = connection.cursor()

    # Reset auto-increment
    reset_autoincrement(cursor, "cars")

    # Clear 'cars' table
    cursor.execute("DELETE FROM cars")
    connection.commit()

    # Create cars table
    cursor.execute("CREATE TABLE IF NOT EXISTS cars (id INTEGER PRIMARY KEY AUTOINCREMENT, model TEXT, year INTEGER, engine TEXT)")
    connection.commit()

    # Insert data into 'cars'
    car_models = [
        ("BMW", 2022, "3.0"),
        ("Audi", 2015, "2.0"),
        ("Vw", 2010, "1.0")
    ]
    for car in car_models:
        model, year, engine = car
        if not check_car_existence(cursor, model, year, engine):
            insert_data(cursor, connection, model, year, engine)

    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()

    connection.close()

    # Render template
    return render_template('index.html', cars=cars)


if __name__ == '__main__':
    app.run(debug=True)

