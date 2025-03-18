from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Secret key for session security

CORS(app)  # Enable CORS for all routes

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"  # Using SQLite
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect if not logged in


# User model for the database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


# Tweet model for storing user posts
class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.String(280), nullable=False)  # Max 280 characters (like Twitter)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Relationship to get the User object
    user = db.relationship("User", backref="tweets")

# Create tables before running the app
with app.app_context():
    db.create_all()


# Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# User Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")  # Hash the password

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already taken!", "danger")
            return redirect(url_for("register"))

        # Create a new user and store it in the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# User Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")


# add a new route for posting tweets

@app.route("/tweet", methods=["POST"])
@login_required
def tweet():
    content = request.form.get("content")

    if not content or len(content) > 280:
        flash("Tweet cannot be empty or exceed 280 characters!", "danger")
        return redirect(url_for("dashboard"))

    new_tweet = Tweet(user_id=current_user.id, content=content)
    db.session.add(new_tweet)
    db.session.commit()

    flash("Tweet posted successfully!", "success")
    return redirect(url_for("dashboard"))


# Protected Dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    tweets = Tweet.query.order_by(Tweet.timestamp.desc()).all()  # Get all tweets from all users
    return render_template("dashboard.html", tweets=tweets)

@app.route("/users")
@login_required  # Only logged-in users can see this
def view_users():
    if current_user.username != "admin":  # Only allow the admin to see users
        flash("Access denied!", "danger")
        return redirect(url_for("dashboard"))

    users = User.query.all()
    return render_template("users.html", users=users)


# User Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("login"))

# create API Endpoint for Tweets
@app.route("/api/tweets")
def get_tweets():
    tweets = Tweet.query.order_by(Tweet.timestamp.desc()).all()
    tweet_list = [{"id": t.id, "user": t.user.username, "content": t.content, "timestamp": t.timestamp.strftime('%Y-%m-%d %H:%M')} for t in tweets]
    return {"tweets": tweet_list}

if __name__ == "__main__":
    app.run(debug=True)
