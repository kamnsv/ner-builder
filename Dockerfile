FROM python:3.11-slim

# Обновляем пакеты и устанавливаем необходимые зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        git \
        cmake \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем PyTorch с CPU-версией и остальные зависимости из requirements.txt
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --timeout 180 && \
    pip install --no-cache-dir -r requirements.txt --timeout 180
