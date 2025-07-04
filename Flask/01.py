


from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime, timezone
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# ✅ MongoDB Connection
MONGODB_URI = "mongodb+srv://sonugupta05001:A1RkGpzKbVSwvEFe@sonu.2qsfb.mongodb.net/gharDekho?retryWrites=true&w=majority&appName=sonu"
try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ Connected to MongoDB successfully.")
except Exception as e:
    print(" MongoDB connection error:", e)

db = client.gharDekho
events_collection = db.events

@app.route('/webhook', methods=['POST'])
def github_webhook():
    # Add CORS headers manually (though Flask-CORS should handle this)
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    payload = request.json
    event = request.headers.get('X-GitHub-Event', 'ping')

    print(f"\n=== GitHub Event Received: {event} ===")
    print(f"Payload received: {payload}")

    timestamp = datetime.now(timezone.utc).strftime("%d %B %Y - %I:%M %p UTC")
    event_data = None

    if event == "ping":
        print("Ping event received, webhook setup successful.")

    elif event == "push":
        author = payload.get("pusher", {}).get("name", "Unknown")
        to_branch = payload.get("ref", "").split("/")[-1]
        request_id = payload.get("after", "N/A")

        print(f'{author} pushed to "{to_branch}" on {timestamp}')

        event_data = {
            "request_id": request_id,
            "author": author,
            "action": "PUSH",
            "from_branch": "",
            "to_branch": to_branch,
            "timestamp": timestamp
        }

    elif event == "pull_request":
        action = payload.get("action")
        author = payload["pull_request"]["user"]["login"]
        from_branch = payload["pull_request"]["head"]["ref"]
        to_branch = payload["pull_request"]["base"]["ref"]
        request_id = str(payload["pull_request"]["id"])

        if action == "opened":
            print(f'{author} submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}')
            event_data = {
                "request_id": request_id,
                "author": author,
                "action": "PULL_REQUEST",
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }

        elif action == "closed" and payload["pull_request"].get("merged", False):
            print(f'{author} merged branch "{from_branch}" to "{to_branch}" on {timestamp}')
            event_data = {
                "request_id": request_id,
                "author": author,
                "action": "MERGE",
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }

    else:
        print("⚠ Unhandled event type:", event)

    if event_data:
        try:
            result = events_collection.insert_one(event_data)
            print(f"✅ Event saved to MongoDB with ID: {result.inserted_id}")
        except Exception as e:
            print(f"❌ Error saving to MongoDB: {e}")

    response = jsonify("Event Received")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

@app.route('/events', methods=['GET'])
def get_events():
    try:
        events = list(events_collection.find().sort("_id", -1))
        for event in events:
            event["_id"] = str(event["_id"])
        response = jsonify(events)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print(f"❌ Error fetching events from MongoDB: {e}")
        response = jsonify({"error": "Failed to fetch events"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)