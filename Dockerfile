# Use the official Python image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Create a new user and switch to this user
RUN useradd -m -u 1000 user
USER user

# Set environment variables for the new user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

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

# Copy the .env file
COPY .env .env

# Copy the rest of the application code
COPY . .

# Extract data for app
RUN poetry run ploomber build

# Expose the port that the app runs on
EXPOSE 8000

# Define the command to run the app
CMD ["poetry", "run", "chainlit", "run", "app.py", "--port", "7860"]