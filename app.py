from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/reports'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key = 'your_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import Report, User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stories')
def stories():
    return render_template('stories.html')


@app.route('/home')
def home():
    return render_template('base.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        if current_user.is_authenticated:
            user = current_user
            report_count = len(user.reports)
            return render_template('profile.html', user=user, report_count=report_count)
        else:
            # Handle the case when no user is logged in
            return 'No user logged in'
    return render_template('profile.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Store the user's session
            session['username'] = username
            login_user(user)
            return redirect(url_for('profile'))
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html', error=error)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        mobile = request.form['mobile']
        user_agent = request.headers.get('User-Agent')
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr
        existing_ip = User.query.filter_by(ip_address=ip).first()
        existing_email = User.query.filter_by(email=email).first()
        existing_user = User.query.filter_by(username=username).first()
        existing_mobile = User.query.filter_by(mobile=mobile).first()
        existing_agent = User.query.filter_by(user_agent=user_agent).first()
        if existing_user:
            error = "This username already exists."
            return render_template('signup.html', error=error)
        if existing_email and email != "":
            error = "This email already exists."
            return render_template('signup.html', error=error)
        if existing_mobile and mobile != "":
            error = "This mobile number already exists."
            return render_template('signup.html', error=error)
        if existing_ip and existing_agent:
            error = "You can create one account per device only."
            return render_template('signup.html', error=error)
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password, email=email, mobile=mobile, user_agent=user_agent,
                        ip_address=ip)
        db.session.add(new_user)
        db.session.commit()
        if error is None:
            login_user(new_user)
            return redirect(url_for('login'))
    return render_template('signup.html', error=error)


# Route to save marker data
@app.route('/save_report', methods=['POST'])
def save_report():
    data = request.json
    input_value = data.get('input')
    latlng = data.get('latlng')
    if current_user.is_authenticated:
        user = current_user
        print(user)
        print(user.id)
        # Create a new record in the database
        new_report = Report(report_text=input_value, location_lat=latlng.get('lat'), location_lang=latlng.get('lng'), user_id=user.id)
        db.session.add(new_report)
        db.session.commit()

        return jsonify({'message': 'Report saved successfully!'})
    else:
        return jsonify({'message': 'Please login.'})


if __name__ == '__main__':
    app.run(debug=True)
