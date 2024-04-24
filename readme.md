# Build Container
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 860297550696.dkr.ecr.ap-south-1.amazonaws.com
docker tag school-framework:latest 860297550696.dkr.ecr.ap-south-1.amazonaws.com/school-framework:latest
docker push 860297550696.dkr.ecr.ap-south-1.amazonaws.com/school-framework:latest

# Build Container
docker-compose build dev
docker-compose up dev -d
docker exec -it school_dev python manage.py migrate