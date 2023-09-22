from flask import Flask, render_template, request, url_for, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.template_folder = 'src/templates'
app.static_folder = 'src/assets'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/jhonathan/Documentos/Project/database.db'

db = SQLAlchemy(app)

class user(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        fullname = db.Column(db.String(128), nullable=False)
        email = db.Column(db.String(128), unique=True, nullable=False)
        password = db.Column(db.String(500), nullable=False)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/signin', methods=['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']
    
    user_l = user.query.filter_by(email=email).first()
    
    if user_l and check_password_hash(user_l.password, password):
        status = 'success'
        message = 'Login successful!'
    else:
        status = 'danger'
        message = 'Incorrect email or password. Please try again.'

    response_data = {
        "type": status,
        "body": {
            "message": message
        }
    }
    response = jsonify(response_data)
    response.status_code = 200
    return response  

@app.route('/signup', methods=['POST'])
def signup():
    fullname = request.form['fullname']
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password, method='scrypt')
    
    new_user = user(fullname=fullname, email=email, password=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        status = 'success'
        message = url_for('login')

    except Exception:
        status = 'danger'
        message = 'There was an error logging in. Try another email.'
        
    response_data = {
        "type": status,
        "body": {
            "message": message
        }
    }
    response = jsonify(response_data)
    response.status_code = 200
    return response  

if __name__ == '__main__':
    app.run(debug=True)
