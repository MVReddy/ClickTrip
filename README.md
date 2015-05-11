
Before you start
1. All libs must be python 3
2. Need OpenCV
3. RabbitMQ,Celery is used
4. Change path informatoion in pics.tasks for cascade xml information according to your installation.

`$ python3.3 manage.py runserver`

from client

`curl -X POST http://localhost:8000/api/new/ -H "Content-Type: application/json"  -d '{"lat":26.9000, "lng":75.8000}'`

then check in django admin for pics saved. 