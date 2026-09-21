From python:3.12-slim

WORKDIR /app

# Don't create Python .pyc bytecode files.
ENV PYTHONDONTWRITEBYTECODE=
# Output logs immediately.
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

# This application is expected to listen on port 8000
EXPOSE 8000

# 0.0.0.0:8000 ---> Listen on all network interfaces inside the container. Otherwise it will only listen to 127.0.0.1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]