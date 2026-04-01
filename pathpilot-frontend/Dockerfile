FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
# install dependencies
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# port 5003 for jinja2
EXPOSE 5003
# command to run
CMD ["python", "app.py"]