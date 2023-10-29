# Use the official Python image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Create a new user 
RUN useradd -m -u 1000 user

# Set environment variables for the new user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Copy and set the kaggle.json file
COPY --chown=user:user --chmod=600 kaggle.json $HOME/.kaggle/kaggle.json

# Switch to new user
USER user

# Copy the .env file
COPY .env .env

# Set the working directory for the user
WORKDIR $HOME/app

# Copy the current directory contents into the container at /app
COPY --chown=user . $HOME/app

# Copy the requirements file
COPY --chown=user:user requirements.txt $HOME/app/

# Upgrade pip
RUN pip install --upgrade pip

# Install project dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY --chown=user:user .env kaggle.json README.md chainlit.md .chainlit/ /src/app/ $HOME/app/

# Define the command to run the app
CMD ["chainlit", "run", "src/app/app.py", "--host=0.0.0.0", "--port=80", "--headless"]