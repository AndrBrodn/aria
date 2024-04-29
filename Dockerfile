FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

# Install necessary packages
RUN apt update && apt upgrade -y \
    && apt install -y git python3-pip python3.10-venv

# Clone the repository
RUN git clone https://github.com/lef-fan/aria.git /aria
WORKDIR /aria

# Setup Python virtual environment
RUN python3 -m venv venv
ENV VIRTUAL_ENV=venv
ENV PATH="/aria/venv/bin:$PATH"

# Install Python dependencies
RUN pip install wheel numpy torch onnxruntime \
    git+https://github.com/huggingface/transformers \
    && CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python \
    TTS accelerate flash-attn deepspeed

# Assuming the application uses Flask and the entry point is app.py
COPY ./app.py /aria  # Ensure you have this file in your context directory
EXPOSE 5000
CMD ["python", "main.py"]
