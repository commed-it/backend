# Usage and Installation
## Settings
Ask for the `.env` file to have all the configuration done in the development stage :grin: .
## Building the database and web images
The first time, you must build the images using
```bash
docker-compose build
```
## Start the application
In order to run the container, you must:
```bash
docker-compose up
```
You can run the container in detach mode:
```bash
docker-compose up -d
```
## Database Migration
If you have implemented some models in `apps/<app-name>/models.py`.
You will want to see these changes on the applciation.
Therefore, having the docker images up, you have to create the `migrations.py` automatically:
```
docker-compose exec web python manage.py makemigrations
```
Once you have created the different migrations, you will want to do these migrations in your database.
```bash
docker-compose exec web python manage.py migrate
```

## Create a super user
The super user will have admin privileges.
```
docker-compose exec web python manage.py createsuperuser
```