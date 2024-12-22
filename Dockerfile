# Use the official Python base image
FROM python:3.11-slim

# Install Java JDK (needed for H2O)
RUN apt-get update && \
    apt-get install -y openjdk-11-jre

# Set the environment variable for Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any necessary dependencies
RUN pip install -r requirements.txt

# Expose the required port
EXPOSE 5000

# Run the app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
