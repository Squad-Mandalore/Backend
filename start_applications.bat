@echo off

docker load -i path_to_your_backend_image_tar\backend_image.tar
docker load -i path_to_your_frontend_image_tar\frontend_image.tar

docker-compose up -d

pause
