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

## Testing

``` bash
docker-compose exec web python3 manage.py test
```

## Development tips
Copy the .env file and execute on a WSL or Linux terminal:

``` bash
cp .env-sample .env
source venv/bin/activate
set -o allexport; source .env; set +o allexport
```

The first line is to copy the sample, which is already configured for development options. The second is to activate the venv.

Finally, the third will export all the environment variables so that you can use `python3 manage.py <<comands>>`.

But you have to keep in mind that it tests with postgresql should also be done, and to keep your python version up to (or at least close to) python3.10, as the server is executed in this version.
