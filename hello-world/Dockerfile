FROM python:3-alpine
WORKDIR /service
COPY requirements.txt .
RUN /usr/local/bin/pip3 install -r requirements.txt
COPY app.py .
# pass --build-arg PORT=<no> while building
ARG PORT
ENV PORT=${PORT}
RUN echo "port : $PORT"
EXPOSE ${PORT}
CMD [ "/usr/local/bin/python3", "app.py" ]
