### Steps to run backend i.e django-rest-framework server - 
1. Make sure you have GDAL in your system installed.  \
    Download and setup the GDAL executable file from [OSGeo4W network installer](https://trac.osgeo.org/osgeo4w/)
2. Now, download the docker image for postgreSQL and POSTGIS extension for database. \
    Run the cmd  - 
    *```docker run --name=postgis -d -p 5432:5432 -e POSTGRES_DB=pothole_patrol_db -e POSTGRES_USER=postgis -e POSTGRES_PASSWORD=postgis postgis/postgis```* \
    Above command is to executed only for first time to create the container and from next time you just need to start the container. \
    Above command will also come in handy when you update the schema of DB like adding more tables or fields. So, for that first remove the container and run the above cmd. \
    **Imp cmds** : \
    *```docker start postgis``` \
    ```docker stop postgis``` \
    ```docker remove postgis``` \
    ```docker ps [-a]```*
3. Next, git clone this repo change directory to *```BE-Project-Pothole-Detection-backend\pothole_patrol_backend\```*
4. Make virtual environment for project using *```virtualenv venv```* \
    Activate virtual env using cmd - *```venv\scripts\activate```* \
    For deactivating virtual env when you exit project at the end, run the cmd - *```deactivate```*
5. Run the cmd - *```pip install -r requirements.txt```* to install the required libraries for project.
6. Now, we need to create tables in DB running in docker. So, make migrations for django models. \
    Run below cmds one after other - \
    *```python manage.py makemigrations``` \
    ```python manage.py migrate```*
8. Finally, run the django server. \
    *```python manage.py runserver 0.0.0.0:8000```*
