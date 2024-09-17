# Use the bitsandbytes image as the base
FROM dustynv/bitsandbytes:r35.3.1

# Install PEFT and Flask using pip
RUN pip install peft flask

# Set the working directory in the container
WORKDIR /

# Copy your application code to the container
COPY image2text_app.py /

# Specify the command to run your application
CMD ["python3", "/image2text_app.py"]
