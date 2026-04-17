from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

# ==========================================
# MONGODB SETUP
# ==========================================
MONGO_URI = "mongodb+srv://my_app_user:gmbng_QtMCXCnq999@cluster0.2jeidzd.mongodb.net/?appName=Cluster0"

# Initialize variables to None first
client = None
collection = None

try:
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    
    db = client['college_database']
    collection = db['student_submissions']
except Exception as e:
    print(f"MongoDB Connection Error: {e}")
    # The app will still run, but client and collection remain None

# ... (rest of the app.py code stays the same)

# ==========================================
# TASK 1: /api Route
# ==========================================
@app.route('/api', methods=['GET'])
def get_api_data():
    try:
        # Read data from the backend file
        with open('data.json', 'r') as file:
            data = json.load(file)
        
        # Send it as a JSON response
        return jsonify(data), 200
        
    except FileNotFoundError:
        return jsonify({"error": "Backend file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# TASK 2: Form and MongoDB Submission
# ==========================================
@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        try:
            # Simulate an error condition (e.g., if database client isn't connected)
            if not client:
                raise Exception("Database not connected.")
                
            # Insert data into MongoDB Atlas
            document = {
                "name": username,
                "email": email
            }
            collection.insert_one(document)
            
            # On successful submission, redirect to success page
            return redirect(url_for('success'))
            
        except Exception as e:
            # If there's an error, capture it and display on the same page
            error_message = f"Failed to submit data: {str(e)}"
            return render_template('index.html', error=error_message)

    # Render form for GET requests or if there's an error
    return render_template('index.html', error=error_message)


@app.route('/success')
def success():
    # Target success message exactly as requested
    return "<h2>Data submitted successfully</h2><br><a href='/'>Go back</a>"


if __name__ == '__main__':
    app.run(debug=True)