* Клонирование проекта

`git clone git@github.com:DeafProger/drf.git`

Заполните файл .env своими данным по примеру .env.sample


Сборка и запуск контейнеров

`docker-compose up --build`

* Регистрация нового пользователя - http://127.0.0.1:8000/register/ {POST}
* Получение токена - http://127.0.0.1:8000/login/
* Создание привычки - http://127.0.0.1:8000/habits/create/
* Документация: 
* Swagger - http://127.0.0.1:8000/swagger/
* Redoc - http://127.0.0.1:8000/redoc/
