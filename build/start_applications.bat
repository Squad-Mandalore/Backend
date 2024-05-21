@echo off

docker load -i backend_image.tar
docker load -i frontend_image.tar

docker compose up -d

pause
