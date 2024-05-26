FROM python:3.11

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /scheduler

COPY start.sh /scheduler/start.sh
RUN chmod +x /scheduler/start.sh

CMD ["/scheduler/start.sh"]
