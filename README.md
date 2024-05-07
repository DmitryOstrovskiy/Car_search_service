#### **API: Сервис поиска ближайших машин для перевозки грузов.**

### Описание

**REST API сервиc для поиска ближайших машин к грузам. При создании машины, ей автоматически, в случайном порядке, присваивается локация из загруженного в базу списка локаций. Каждая локация имеет свои харакетистики, включая широут и долготу. Созданный груз обязательно должен иметь локацию местонахождения и локацию доставки. Сервис анализиурет локацию имеющихся машин и подбирает ближайшие к метоположению груза, на расстояни не более 450 миль. Возможен просомрт всего списка грузов с количеством ближайших машин и просомотр деталей конкретного груза со списки номеров машин и расстоянием до груза.** 
 
### Функционал

- **БД по умолчанию должна заполнена 20 машинами.**
- **В БД загружен файл с локациями.**
- **Груз содержит следующие характеристики:**

    *локация pick-up*

    *локация delivery*

    *вес (1-1000)*

    *описание*
- **Машина содержит следующие характеристики:**

    *уникальный номер (цифра от 1000 до 9999 + случайная заглавная буква английского алфавита в конце, пример: "1234A", "2534B", "9999Z")*

    *текущая локация*

    *грузоподъемность (1-1000)*
- **Локация содержит следующие характеристики:**

    *город*

    *штат*

    *почтовый индекс (zip)*

    *широта*

    *долгота*
- **При создании машин по умолчанию локация каждой машины заполняется случайным образом.**
- **Создание нового груза (характеристики локаций pick-up, delivery определяются по введенному zip-коду)**
- **Получение списка грузов (локации pick-up, delivery, количество ближайших машин до груза ( =< 450 миль))** Расчет и отображение расстояния осуществляется в милях. Расчет расстояния осуществляется с помощью библиотеки geopy. Маршруты не учитыватются, используются расстояния от точки до точки.
- **Получение информации о конкретном грузе по ID (локации pick-up, delivery, вес, описание, список номеров ВСЕХ машин с расстоянием до выбранного груза)**
- **Редактирование машины по ID (локация (определяется по введенному zip-коду))**
- **Редактирование груза по ID (вес, описание)**
- **Удаление груза по ID**
- **Фильтр списка грузов (вес, мили ближайших машин до грузов)**
- **Автоматическое обновление локаций всех машин раз в 3 минуты (локация меняется на другую случайную)**

### Технологии

- Python 3.9
- Django 4.2.11
- Django Rest Framework 3.15.1
- drf-spectacular 0.27.1
- geopy 2.4.1
- redis 5.0.3
- celery 5.3.6

### Установка и запуск проекта

Клонируйте репозиторий и перейдите к нему в командной строке:
```sh
git clone https://github.com/DmitryOstrovskiy/Car_search_service && cd Car_search_service
```
Создать и запустить контейнер:

```sh
docker-compose up -d
```

###  Проект запущен по адресу::

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/api/schema/swagger-ui/ - документация по пользовательскому интерфейсу Swagger
- http://127.0.0.1:8000/api/schema/redoc/ - документация по пользовательскому интерфейсу redoc
- http://127.0.0.1:8000/admin/ - страница администратора


### Примеры запрсоов:

### _Создание машины_
**POST**: http://127.0.0.1:8000/api/trucks/

Request example:
```json
{
  "unique_number": "3658J",
  "capacity": 850
}
```
Response example:
```json
{
    "unique_number": "3658J",
    "current_location": {
        "city": "Auburn",
        "state": "Washington",
        "zip_code": "98002",
        "latitude": "47.308200",
        "longitude": "-122.215670"
    },
    "capacity": 850
}
```

### _Создание груза_
**POST**: http://127.0.0.1:8000/api/cargos/
Request example:
```json
{
  "pick_up_location_zip": 29175,
  "delivery_location_zip": 29201,
  "weight": 750,
  "description": "string10"
}
```
Response example:
```json
{
    "id": 7,
    "weight": 750,
    "description": "string10",
    "nearby_trucks": [
        "4545L",
        "1478U",
        "4613H",
        "6497W"
    ],
    "pick_up_location": {
        "city": "Westville",
        "state": "South Carolina",
        "zip_code": "29175",
        "latitude": "34.442660",
        "longitude": "-80.606660"
    },
    "delivery_location": {
        "city": "Columbia",
        "state": "South Carolina",
        "zip_code": "29201",
        "latitude": "33.983810",
        "longitude": "-81.028290"
    }
}
```
### _Получение списка грузов_
**GET**: http://127.0.0.1:8000/api/cargos/

Response example:
```json
[
    {
        "id": 3,
        "pick_up_location": {
            "city": "Melrose Park",
            "state": "Illinois",
            "zip_code": "60164",
            "latitude": "41.916670",
            "longitude": "-87.901120"
        },
        "delivery_location": {
            "city": "Comerio",
            "state": "Puerto Rico",
            "zip_code": "00782",
            "latitude": "18.225010",
            "longitude": "-66.224520"
        },
        "nearby_trucks_count": 0
    },
    {
        "id": 6,
        "pick_up_location": {
            "city": "McIntyre",
            "state": "Georgia",
            "zip_code": "31054",
            "latitude": "32.882140",
            "longitude": "-83.207230"
        },
        "delivery_location": {
            "city": "San Juan",
            "state": "Puerto Rico",
            "zip_code": "00907",
            "latitude": "18.452870",
            "longitude": "-66.083810"
        },
        "nearby_trucks_count": 2
    },
    {
        "id": 7,
        "pick_up_location": {
            "city": "Westville",
            "state": "South Carolina",
            "zip_code": "29175",
            "latitude": "34.442660",
            "longitude": "-80.606660"
        },
        "delivery_location": {
            "city": "Columbia",
            "state": "South Carolina",
            "zip_code": "29201",
            "latitude": "33.983810",
            "longitude": "-81.028290"
        },
        "nearby_trucks_count": 4
    }
]
```
### _Получение информации о конкретном грузе по ID_
**GET**: http://127.0.0.1:8000/api/cargos/6/

Response example:
```json
    {
    "id": 6,
    "pick_up_location": {
        "city": "McIntyre",
        "state": "Georgia",
        "zip_code": "31054",
        "latitude": "32.882140",
        "longitude": "-83.207230"
    },
    "delivery_location": {
        "city": "San Juan",
        "state": "Puerto Rico",
        "zip_code": "00907",
        "latitude": "18.452870",
        "longitude": "-66.083810"
    },
    "weight": 750,
    "description": "string_read",
    "truck_distances": [
        {
            "unique_number": "1478U",
            "distance": 159.03496728169307
        },
        {
            "unique_number": "4613H",
            "distance": 228.11579427313006
        },
        {
            "unique_number": "6497W",
            "distance": 327.04417512170545
        },
        {
            "unique_number": "3214M",
            "distance": 348.38192903705146
        },
        {
            "unique_number": "4545L",
            "distance": 384.3881289203619
        },
        {
            "unique_number": "7946N",
            "distance": 442.4248020902889
        },
        {
            "unique_number": "98765",
            "distance": 446.76998815006783
        }
    ]
}
```
### _Редактирование машины по ID_
**PUT**: http://127.0.0.1:8000/api/trucks/3/
Request example:
```json
{
  "zip_code": "78558"
}
```
Response example:
```json
{
    "unique_number": "98765",
    "current_location": {
        "city": "La Blanca",
        "state": "Texas",
        "zip_code": "78558",
        "latitude": "26.292760",
        "longitude": "-98.023660"
    },
    "capacity": 2147483647
}
```
### _Редактирование груза по ID_
**PUT**: http://127.0.0.1:8000/api/cargos/6/
Request example:
```json
{
  "weight": 750,
  "description": "string_read"
}
```
Response example:
```json
{
    "weight": 750,
    "description": "string_read"
}
```
### _Удаление груза_
**DELETE**: http://127.0.0.1:8000/api/cargos/3/



### Author - Dmitriy Ostrovskiy

# 💫 About Me:
🔭 I am currently working on Django projects<br>👯 I’m looking to collaborate on<br>🤝 I’m looking for help with<br>🌱 I am currently learning how to work with FastAPI<br>💬 Ask me about<br>⚡ Fun fact


## 🌐 Socials:
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/DmitriyOstrovskiy) 

# 💻 Tech Stack:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white) ![PowerShell](https://img.shields.io/badge/PowerShell-%235391FE.svg?style=for-the-badge&logo=powershell&logoColor=white) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens) ![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
# 📊 GitHub Stats:
![](https://github-readme-stats.vercel.app/api?username=DmitryOstrovskiy&theme=tokyonight&hide_border=false&include_all_commits=true&count_private=true)<br/>
![](https://github-readme-streak-stats.herokuapp.com/?user=DmitryOstrovskiy&theme=tokyonight&hide_border=false)<br/>
![](https://github-readme-stats.vercel.app/api/top-langs/?username=DmitryOstrovskiy&theme=tokyonight&hide_border=false&include_all_commits=true&count_private=true&layout=compact)

---
[![](https://visitcount.itsvg.in/api?id=DmitryOstrovskiy&icon=0&color=0)](https://visitcount.itsvg.in)

<!-- Proudly created with GPRM ( https://gprm.itsvg.in ) -->