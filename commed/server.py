import os
import uvicorn
import django

from commed.asgi import create_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commed.settings")
django.setup()

application = create_application()

if __name__ == '__main__':
    debug = int(os.getenv('DJANGO_DEBUG')) == 1
    if debug:
        uvicorn.run('server:application', port=int(os.getenv('DJANGO_PORT')), host='0.0.0.0', reload=True)
    else:
        uvicorn.run('server:application', port=int(os.getenv('DJANGO_PORT')), host='0.0.0.0')
