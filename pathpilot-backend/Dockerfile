FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
# install dependencies
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# port 5000 for flask
EXPOSE 5000
RUN adduser --disabled-password --gecos "" appuser
USER appuser
# command to run, 2 workers since each request blocks on two external apis
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "2", "--timeout", "60", "app:app"]