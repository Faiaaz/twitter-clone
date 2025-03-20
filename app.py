from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Secret key for session security
app.config["SESSION_TYPE"] = "filesystem"

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


# user registration
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json  # Get JSON data from React
    username = data.get("username")
    password = data.get("password")

    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already taken"}), 400

    # Hash the password and create a new user
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful!"}), 201


# User Login
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json  # Get JSON data from React
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful", "username": username}), 200


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
# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     flash("Logged out successfully", "success")
#     return redirect(url_for("login"))


@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)  # Remove user session
    return jsonify({"message": "Logged out successfully!"}), 20


# create API Endpoint for Tweets
@app.route("/api/tweets")
def get_tweets():
    tweets = Tweet.query.order_by(Tweet.timestamp.desc()).all()
    tweet_list = [
        {"id": t.id, "user": t.user.username, "content": t.content, "timestamp": t.timestamp.strftime('%Y-%m-%d %H:%M')}
        for t in tweets]
    return {"tweets": tweet_list}


@app.route("/api/tweets", methods=["POST"])
def post_tweet():
    data = request.json  # Ensure we receive JSON data
    username = data.get("username")
    content = data.get("content")

    if not username or not content:
        return jsonify({"error": "Username and content are required"}), 400

    # Find user in database
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Save tweet in database
    new_tweet = Tweet(user=user, content=content)
    db.session.add(new_tweet)
    db.session.commit()

    return jsonify({
        "message": "Tweet posted successfully!",
        "tweet": {
            "id": new_tweet.id,
            "content": new_tweet.content,
            "timestamp": new_tweet.timestamp.strftime('%Y-%m-%d %H:%M')
        }
    }), 201

@app.route("/api/tweet/<int:tweet_id>", methods=["PUT"])
def edit_tweet(tweet_id):
    data = request.json
    new_content = data.get("content")
    username = data.get("username")

    if not new_content or not username:
        return jsonify({"error": "Content and username are required"}), 400

    tweet = Tweet.query.get(tweet_id)

    if not tweet:
        return jsonify({"error": "Tweet not found"}), 404

    if tweet.user.username != username:
        return jsonify({"error": "You can only edit your own tweets"}), 403

    tweet.content = new_content
    db.session.commit()
    return jsonify({"message": "Tweet updated successfully!"})


@app.route("/api/tweet/<int:tweet_id>", methods=["DELETE"])
def delete_tweet(tweet_id):
    data = request.json
    username = data.get("username")

    tweet = Tweet.query.get(tweet_id)

    if not tweet:
        return jsonify({"error": "Tweet not found"}), 404

    if tweet.user.username != username:
        return jsonify({"error": "You can only delete your own tweets"}), 403

    db.session.delete(tweet)
    db.session.commit()
    return jsonify({"message": "Tweet deleted successfully!"})


@app.route("/api/user/<username>")
def get_user_profile(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    tweets = Tweet.query.filter_by(user=user).order_by(Tweet.timestamp.desc()).all()
    tweet_list = [{"id": t.id, "content": t.content, "timestamp": t.timestamp.strftime('%Y-%m-%d %H:%M')} for t in
                  tweets]

    return jsonify({
        "username": user.username,
        "tweets": tweet_list
    })


@app.route("/api/user/<username>/tweets", methods=["GET"])
def get_user_tweets(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    tweets = Tweet.query.filter_by(user_id=user.id).order_by(Tweet.timestamp.desc()).all()
    tweet_list = [
        {"id": t.id, "user": t.user.username, "content": t.content, "timestamp": t.timestamp.strftime('%Y-%m-%d %H:%M')}
        for t in tweets]

    return jsonify({"tweets": tweet_list})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
