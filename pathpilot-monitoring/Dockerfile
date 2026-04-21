FROM python:3.11-slim
WORKDIR /dashboard
COPY requirements.txt .
# install dependencies
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# port 8050 for dashboard
EXPOSE 8050
RUN adduser --disabled-password --gecos "" appuser
USER appuser
# command to run
CMD ["python", "dashboard.py"]