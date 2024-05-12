# This sets up the container with Python 3.12.2 installed.
FROM python:3.12.2-slim

# Set the working directory in the container to /app
WORKDIR /app

# Install system-level dependencies required for matplotlib and Prophet
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    python3-dev \
    libgfortran5 \
    libatlas-base-dev \
    libpangocairo-1.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# First, copy only the requirements.txt file to leverage Docker cache
# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files to /app
COPY . /app

# Make port 8501 available outside this container
EXPOSE 8501

# This sets the default command for the container to run the app with Streamlit.
ENTRYPOINT ["streamlit", "run"]

# This command tells Streamlit to run your app.py script when the container starts.
CMD ["app.py"]

