import os
import uvicorn
import django
import re

from commed.asgi import create_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commed.settings")
django.setup()

application = create_application()

if __name__ == '__main__':
    print("Get debug paramenter")
    debug = int(os.getenv('DJANGO_DEBUG')) == 1
    print(f'debug: {debug}')
    port = int(os.getenv('PORT', os.getenv('DJANGO_PORT')))
    host = os.getenv('HOST', '0.0.0.0')
    postgres_url = os.getenv('DATABASE_URL', False)
    if postgres_url:
        matcher = re.compile(r'postgres://([\w]+):([\w]+)@([\w\-.]+):([\d]+)/([\w]+)')
        match = matcher.match(postgres_url)
        m = match.groups()
        os.environ['POSTGRES_USER'] = m[0]
        os.environ['POSTGRES_PASSWORD'] = m[1]
        os.environ['POSTGRES_HOST'] = m[2]
        os.environ['POSTGRES_PORT'] = m[3]
        os.environ['POSTGRES_DBNAME'] = m[4]
    if debug:
        uvicorn.run('server:application', port=port, host=host, reload=True)
    else:
        print(f"Starting server on: {port}")
        uvicorn.run('server:application', port=port, host=host)
