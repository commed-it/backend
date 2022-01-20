import os
import uvicorn
import django

from commed.asgi import create_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commed.settings")
django.setup()

application = create_application()

if __name__ == '__main__':
    print("Get debug paramenter")
    debug = int(os.getenv('DJANGO_DEBUG')) == 1
    print(f'debug: {debug}')
    if debug:
        uvicorn.run('server:application', port=int(os.getenv('DJANGO_PORT')), host='0.0.0.0', reload=True)
    else:
        port = int(os.getenv('PORT', os.getenv('DJANGO_PORT')))
        host = os.getenv('HOST', '0.0.0.0')
        print(f"Starting server on: {port}")
        uvicorn.run('server:application', port=port, host=host)
