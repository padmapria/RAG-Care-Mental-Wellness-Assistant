# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install any needed packages specified in app_requirements.txt
COPY app_requirements.txt /app/

# Set the working directory to /app
WORKDIR /app
	
# Install any needed packages specified in app_requirements.txt
RUN pip install --no-cache-dir -r app_requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the create_index_elasticsearch.py script first to create index and then start the Flask application
CMD sh -c "python create_index_elasticsearch.py && python app.py --server.port=5000 --server.address=0.0.0.0"