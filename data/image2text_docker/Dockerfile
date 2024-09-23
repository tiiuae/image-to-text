# Use the pytorch image as the base
FROM dustynv/l4t-pytorch:r36.2.0

LABEL org.opencontainers.image.source=https://github.com/tiiuae/image-to-text

# Install dependencies using pip
RUN pip3 install timm PySide6 accelerate flash_attn transformers python-multipart uvicorn fastapi

# Set the working directory in the container
WORKDIR /

# Copy your application code to the container
COPY image2text_app.py /

COPY test.jpg /

# Specify the command to run your application
CMD ["python3", "/image2text_app.py"]
