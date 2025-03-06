from flask import Flask, render_template, request, redirect, url_for, session, flash
import db_config

app = Flask(__name__)
app.secret_key = "secretkey"  # For session handling

# Render Login & Registration Page
@app.route('/')
def login():
    return render_template('login.html')

# Handle Registration
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    conn = db_config.get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        conn.commit()
        flash("Registration Successful! Please login.", "success")
    except db_config.mysql.connector.Error as err:
        flash("Error: " + str(err), "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('login'))

# Handle Login
@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    conn = db_config.get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        session['user_id'] = user['id']
        session['username'] = user['name']
        return redirect(url_for('home'))
    else:
        flash("Invalid Credentials!", "danger")
        return redirect(url_for('login'))

# Home Page After Login
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

# 📌 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)