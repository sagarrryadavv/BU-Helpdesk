from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Initialize the Flask application
app = Flask(__name__)
# A secret key is needed for session management to keep things secure
app.secret_key = os.urandom(24)

# Load up the environment variables from the .env file
load_dotenv()

# --- Load System Instructions ---
# build an absolute path to make sure this works everywhere.
try:
    # Get the directory where this script is located.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Join it with the filename to get the full path.
    instructions_path = os.path.join(base_dir, 'instructions.txt')
    # To read the instructions from this full path, making sure to use UTF-8 encoding.
    with open(instructions_path, 'r', encoding='utf-8') as f:
        system_instruction = f.read()
except FileNotFoundError:
    # If the instructions file is missing, bot will just use a default.
    print("Heads up: instructions.txt wasn't found, so I'm using a generic instruction.")
    system_instruction = "You are a helpful assistant."

# Now, let's get the Gemini API ready.
try:
    # Configuring the generative AI model with the API key from our environment variables.
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    # Passing the system instructions when initializing the model is the way to go.
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)
except Exception as e:
    # If something goes wrong with the API configuration, bot will log this.
    print(f"Couldn't configure the Gemini API: {e}")
    # And set the model to None so we know it's not ready.
    model = None

# --- Application Routes ---

@app.route('/')
def index():
    """
    This route renders the main chat page.
    I'm clearing the session to make sure every visit is a fresh conversation.
    """
    session.clear()
    # Starting with an empty history since the model now handles the system prompt directly.
    session['history'] = []
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    This function handles the chat requests, sends them to the Gemini API,
    and then returns the AI's response.
    """
    # First, a quick check to make sure the Gemini model is actually working.
    if not model:
        return jsonify({"error": "The Gemini API isn't configured, or the API key is missing."}), 500

    try:
        # get the user's message from the request and trim any extra whitespace.
        user_input = request.json.get('message', '').strip()
        if not user_input:
            # Can't do much with an empty message.
            return jsonify({"error": "Received an empty message"}), 400

        # Making sure the chat history exists in the session.
        if 'history' not in session:
            session['history'] = []

        # Adding the user's message to our session history.
        session['history'].append({"role": "user", "parts": [user_input]})

        # Now, let's get a response from the Gemini model.
        # The model already has the system instructions from when we initialized it.
        response = model.generate_content(
            contents=session['history'],
            generation_config={
                "max_output_tokens": 200, # Bumping up the token limit for longer answers.
                "temperature": 0.6
            }
        )

        bot_response = response.text

        # add the model's response to our history.
        session['history'].append({"role": "model", "parts": [bot_response]})
        # make sure the session is marked as modified so the changes stick.
        session.modified = True

        return jsonify({"response": bot_response})

    except Exception as e:
        # If any errors pop up, log them for debugging.
        app.logger.error(f"An error occurred in /chat: {e}")
        # Then send back a generic error message to the user.
        return jsonify({"error": "Sorry, an unexpected error occurred. Please try again."}), 500

@app.route('/speak')
def speak_page():
    """This just renders the speak page."""
    return render_template('speak.html')

@app.route('/api/config')
def api_config():
    """This route provides the Gemini API key and system instructions to the frontend."""
    return jsonify({
        'gemini_api_key': os.getenv("GEMINI_API_KEY"),
        'system_instruction': system_instruction
    })

# --- Let's get this thing running ---
if __name__ == '__main__':
    # Running the app in debug mode for development.
    app.run(debug=True)