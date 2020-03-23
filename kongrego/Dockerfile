FROM alpine:3.7

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY . /app
WORKDIR /app
RUN chmod go+w /etc/passwd
ENTRYPOINT [ "python3" ]
CMD [ "run.py" ]
