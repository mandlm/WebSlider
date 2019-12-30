FROM python:3
ADD app /app
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --requirement /app/requirements.txt
WORKDIR /app

EXPOSE 5000/TCP

CMD [ "python3", "server.py" ]
