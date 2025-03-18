# Use official Python image
FROM python:3.12

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port for Django
EXPOSE 8000

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8100"]
