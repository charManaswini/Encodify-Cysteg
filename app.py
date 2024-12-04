from flask import Flask, render_template, redirect, url_for, flash, session, request
from config import Config
import pyotp
from extensions import db, bcrypt  # Import from extensions
from models import User  # Import models after db is set up
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions with the app
db.init_app(app)
bcrypt.init_app(app)

# Routes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        totp_secret = pyotp.random_base32()  # Generate TOTP secret key
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, totp_secret=totp_secret)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Login successful! Please complete 2FA.', 'info')
            return redirect(url_for('two_factor_auth'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'info')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/2fa', methods=['GET', 'POST'])
def two_factor_auth():
    if 'user_id' not in session:
        flash('Please log in first.', 'info')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        totp = pyotp.TOTP(user.totp_secret)
        if totp.verify(request.form.get('otp_code')):
            flash('2FA successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid 2FA code. Please try again.', 'danger')
    return render_template('2fa.html')


if __name__ == '__main__':
    app.run(debug=True)
