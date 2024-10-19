FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements_versions.txt /app
RUN pip3 install --no-cache-dir -r requirements_versions.txt

# Copy the rest of the application code
COPY . /app

# Ensure permissions for writing output files
RUN chmod -R 777 /app

# Expose the port for Gradio
EXPOSE 7860

# Command to run the application
CMD ["python", "app.py"]
