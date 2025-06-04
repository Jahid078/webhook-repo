from flask import Flask, request, jsonify, render_template
from db import collection
from utils import format_log
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    """
    Render the home page.
    """
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Endpoint to receive GitHub webhook events.
    Handles 'push', 'pull_request', and 'merge' events.
    Stores formatted event data to MongoDB.
    """
    data = request.json
    event_type = request.headers.get("X-GitHub-Event")
    try:
        # Handle push event
        if event_type == "push":
            author = data["pusher"]["name"]
            to_branch = data["ref"].split("/")[-1]
            timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
            document = {
                "author": author,
                "action": "push",
                "from_branch": None,
                "to_branch": to_branch,
                "timestamp": timestamp
            }

        # Handle pull request opened event
        elif event_type == "pull_request" and data["action"] == "opened":
            author = data["pull_request"]["user"]["login"]
            from_branch = data["pull_request"]["head"]["ref"]
            to_branch = data["pull_request"]["base"]["ref"]
            timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
            document = {
                "author": author,
                "action": "pull_request",
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }

        # Handle merge event
        elif event_type == "pull_request" and data["action"] == "closed" and data["pull_request"]["merged"]:
            author = data["pull_request"]["user"]["login"]
            from_branch = data["pull_request"]["head"]["ref"]
            to_branch = data["pull_request"]["base"]["ref"]
            timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
            document = {
                "author": author,
                "action": "merge",
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }

        else:
            return "Event not handled", 200

        # Save event data to MongoDB
        collection.insert_one(document)
        return "Webhook received", 200

    except Exception as error:
        print("Error occurred:", str(error))
        return "Internal Server Error", 500

@app.route("/logs", methods=["GET"])
def get_logs():
    """
    Fetch recent logs from MongoDB.
    Returns formatted event messages.
    """
    logs = collection.find().sort("_id", -1).limit(10)
    response = [format_log(entry) for entry in logs]
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)