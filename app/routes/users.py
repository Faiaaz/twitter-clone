from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import User, Tweet

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/dashboard")
@login_required
def dashboard():
    tweets = Tweet.query.order_by(Tweet.timestamp.desc()).all()
    return render_template("dashboard.html", tweets=tweets)


@user_bp.route("/users")
@login_required
def view_users():
    if current_user.username != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for("user_bp.dashboard"))

    users = User.query.all()
    return render_template("users.html", users=users)


@user_bp.route("/api/user/<username>")
def get_user_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    tweets = Tweet.query.filter_by(user=user).order_by(Tweet.timestamp.desc()).all()
    tweet_list = [
        {"id": t.id, "content": t.content, "timestamp": t.timestamp.strftime('%Y-%m-%d %H:%M')}
        for t in tweets
    ]

    return jsonify({
        "username": user.username,
        "tweets": tweet_list
    })


@user_bp.route("/api/user/<username>/tweets", methods=["GET"])
def get_user_tweets(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    tweets = Tweet.query.filter_by(user_id=user.id).order_by(Tweet.timestamp.desc()).all()
    tweet_list = [
        {
            "id": t.id,
            "user": t.user.username,
            "content": t.content,
            "timestamp": t.timestamp.strftime('%Y-%m-%d %H:%M')
        }
        for t in tweets
    ]

    return jsonify({"tweets": tweet_list})
