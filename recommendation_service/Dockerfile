FROM python:3.11

#ARG DB_CONNECTION
#ARG MODE

#ENV SQLALCHEMY_DATABASE_URI=${DB_CONNECTION}
#ENV MODE=${MODE}

COPY requirements.txt .
RUN pip install -r requirements.txt

#COPY ./scripts /app
COPY . /app
#WORKDIR /app

#CMD nohup python main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
#CMD python main.py