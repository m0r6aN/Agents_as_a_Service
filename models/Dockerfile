# Use a base image with CUDA support
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    wget \
    git \
    libgl1-mesa-glx

# Add deadsnakes PPA for Python 3.12
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.12 python3.12-distutils python3.12-dev python3-pip

# Set Python 3.12 as the default version of Python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# Install pip for Python 3.12
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.12 get-pip.py

# Set working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the API port
EXPOSE 9000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "sql-nlp:app", "--host", "0.0.0.0", "--port", "9000"]


# Build the Docker image - Use Cached Docker Layers
# docker build -t sql-nlp --cache-from sql-nlp .

# Run the Docker container with GPU support
# docker run --gpus all -d -p 9000:9000 sql-nlp

# Verify GPU Usage: You can verify that PyTorch is using the GPU by running this command inside your FastAPI app or container:
# import torch
# print(torch.cuda.is_available())  # Should print True if GPU is available

# You can verify that the correct Python version is running inside your Docker container by executing the following:
# docker exec -it <container_id> python3 --version
