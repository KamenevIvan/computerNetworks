## Задание 7

Блокировка российских IP

## Запуск

Контейнер с бд:
````
docker run -d --name db --network my_network -e POSTGRES_DB=avito_parser -e POSTGRES_USER=parser_user -e POSTGRES_PASSWORD=password postgres
````

Контейнер приложения (внимание, делать в той же папке, где лежит dockerfile):
````
docker build -t my_fastapi_app .
docker run -d --name app --network my_network -p 5000:5000 my_fastapi_app
````

Необходимо создать контейнер с nginx:
````
docker build -t my_nginx_image -f Dockerfile_nginx .
docker run -d --name my_nginx --network my_network -p 80:80 my_nginx_image
````
Внимание! следите за названиями сети my_network, все трое должны быть в одной сети, иначе ничего работать не будет!
Теперь, если всё правильно, по адресу: http://localhost/docs у вас будет заглушка. 

## Использование 
Запрос на добавление url в базу данных:
````
docker exec -it my_nginx curl -X POST "http://localhost/parse?url=YOUR_URL" -H "accept: application/json"
````
Ожидаемый ответ: {"message":"URL added successfully"}

Запрос на показ всех добавленных url:
````
docker exec -it my_nginx curl -X GET "http://localhost/ads" -H "accept: application/json"
````
Ожидаемый ответ: {"id":1,"link":"https://vk.com/feed"},...
