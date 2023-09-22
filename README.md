# QRkot_spreadseets
### Описание 
```
Сервис собирает пожертвования на различные целевые проекты, связанные с поддержкой кошачьей популяции. Реализована дополнительная возможность формирования отчёта в гугл-таблице.
```

### Технологи проекта:
```
Python
FasAPI
SQLAlchemy
Alembic
Pydantic
Uvicorn
Google API
```

### Как запустить проект

Клонировать репозиторий:
```
git clone https://github.com/Nastasya-M/QRkot_spreadsheets
```
Создать виртуальное окружение:
```
python -m venv venv
```
Активировать виртуальное окружение и установить зависимости:
```
source venv/Scripts/activate
pip install -r requirements.txt
```

### Пример заполнения .env файла:
```
APP_TITLE=Кошачий благотворительный фонд
DESCRIPTION=Сервис для поддержки котиков
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secret #Придумайте секретный код
FIRST_SUPERUSER_EMAIL=user@example.com
FIRST_SUPERUSER_PASSWORD=example1234
EMAIL=<USER_EMAIL>
TYPE=service_account
PROJECT_ID=<PROJECT_ID>
PRIVATE_KEY_ID=<PRIVATE_KEY_ID>
PRIVATE_KEY=<PRIVATE_KEY>
CLIENT_EMAIL=<CLIENT_EMAIL>
CLIENT_ID=<CLIENT_ID>
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=<CLIENT_ID>
```


### Документация
```
Swagger: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
```
Автор: [Настасья Мартынова](https://github.com/Nastasya-M)