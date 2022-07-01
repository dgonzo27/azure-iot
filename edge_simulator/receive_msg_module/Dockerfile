# pull official base image
FROM python:3.9-slim-buster

# set working directory
WORKDIR /usr/src/app

# install dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy src code
COPY . .

# run main.py
CMD [ "python3", "-u", "./src/main.py" ]
