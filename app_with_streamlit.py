import os
import PyPDF2
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get OpenAI API key from the .env file
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)

# Set up Streamlit page configuration
st.set_page_config(page_title="PDF Chatbot", layout="wide")

# Helper function: Check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

# Helper function: Extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# In-memory knowledge base
knowledge_base = {}

# Streamlit UI
st.title("PDF Chatbot")

# File upload section
st.sidebar.header("Upload a PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=['pdf'])

if uploaded_file is not None:
    if allowed_file(uploaded_file.name):
        # Extract text from the uploaded PDF
        pdf_text = extract_text_from_pdf(uploaded_file)
        knowledge_base[uploaded_file.name] = pdf_text

        st.sidebar.success(f"Uploaded and processed: {uploaded_file.name}")

        # Display the text content for verification (optional)
        with st.expander("Extracted PDF Text"):
            st.write(pdf_text)
    else:
        st.sidebar.error("Invalid file format. Please upload a PDF.")

# Question and Answer Section
st.header("Chat with the PDF")
if knowledge_base:
    context = " ".join(knowledge_base.values())

    # Input for the user's question
    question = st.text_input("Enter your question:")

    # Button to trigger the answer generation
    if st.button("Get Answer"):
        if question:
            try:
                # Use OpenAI's ChatCompletion API for answering questions
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                        {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
                    ],
                    model="gpt-4o",
                )

                answer = response.choices[0].message.content

                # Display the answer
                st.subheader("Answer:")
                st.write(answer)

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please enter a question to get an answer.")
else:
    st.info("Please upload a PDF to begin.")
