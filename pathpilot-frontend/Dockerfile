FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
# install dependencies
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# port 5000 inside the container, docker-compose maps it to 5003
EXPOSE 5000
RUN adduser --disabled-password --gecos "" appuser
USER appuser
# command to run, 1 worker keeps the in-memory rate limiter counting correctly,
# threads give concurrency. more workers would multiply the roadmap limit
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "1", "--threads", "8", "--timeout", "60", "app:app"]