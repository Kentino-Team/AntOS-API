FROM python:3.8

RUN python -m pip install --upgrade pip

RUN pip3 install pipenv

COPY ./ /app

WORKDIR /app

RUN pipenv install
RUN pipenv install flask uwsgi

EXPOSE 80/tcp

CMD pipenv run uwsgi --http :80 --processes 4 --wsgi-file app.wsgi