from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import pytz

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.github_events
collection = db.events

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        payload = request.json
        
        # Extract common fields
        author = payload.get("sender", {}).get("login", "unknown")
        timestamp = datetime.utcnow().replace(tzinfo=pytz.UTC)
        
        # Determine the event type from GitHub headers
        event_type = request.headers.get('X-GitHub-Event')
        
        event_data = {
            "author": author,
            "timestamp": timestamp
        }
        
        if event_type == "push":
            # For push events
            ref = payload.get("ref", "").split('/')[-1]  # Gets branch name from refs/heads/branch
            event_data.update({
                "action": "push",
                "to_branch": ref
            })
            
        elif event_type == "pull_request":
            # For pull request events
            pr = payload.get("pull_request", {})
            action = payload.get("action")
            
            if action in ["opened", "reopened"]:
                event_data.update({
                    "action": "pull_request",
                    "from_branch": pr.get("head", {}).get("ref"),
                    "to_branch": pr.get("base", {}).get("ref")
                })
            elif action == "closed" and pr.get("merged"):
                event_data.update({
                    "action": "merge",
                    "from_branch": pr.get("head", {}).get("ref"),
                    "to_branch": pr.get("base", {}).get("ref")
                })
        
        # Store in MongoDB
        collection.insert_one(event_data)
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/events", methods=["GET"])
def get_events():
    events = list(collection.find({}, {"_id": 0}).sort("timestamp", -1))
    # Format timestamps
    for event in events:
        event['timestamp'] = event['timestamp'].strftime("%d %B %Y - %I:%M %p UTC")
    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True)