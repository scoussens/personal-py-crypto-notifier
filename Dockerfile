FROM python:3.9-slim

RUN pip install --no-cache-dir pipenv

# Creating working directory
WORKDIR usr/src/app
COPY . .

RUN pipenv install

CMD ["pipenv", "run", "python", "main.py"]