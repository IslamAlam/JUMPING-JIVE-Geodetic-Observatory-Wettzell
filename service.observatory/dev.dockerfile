# # https://hub.docker.com/r/library/python/tags/
# FROM python:3-onbuild  
# 
# # Coping source in current directory into the image
# # python:3-onbuild expects the source in /usr/src/app
# COPY ./usr/src/app
# 
# # Commands in a list
# CMD ["python", "api.py"]

# FROM python:3.5-jessie
# 
# # Upgrade pip and install YAPF
# RUN pip install --upgrade pip && \
#     pip install yapf
# 
# # Add the libraries
# COPY ./libraries/python /root/.local/lib/python3.5/site-packages/
# 
# # Install requirements
# RUN mkdir -p /usr/src/app
# WORKDIR /usr/src/app
# COPY ./service.observatory/requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# 
# # Copy the application files
# COPY ./service.observatory .
# 
# # Commands in a list
# CMD ["python", "api.py"]


#RUN chmod +x ./run.sh

#CMD ./run.sh

# https://hub.docker.com/r/library/python/tags/
# FROM python:3-onbuild  
# 
# # Coping source in current directory into the image
# # python:3-onbuild expects the source in /usr/src/app
# COPY . /usr/src/app
# EXPOSE 5000
# 
# # Commands in a list
# CMD ["python", "api.py"]

FROM tiangolo/uwsgi-nginx-flask:python3.7

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
ENV STATIC_INDEX 1
# ENV STATIC_INDEX 0


COPY ./service.observatory/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
