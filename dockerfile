FROM python:3.12.3 AS base
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "pr_reviewer/server.py"]
EXPOSE 8080