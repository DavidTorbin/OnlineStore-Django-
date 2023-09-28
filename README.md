# Серверная часть магазина с API
с использование Django REST Framework

## Контракт для API
Названия роутов и ожидаемую структуру ответа от API endpoints можно найти в [swagger.yaml](./diploma_backend/swagger/swagger.yaml). 

## Запуск приложения
### Установка
Клонировать репозиторий:

``` git cline https://github.com/AlexMuller45/Django_REST_API_for_Shop.git```

Создать виртуальное окружение
``` 
cd Django_REST_API_for_Shop/
python3 -m venv venv_name
source venv_name/bin/activate
pip install -r requirements.txt
```

Установить diploma-frontend пакет в виртуальное окружение: 
```
cd diploma-frontend
pip install diploma-frontend-0.1.tar.gz
```

В `settings.py` проекта подключить приложение:
```python
INSTALLED_APPS = [
        ...
        'frontend',
    ]
```

В `urls.py` добавить:
```python
urlpatterns = [
    path("", include("frontend.urls")),
    ...
]
```

Если запустить сервер разработки: `python manage.py runserver`, то по адресу `127.0.0.1:8000` должна открыться стартовая страница интернет-магазина:
![image](./root-page.png)

### Детали подключаемого приложения `frontend`
Приложение служит только для отрисовки шаблонов из `templates/frontend`, поэтому в `urls.py` напрямую 
используются `TemplateView` из стандартной поставки Django.

В качестве frontend фреймворка был использован Vue3, который подключается в базовом шаблоне `templates/frontend/base.html`:
```
html <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
```
JS скрипт `static/frontend/assets/js/app.js` содержит реализацию Vue объекта, а все остальные JS скрипты из 
директории `static/frontend/assets/js` реализуют объекты примеси для соответствующей страницы проекта.
