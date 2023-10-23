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
COPY kaggle.json $HOME/.kaggle/kaggle.json
RUN chown user:user $HOME/.kaggle/kaggle.json
RUN chmod 600 $HOME/.kaggle/kaggle.json 

# Switch to new user
USER user

# Copy the .env file
COPY .env .env

# Set the working directory for the user
WORKDIR $HOME/app

# Copy the current directory contents into the container at /app
COPY --chown=user . $HOME/app

# Copy the poetry files
COPY pyproject.toml poetry.lock /app/

# Upgrade pip and install poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Set environment variable to create a virtual environment within the project directory
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Install project dependencies
RUN poetry lock
RUN poetry install

# Copy the rest of the application code
COPY . .

# Define the command to run the app
CMD ["poetry", "run", "chainlit", "run", "src/app/app.py", "--host=0.0.0.0", "--port=80", "--headless"]
#ENTRYPOINT ["chainlit", "run", "app.py", ]