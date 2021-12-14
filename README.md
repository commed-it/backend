# Commed Backend

## Database Model
![Database UML diagram](./doc/img/db.png)

## Structure

```
.
|- doc -- Contains documentation about the project, 
|  |      as well as scripts, mainly plantuml, for 
|  |      generating the diagrams
|  | 
|  | 
```

## Stack Used
- [Django](https://www.djangoproject.com/) - We will use Django for power up most of the services provided by the application
  + [django-channels](https://channels.readthedocs.io/en/stable/) - It powers up django to provide WebSockets, used by the chat.
  + [django-richtextfield](https://pypi.org/project/django-richtextfield/) - It gaves us a higher level RichTextField for the database.
- [Spacy](https://spacy.io/) - it provides us a way to achieve a better ontology for searching
- [Docker](https://www.docker.com/) - Container management.
- [SQLite](https://sqlite.org/index.html) - Open Source Database. Used only for development.
- [PostgreSQL](https://www.postgresql.org/) - Open source database with full bateries. Used for development, integration tests and deployment.
- [Django Rest Framework](https://www.django-rest-framework.org/) - Makes Django a REST framework
- [Dj-rest-auth](https://github.com/jazzband/dj-rest-auth) - Gets a secure API for authentication
- [Django All auth](https://django-allauth.readthedocs.io/en/latest/installation.html) - Secure Registration Implementation. Has many social adaptors.
## Collaborators
- @quimpm
- @Oriolac
- @Emina33
- @sergis

