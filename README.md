## Docker

docker-compose down -v  # Stop and remove volumes
docker-compose up --build  # Rebuild and restart
docker exec -it django_container pip install -r requirements.txt
docker exec -it django_container python manage.py makemigrations api
docker exec -it django_container python manage.py migrate
docker exec -it django_container python manage.py runserver 0.0.0.0:8200
http://localhost:8200/
http://localhost:8200/api/
http://localhost:8200/api/token

✅ 100% Test Coverage using TDD
docker exec -it django_container pytest --ds=core.settings --cov=api


✅ Generic Model, ModelViewSet, and Serializer
✅ API structure similar to provided format
✅ JWT Authentication
✅configuration
✅validation
✅ Postman Collection with Token Authentication
✅ JSON and Excel support