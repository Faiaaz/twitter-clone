from flask import Blueprint, request, jsonify
from app.models import Tweet, User
from app.extensions import db

tweet_bp = Blueprint("tweet_bp", __name__, url_prefix="/api")

@tweet_bp.route("/tweets", methods=["GET"])
def get_tweets():
    tweets = Tweet.query.order_by(Tweet.timestamp.desc()).all()
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


@tweet_bp.route("/tweets", methods=["POST"])
def post_tweet():
    data = request.json
    username = data.get("username")
    content = data.get("content")

    if not username or not content:
        return jsonify({"error": "Username and content are required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

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


@tweet_bp.route("/tweet/<int:tweet_id>", methods=["PUT"])
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


@tweet_bp.route("/tweet/<int:tweet_id>", methods=["DELETE"])
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
