from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Initialize the Flask application
# Basically starting the engine of the project.
app = Flask(__name__)

# A secret key is needed for session management to keep things secure.
# Using os.urandom so it's actually random (prof said not to use "password123").
app.secret_key = os.urandom(24)

# Load up the environment variables from the .env file.
# Keeps my API key hidden so I don't accidentally push it to GitHub and get hacked.
load_dotenv()

# --- Load System Instructions ---
# Need to build an absolute path because relative paths always mess up on my laptop.
try:
    # Get the directory where this script is located.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Join it with the filename to get the full path.
    instructions_path = os.path.join(base_dir, 'instructions.txt')
    
    # Reading the file with UTF-8 so emojis don't break the code.
    with open(instructions_path, 'r', encoding='utf-8') as f:
        system_instruction = f.read()
except FileNotFoundError:
    # If the file is missing, I'll just use a generic prompt so the app doesn't crash.
    print("Yo, instructions.txt is missing! Using a generic prompt for now.")
    system_instruction = "You are a helpful assistant."

# Now, let's get the Gemini API ready.
try:
    # Configuring the AI with the key. Fingers crossed the key in .env is correct.
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Passing the system instructions when initializing.
    # IMPORTANT: Switched to 'gemini-2.5-flash' because '1.5' gave me a 404 error.
    # This model seems to actually work with my account.
    model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=system_instruction)
    print("Success: Connected to Gemini 2.5!")

except Exception as e:
    # If the API fails, print the error so I can google it later.
    print(f"Bummer. Couldn't configure the Gemini API: {e}")
    # Set model to None so I can handle it gracefully in the chat route.
    model = None

# --- Application Routes ---

@app.route('/')
def index():
    """
    This route renders the main chat page.
    I'm clearing the session every time so I don't see old chats when I refresh.
    """
    session.clear()
    # Starting with an empty history list.
    session['history'] = []
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    This handles the chat logic.
    User sends text -> We ask Gemini -> We send answer back.
    """
    # First, a sanity check to make sure the model actually loaded.
    if not model:
        return jsonify({"error": "Server Error: The Gemini API isn't configured. Check the console logs."}), 500

    try:
        # Get the user's message and trim extra spaces.
        user_input = request.json.get('message', '').strip()
        
        # Validation: Don't let empty messages through.
        if not user_input:
            return jsonify({"error": "Bro, you sent an empty message."}), 400

        # Making sure the history list exists in the session.
        if 'history' not in session:
            session['history'] = []

        # Add the user's message to history.
        session['history'].append({"role": "user", "parts": [user_input]})

        # Safety hack: Keep history short (last 6 messages) so I don't hit the "Quota Exceeded" error again.
        if len(session['history']) > 12:
             session['history'] = session['history'][-12:]

        # Generating the response.
        response = model.generate_content(
            contents=session['history'],
            generation_config={
                "max_output_tokens": 400, # Keeping it short-ish.
                "temperature": 0.6 # 0.6 is a good balance of creative and logical.
            }
        )

        bot_response = response.text

        # Add the AI's response to history so it remembers the context.
        session['history'].append({"role": "model", "parts": [bot_response]})
        # Mark session as modified so Flask saves the updates.
        session.modified = True

        return jsonify({"response": bot_response})

    except Exception as e:
        # If it crashes, log the error and tell the user something went wrong.
        # Also printing 'e' to console so I can debug it.
        print(f"Crash in /chat: {e}")
        return jsonify({"error": "Sorry, something crashed on the server. Check the terminal."}), 500

@app.route('/speak')
def speak_page():
    """This just renders the speak page."""
    return render_template('speak.html')

@app.route('/api/config')
def api_config():
    """
    Sends the API key to the frontend.
    Needed this for the client-side voice stuff to work.
    """
    return jsonify({
        'gemini_api_key': os.getenv("GEMINI_API_KEY"),
        'system_instruction': system_instruction
    })

# --- Let's get this thing running ---
if __name__ == '__main__':
    # Running in debug mode.
    # Using port 5002 because 5000 is always stuck on my machine.
    app.run(debug=True, port=5002)
