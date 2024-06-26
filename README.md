# Library-API-Service

Service for borrowing books with stripe payment system and notifications via telegram bot

## Installing process
#### Run with IDE
``` shell
    git clone https://github.com/DmytroBondariev/CurrencyAPI.git
```
``` shell
    cd CurrencyAPI
```
Change mocks to your native data inside .env.sample. Do not forget to change file name to ".env".
#### Set unique data to .env file

    DJANGO_SECRET_KEY=your django secret key
    POSTGRES_DB_USER=your postgres user
    POSTGRES_DB_NAME=your postgres db name
    POSTGRES_DB_PASSWORD=yout postgres password

#### Run with docker
``` shell
    docker-compose up
```

## Features
* [Swagger documentation](http://localhost:8000/api/doc/swagger/)
* JWT authenticated:
  * [registration](http://localhost:8000/api/users/register/)
  * save access token after [login](http://localhost:8000/api/users/login/) and promote it with "Bearer" keyword via [MobHeader](https://chromewebstore.google.com/detail/modheader-modify-http-hea/idgpnmonknjnojddfkpgkljpfnnfcklj?pli=1) while sending requests
* [Admin panel](http://localhost:8000/admin/) - create admin via command:
``` shell
    manage.py createsuperuser
```
* Managing subscriptions for users
* Filtering currencies by name
* Filtering currencies history by date
* Celery task for sending request to external API(Monobank) every 10 minutes
* Command for uploading actual currencies to csv file (use inside django app docker container)
``` shell
    manage.py export_currencies
```
