
# BU Helpdesk Bot

A sophisticated, conversational AI assistant for Barkatullah University, designed to provide instant and accurate information to students, applicants, and staff. This chatbot features both a text-based interface and a hands-free, voice-activated mode.

---

## 📷 Preview

<div align="center">
  <img src="https://github.com/user-attachments/assets/cecdfeff-62c9-4a7f-b0c5-debf97590943" alt="BU Helpdesk Bot Preview" width="600" />
</div>

<div align="center" style="margin-top:20px;">
  <a href="https://sagarryadvav.pythonanywhere.com/" target="_blank" style="text-decoration:none;">
    <button style="background-color:#4CAF50;color:white;padding:15px 30px;font-size:18px;border:none;border-radius:8px;cursor:pointer;">
      Try Here / Visit Website
    </button>
  </a>
</div>

## ✨ Features

* **Dual Interface**: Users can interact through a traditional text chat or a modern, voice-controlled interface.
* **Powered by Google Gemini**: Leverages the Gemini 1.5 Flash model for natural, intelligent, and context-aware conversations.
* **Comprehensive Knowledge Base**: Trained with a detailed set of instructions to provide accurate information on courses, admissions, exams, events, and campus infrastructure at Barkatullah University.
* **Session Management**: Maintains a continuous conversation history within a session for contextual responses.
* **Flask Backend**: Built with a lightweight and scalable Python Flask server to handle chat logic and API requests.

## 🛠️ Technologies Used

* **Backend**: Python, Flask
* **AI Model**: Google Gemini 1.5 Flash
* **Frontend**: HTML, CSS, JavaScript
* **Web Speech API**: For voice recognition and speech synthesis in the voice interface.

## 🚀 Getting Started

Follow these steps to get the BU Helpdesk Bot running on your local machine.

### 1. Prerequisites

* Python 3.7+
* A Google Gemini API Key. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Clone the Repository

```bash
git clone [https://github.com/your-username/bu-helpdesk-bot.git](https://github.com/your-username/bu-helpdesk-bot.git)
cd bu-helpdesk-bot
```
### 3. Set Up Environment & Install Dependencies

```bash
# Create and activate a virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```
### 4. Configure API Key (❗Crucial Step)
Create a new file named .env in the project's root directory. Inside this file, add your Gemini API key.


```bash

GEMINI_API_KEY=REPLACE_WITH_YOUR_GEMINI_API_KEY
```

Important: You must replace REPLACE_WITH_YOUR_GEMINI_API_KEY with your actual key. The application will not work without it.

### 5. Run the Application
Start the local server with the following command:
```bash

python app.py
```
Text Chat: Access at http://127.0.0.1:5000

Voice Chat: Access at http://127.0.0.1:5000/speak



