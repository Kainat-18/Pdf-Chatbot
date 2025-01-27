# PDF Chatbot Application

A Python-based application that uses AI/ML techniques to create a chatbot capable of answering user questions based on information extracted from PDF documents. This project leverages Flask for the backend, Streamlit for the frontend, and OpenAI's GPT-4 model for Natural Language Processing (NLP).

---

## Features and Functionalities

- **PDF Upload and Text Extraction:** Users can upload PDF files, and the application extracts and processes the text into a knowledge base.
- **AI-Powered Chatbot:** OpenAI's GPT-4 is used to answer questions based on the extracted content from the uploaded PDFs.
- **User-Friendly Interface:** A simple and accessible interface built using Streamlit for seamless interaction.
- **API Endpoints:** Flask APIs for uploading PDFs and generating responses to user queries.
- **Dockerized Deployment:** Simplified deployment process using Docker.

---

## Setup Instructions

### Prerequisites
1. Python 3.11 or higher installed.
2. Docker installed on your system (optional for containerized deployment).
3. OpenAI API key (set up in a `.env` file).

### Installation Steps

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

#### 2. Set Up Environment Variables
- Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run the Flask Backend
```bash
python app_with_flask.py
```

#### 5. Run the Streamlit Frontend
```bash
streamlit run app_with_streamlit.py
```


## API Documentation

### 1. `/upload` (POST)
Uploads a PDF document and processes it into the knowledge base.

#### Request:
- **File:** The PDF file to be uploaded.

#### Response:
```json
{
  "message": "File uploaded and processed successfully",
  "filename": "example.pdf"
}
```

---

### 2. `/chat` (POST)
Submits a user query and retrieves an AI-generated answer based on the processed PDF content.

#### Request:
```json
{
  "question": "----------------t?"
}
```

#### Response:
```json
{
  "answer": "-------------"
}
```
# Python Chatbot with Streamlit UI

## Description
A simple chatbot application built using Python and Streamlit, containerized with Docker for seamless deployment.

## How to Run Using Docker

### Step 1: Build the Docker Image
Run the following command to build the Docker image:
```bash
docker build -t python-chatbot-app .
```

### Step 2: Run the Docker Container
Use the following command to run the container and expose the Streamlit app on port 8501:

```bash
docker run -p 8501:8501 python-chatbot-app
```

### Step 3: Access the Application
Open your web browser and navigate to: (http://localhost:8501)[http://localhost:8501]

## Notes
Ensure Docker is installed and running on your machine before executing these commands.
Modify the Dockerfile or requirements.txt as needed for additional dependencies or customizations.


