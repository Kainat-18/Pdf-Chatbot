import os
from flask import Flask, request, jsonify
import PyPDF2
import openai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get OpenAI API key from the .env file
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize the Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function: Check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function: Extract text from PDF
def extract_text_from_pdf(filepath):
    with open(filepath, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

# In-memory knowledge base
knowledge_base = {}

# Home Endpoint
@app.route('/')
def home():
    return "Welcome to Chatbot PDF! Upload a PDF to start interacting with it."

# Route 1: Upload PDF and extract text
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        text = extract_text_from_pdf(filepath)
        knowledge_base[filename] = text
        return jsonify({'message': 'File uploaded and processed successfully', 'filename': filename}), 200
    return jsonify({'error': 'Invalid file format'}), 400

# Route 2: Chatbot API for answering questions
@app.route('/chat', methods=['POST'])
def chatbot():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Combine all extracted text into a single context
    context = " ".join(knowledge_base.values())
    
    if not context:
        return jsonify({'error': 'Knowledge base is empty. Please upload a PDF first.'}), 400

    # Use OpenAI's ChatCompletion API for NLP-based response
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use the latest GPT model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
            ]
        )
        answer = response['choices'][0]['message']['content'].strip()

        # Post-process the answer to remove unnecessary newlines or extra spaces
        cleaned_answer = " ".join(answer.splitlines()).strip()
        cleaned_answer = cleaned_answer.replace("\n", "").replace("  ", " ")

        # Format the output
        formatted_answer = {
            "answer": cleaned_answer
        }
        return jsonify(formatted_answer), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
