from flask_socketio import SocketIO
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from flask_cors import CORS
import pytz
import logging
import sys
import json

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('webhook.log')
    ]
)

# Custom JSON encoder to handle ObjectId
class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.strftime("%d %B %Y - %I:%M %p UTC")
        return super().default(o)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app)
app.json_encoder = MongoJSONEncoder

# MongoDB connection
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client.github_events
    collection = db.events
    logging.info("Successfully connected to MongoDB")
except Exception as e:
    logging.error(f"Failed to connect to MongoDB: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Log incoming request details
        logging.info("Received webhook request")
        logging.debug(f"Headers: {dict(request.headers)}")
        
        # Parse JSON payload
        payload = request.json
        logging.info(f"Parsed payload: {payload}")
        
        # Extract common fields
        author = payload.get("sender", {}).get("login", "unknown")
        timestamp = datetime.utcnow().replace(tzinfo=pytz.UTC)
        
        # Determine the event type
        event_type = request.headers.get('X-GitHub-Event', 'push')
        logging.info(f"Event type: {event_type}")
        
        event_data = {
            "author": author,
            "timestamp": timestamp
        }
        
        if event_type == "push":
            ref = payload.get("ref", "")
            branch = ref.split('/')[-1] if ref else "unknown"
            event_data.update({
                "action": "push",
                "to_branch": branch
            })
            logging.info(f"Processed push event to branch: {branch}")
            
        elif event_type == "pull_request":
            pr = payload.get("pull_request", {})
            action = payload.get("action")
            
            if action in ["opened", "reopened"]:
                event_data.update({
                    "action": "pull_request",
                    "from_branch": pr.get("head", {}).get("ref"),
                    "to_branch": pr.get("base", {}).get("ref")
                })
                logging.info(f"Processed pull request event: {action}")
            elif action == "closed" and pr.get("merged"):
                event_data.update({
                    "action": "merge",
                    "from_branch": pr.get("head", {}).get("ref"),
                    "to_branch": pr.get("base", {}).get("ref")
                })
                logging.info("Processed merge event")
        
        # Store in MongoDB
        result = collection.insert_one(event_data)
        logging.info(f"Stored event in MongoDB with ID: {str(result.inserted_id)}")
        
        # Convert ObjectId to string for response
        event_data['_id'] = str(result.inserted_id)
        return jsonify({"status": "success", "event": event_data}), 200
        
    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/events", methods=["GET"])
def get_events():
    try:
        # Fetch events and convert ObjectId to string
        events = list(collection.find().sort("timestamp", -1))
        for event in events:
            event["_id"] = str(event["_id"])  # Convert ObjectId to string
        
        return jsonify(events)
    except Exception as e:
        logging.error(f"Error retrieving events: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)