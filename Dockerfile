FROM python:3.9
WORKDIR /app
RUN apt-get update && apt-get install -y libgl1 libzbar0
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 7860
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]