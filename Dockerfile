FROM joyzoursky/python-chromedriver

WORKDIR /app
COPY ./ ./
RUN chmod -R 777 /app
RUN pip install -r ./requirements.txt 

EXPOSE 5000
CMD ["python3", "./run.py"]