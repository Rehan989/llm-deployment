FROM tiangolo/tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app 

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./app
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"] 
# Replace 'main:app' if different in your FastAPI setup
