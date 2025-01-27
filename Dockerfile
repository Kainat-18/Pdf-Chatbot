# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose a specific port (change the port number as needed)
EXPOSE 8501

# Set the command to run the application
# Replace 'app.py' with your application's entry point
CMD ["streamlit", "run", "app_with_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
