# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app

COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
COPY . .
# Make port 8501 available to the world outside this container
EXPOSE 8501


# Run streamlit app when the container launches
CMD ["streamlit", "run", "realtimeaudiorecorder.py"]






