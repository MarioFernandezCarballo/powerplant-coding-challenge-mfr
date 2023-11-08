# base image  
FROM python:3.10.11

# set work directory  
RUN mkdir -p /home/app  

# where your code lives  
WORKDIR /home/app

# install dependencies  
RUN pip install --upgrade pip  

# copy whole project to your docker home directory. 
COPY . . 
# run this command to install all dependencies  
RUN pip install -r requirements.txt  
# port where the Django app runs  
EXPOSE 8888
# start server
CMD [ "python", "main.py"]