#FROM AI PA LAHAT HUHU, TRYING TO UNDERSTAND IT EVEN MORE
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Function to connect to the database
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="python_project",
        user="postgres",
        password="admin"
    )
    return conn

# ✅ GET: Retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    cur.close()
    conn.close()

    # Format the result as a list of dictionaries
    users_list = [{"id": user[0], "name": user[1], "age": user[2], "address": user[3]} for user in users]
    
    return jsonify(users_list)

# ✅ POST: Add a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()  # Get JSON payload from request
    name = data.get("name")
    age = data.get("age")
    address = data.get("address")

    if not name or not age or not address:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, age, address) VALUES (%s, %s, %s) RETURNING id;",
                (name, age, address))
    new_user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User added", "user_id": new_user_id}), 201

# ✅ PUT: Update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    address = data.get("address")

    if not name and not age and not address:
        return jsonify({"error": "No fields to update"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    update_fields = []
    values = []
    
    if name:
        update_fields.append("name = %s")
        values.append(name)
    if age:
        update_fields.append("age = %s")
        values.append(age)
    if address:
        update_fields.append("address = %s")
        values.append(address)

    values.append(user_id)

    query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s RETURNING id;"
    cur.execute(query, tuple(values))

    updated_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if updated_user:
        return jsonify({"message": "User updated", "user_id": updated_user[0]})
    else:
        return jsonify({"error": "User not found"}), 404

# ✅ DELETE: Remove a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s RETURNING id;", (user_id,))
    deleted_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if deleted_user:
        return jsonify({"message": "User deleted", "user_id": deleted_user[0]})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)  # Runs the Flask server
