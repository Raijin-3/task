**Voice to Voice Q&A System**
The Voice to Voice Q&A System is a web-based application that allows users to upload a PDF file and ask questions about its content using voice input. The system processes the document and provides answers based on the extracted text.

**Features**
📂 PDF Upload: Users can upload a PDF document for processing.
🎤 Voice Input: Supports voice-based question input.
🤖 AI-Powered Responses: The system extracts relevant answers from the uploaded document.
🔊 Voice Output : Can provide voice-based answers.

**Folder Structure**
├── app/                   # Main application logic
├── templates/app/         # HTML templates for the UI
├── voicebot/              # Voice processing module
├── .gitignore             # Git ignore file
├── manage.py              # Django project management file

**Installation & Setup**
Python 3.10
Django 4.2
Required libraries from requirements.txt

_Steps to Run_
1. Clone the repository
  _git clone <repository-url>_
2. Install the requirements
  _pip install -r requirements.txt_
3. Run the server
  _python manage.py runserver_
4. Open the application
  Visit http://127.0.0.1:8000/ in your browser.

**Usage**
  Upload a PDF using the provided file upload section.
  Ask a question by using voice input.
  Receive an AI-generated answer extracted from the document.
  Use voice recognition for a seamless experience.
**Technologies Used**
  Django – Backend framework
  JavaScript & HTML/CSS – Frontend
  Speech Recognition API – Voice input processing
  NLP & AI Models – For extracting answers from text
