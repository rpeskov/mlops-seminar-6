# Справочник команд к занятию «Сервис инференса и контейнер Docker»

Все команды занятия в порядке появления. Для каждой: что делает, что означает каждый флаг, как выглядит вывод и что в нём смотреть. Примеры вывода реальные по структуре, числа и идентификаторы у вас будут свои.

Команды набираются в терминале в папке с репозиторием. На Windows используйте PowerShell или cmd, на Mac и Linux любой терминал.

---

## Проверка окружения

### `docker --version`

Показывает версию Docker. Если команда не найдена, Docker не установлен или терминал открыт до установки.

```
Docker version 27.3.1, build ce12230
```

Нужна только первая часть: версия больше 20, всё подходит.

### `python --version`

Показывает версию Python. Должна начинаться с `3.12`. На некоторых системах нужно писать `python3`.

```
Python 3.12.6
```

### `docker run --rm hello-world`

Запускает крошечный тестовый контейнер, который печатает приветствие и завершается. Проверяет всю цепочку: Docker работает, может скачать образ, может запустить контейнер.

| Часть | Значение |
|---|---|
| `docker run` | создать и запустить контейнер из образа |
| `--rm` | удалить контейнер после остановки, чтобы не копились остановленные |
| `hello-world` | имя образа; тег не указан, подставится `latest` |

При первом запуске образ скачивается:

```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
c1ec31eb5944: Pull complete
Digest: sha256:d2b1...
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

Первые строки: образа нет локально, Docker скачал его из реестра по умолчанию, Docker Hub. `Pull complete` напротив слоя: слой скачан. `Digest`: контрольная сумма образа. Дальше текст от самого контейнера. Если видите `Hello from Docker!`, всё работает. При повторном запуске первых строк не будет, образ уже на диске.

---

## Окружение и модель

### `python -m venv .venv`

Создаёт виртуальное окружение: папку `.venv` с отдельной копией Python и пустым набором пакетов.

| Часть | Значение |
|---|---|
| `-m venv` | запустить встроенный модуль `venv` как программу |
| `.venv` | имя папки для окружения; точка в начале делает её скрытой |

Вывода нет. Проверка: появилась папка `.venv`.

### Активация окружения

Mac и Linux:
```
source .venv/bin/activate
```

Windows, PowerShell:
```
.venv\Scripts\Activate.ps1
```

Windows, cmd:
```
.venv\Scripts\activate.bat
```

Вывода нет, но в начале строки приглашения появляется `(.venv)`:

```
(.venv) user@laptop project %
```

Это единственный признак, что окружение активно. Нет `(.venv)`, значит пакеты пойдут в системный Python. В каждом новом терминале активацию надо повторять.

Если PowerShell пишет `running scripts is disabled on this system`, выполните один раз `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, ответьте `Y` и повторите активацию.

### `pip install -r requirements.txt`

Устанавливает пакеты по списку из файла.

| Часть | Значение |
|---|---|
| `pip install` | установить пакеты |
| `-r requirements.txt` | взять список из файла, по одному пакету на строку |

В файле версии указаны точно, через `==`, например `scikit-learn==1.8.0`. Это означает «именно эта версия», без обновлений.

```
Collecting fastapi==0.162.0
  Downloading fastapi-0.162.0-py3-none-any.whl (97 kB)
Collecting scikit-learn==1.8.0
  Downloading scikit_learn-1.8.0-cp312-cp312-macosx_12_0_arm64.whl (11.2 MB)
...
Installing collected packages: numpy, scipy, ..., scikit-learn, fastapi
Successfully installed fastapi-0.162.0 numpy-2.4.4 scikit-learn-1.8.0 ...
```

`Collecting`: pip нашёл пакет. `Downloading`: скачивает. Обратите внимание, что скачивается больше пакетов, чем в файле: это зависимости зависимостей. Последняя строка `Successfully installed` со списком всего, что поставлено. Если вместо неё `ERROR`, читайте строку над ней.

### `python train.py`

Запускает скрипт обучения из репозитория. Он генерирует данные, обучает модель и сохраняет её в файл.

```
rows: 2000, cities: moscow, spb, kazan, ekb
validation MAE: 956 484 rub
scikit-learn 1.8.0
saved: model.bin
```

Строки печатает сам скрипт. Запомните версию scikit-learn, она должна совпадать с версией в `requirements.txt`. Если при запуске появится `InconsistentVersionWarning`, версии разошлись.

---

## Сервис

### `uvicorn app:app --host 0.0.0.0 --port 8000`

Запускает HTTP-сервер с вашим приложением.

| Часть | Значение |
|---|---|
| `uvicorn` | сервер, который умеет запускать приложения FastAPI |
| `app:app` | до двоеточия имя файла без `.py`, после двоеточия имя объекта приложения в этом файле |
| `--host 0.0.0.0` | слушать на всех сетевых интерфейсах, а не только на локальном; внутри контейнера без этого сервис недоступен снаружи |
| `--port 8000` | порт, на котором принимать запросы |

```
INFO:     Started server process [48213]
INFO:     Waiting for application startup.
INFO:     model 2026-11-05-linreg loaded from model.bin
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

`Started server process`: процесс запущен, в скобках его номер. `Waiting for application startup`: выполняется код старта, у нас это загрузка модели. Строка про модель напечатана нашим кодом из `lifespan`. `Application startup complete`: модель загружена, можно слать запросы. Последняя строка: адрес и порт. Терминал занят, пока сервер работает. Остановка: `Ctrl+C`.

Дальше на каждый запрос появляется строка:

```
INFO:     127.0.0.1:52140 - "POST /predict HTTP/1.1" 200 OK
INFO:     127.0.0.1:52141 - "POST /predict HTTP/1.1" 422 Unprocessable Entity
```

Откуда пришёл запрос, метод, путь, код ответа. Это и есть простейший журнал, по которому видно, что происходит.

### `curl -i http://localhost:8000/health`

Отправляет HTTP-запрос и печатает ответ.

| Часть | Значение |
|---|---|
| `curl` | инструмент командной строки для HTTP-запросов |
| `-i` | показать заголовки ответа вместе с телом; без него печатается только тело |
| адрес | куда слать: `localhost` это ваша машина, `8000` порт, `/health` путь |

Метод не указан, значит GET.

```
HTTP/1.1 200 OK
date: Thu, 05 Nov 2026 10:31:02 GMT
server: uvicorn
content-length: 15
content-type: application/json

{"status":"ok"}
```

Первая строка: версия протокола, код состояния, его название. Дальше заголовки: когда ответили, какой сервер, длина тела, формат тела. Пустая строка отделяет заголовки от тела. Тело: JSON с ответом.

На Windows в PowerShell пишите `curl.exe`: без `.exe` сработает другая команда.

### `curl -i http://localhost:8000/ready`

То же самое для проверки готовности.

```
HTTP/1.1 200 OK
...
{"status":"ready","model_version":"2026-11-05-linreg"}
```

В теле версия модели. Если модель не загружена, вместо 200 будет 503 и `{"detail":"model not loaded"}`.

### Запрос на предсказание

```
curl -i -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"city": "moscow", "rooms": 2, "area": 54.5}'
```

| Часть | Значение |
|---|---|
| `-X POST` | метод запроса; по умолчанию GET, для передачи данных нужен POST |
| `-H "Content-Type: application/json"` | заголовок: в теле запроса лежит JSON. Без него сервер не поймёт формат |
| `-d '...'` | тело запроса, данные, которые отправляем |
| `\` в конце строки | перенос команды на следующую строку; можно написать всё в одну строку без них |

Одинарные кавычки вокруг JSON нужны, чтобы двойные кавычки внутри дошли до сервера как есть. На Windows с этим проблемы, используйте `python test_requests.py`.

```
HTTP/1.1 200 OK
...
content-type: application/json

{"price":17053472.0,"model_version":"2026-11-05-linreg"}
```

### Неправильные запросы

Нет поля `area`:

```
HTTP/1.1 422 Unprocessable Entity
...
{"detail":[{"type":"missing","loc":["body","area"],"msg":"Field required","input":{"city":"moscow","rooms":2}}]}
```

`detail` это список ошибок. В каждой: `type` вид ошибки, `loc` где, в теле запроса поле `area`, `msg` текст, `input` что пришло. Сервер не вызывал модель.

Строка вместо числа, `"area": "54.5"`:

```
{"detail":[{"type":"float_type","loc":["body","area"],"msg":"Input should be a valid number","input":"54.5"}]}
```

Площадь вне диапазона, `"area": -1`:

```
{"detail":[{"type":"greater_than","loc":["body","area"],"msg":"Input should be greater than 10","input":-1,"ctx":{"gt":10.0}}]}
```

Незнакомый город, `"city": "Москва"`:

```
{"detail":[{"type":"literal_error","loc":["body","city"],"msg":"Input should be 'moscow', 'spb', 'kazan' or 'ekb'","input":"Москва","ctx":{"expected":"'moscow', 'spb', 'kazan' or 'ekb'"}}]}
```

Во всех четырёх случаях код 422 и понятное описание. Все четыре ошибки клиента.

### `python test_requests.py`

Отправляет те же семь запросов через библиотеку `requests` и печатает код и тело каждого. Работает одинаково на всех системах. Адрес можно передать аргументом: `python test_requests.py http://localhost:8001`.

```
Сервис: http://localhost:8000

[   ок    ] служебный адрес /health
           GET /health  ->  200 (ожидали 200)
           {"status": "ok"}

[   ок    ] правильный запрос
           POST /predict  ->  200 (ожидали 200)
           {"price": 17053472.0, "model_version": "2026-11-05-linreg"}

[   ок    ] нет поля area
           POST /predict  ->  422 (ожидали 422)
           ...

Все 7 проверок прошли.
```

Если вместо `ок` стоит `НЕ ТО`, код ответа отличается от ожидаемого. Если `ошибка` и «нет соединения», сервис не запущен, порт другой, или внутри контейнера нет `--host 0.0.0.0`.

### `python batch_client.py sample.csv`

Домашнее задание. Отправляет каждую строку CSV в работающий сервис по HTTP и считает статистику. Сервис должен быть запущен.

```
всего: 100, успешно: 91, ошибок: {422: 9}
среднее время ответа: 2.5 мс
результаты: predictions.csv
```

### `python batch_score.py sample.csv`

Пакетный режим без сервиса: скрипт сам загружает `model.bin` и считает цены. Запускать можно при остановленном сервисе.

```
всего: 100, оценено: 97, ошибок: {'type': 3}
результаты: predictions_batch.csv
```

Три ошибки `type` это строки, где площадь или число комнат не превращаются в число. Остальные 97 получили цену, включая площадь 545 и город «Москва». После подключения схемы `Listing` из `app.py` вывод станет `оценено: 91, ошибок: {'type': 3, 'schema': 6}`.

### Документация в браузере

Откройте `http://localhost:8000/docs`. Это страница, которую FastAPI строит по вашим схемам: список адресов, для каждого описание входа и выхода, и кнопка «Try it out», которая отправляет запрос из браузера. Удобно для тех, кому неудобен `curl`.

---

## Контейнер

### `docker build -t price-estimate:local .`

Собирает образ по Dockerfile.

| Часть | Значение |
|---|---|
| `docker build` | собрать образ |
| `-t price-estimate:local` | имя и тег образа через двоеточие; без `-t` образ получит только идентификатор |
| `.` | папка, в которой лежит Dockerfile и файлы для копирования; точка означает текущую |
| `--platform linux/amd64` | добавить на Mac с Apple Silicon: собрать под архитектуру обычных серверов |

```
[+] Building 48.7s (11/11) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load metadata for docker.io/library/python:3.12-slim
 => [1/6] FROM docker.io/library/python:3.12-slim@sha256:9a1c...
 => [2/6] WORKDIR /app
 => [3/6] COPY requirements.txt .
 => [4/6] RUN pip install --no-cache-dir -r requirements.txt
 => [5/6] COPY app.py .
 => [6/6] COPY model.bin .
 => exporting to image
 => => naming to docker.io/library/price-estimate:local
```

Каждая строка `[N/6]` это инструкция из Dockerfile, по порядку. Справа время выполнения. Шаг 4 с установкой пакетов самый долгий. Если собрать повторно без изменений, напротив шагов появится `CACHED`: слой взят из кэша, выполнять заново не пришлось. Последняя строка: образу присвоено имя.

Если сборка упала, ошибка будет под той строкой `[N/6]`, на которой остановилась.

### `docker images price-estimate`

Список образов на диске, отфильтрованный по имени.

```
REPOSITORY       TAG     IMAGE ID       CREATED          SIZE
price-estimate   local   3f1c2a9b8d7e   40 seconds ago   245MB
```

`REPOSITORY` имя, `TAG` тег, `IMAGE ID` первые символы идентификатора, `CREATED` когда собран, `SIZE` размер. Без имени команда покажет все образы на машине.

### `docker run --rm -p 8000:8000 price-estimate:local`

Запускает контейнер из образа.

| Часть | Значение |
|---|---|
| `--rm` | удалить контейнер после остановки |
| `-p 8000:8000` | проброс порта: слева порт на вашей машине, справа порт внутри контейнера. Без этого сервис внутри работает, но снаружи недоступен |
| `price-estimate:local` | какой образ запустить |

Вывод тот же, что у `uvicorn` без контейнера, потому что внутри запущен он же. Терминал занят. Остановка: `Ctrl+C`.

Если нужно запустить в фоне и освободить терминал, добавьте `-d`, тогда вместо логов напечатается идентификатор контейнера, а логи можно посмотреть через `docker logs`.

### `docker ps`

Список работающих контейнеров.

```
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS          PORTS                    NAMES
a1b2c3d4e5f6   price-estimate:local   "uvicorn app:app --h…"   20 seconds ago   Up 19 seconds   0.0.0.0:8000->8000/tcp   quirky_turing
```

`CONTAINER ID` идентификатор. `IMAGE` из какого образа. `COMMAND` что запущено внутри. `STATUS` сколько работает. `PORTS` проброс: `0.0.0.0:8000->8000/tcp` означает, что порт 8000 вашей машины ведёт на порт 8000 контейнера. `NAMES` имя; если вы не задали своё через `--name`, Docker придумал случайное.

Если контейнера в списке нет, он упал сразу после старта. Добавьте `-a`, чтобы увидеть и остановленные, затем `docker logs <имя>` для причины.

### `docker logs quirky_turing`

Показывает всё, что контейнер напечатал. Имя или идентификатор берётся из `docker ps`. Первая команда при любой отладке: контейнер не отвечает, смотрите логи.

Полезный флаг `-f`: показывать логи непрерывно, как они появляются. Выход `Ctrl+C`.

---

## Реестр

### `docker run -d -p 5000:5000 --name registry registry:2`

Запускает локальный реестр образов в контейнере.

| Часть | Значение |
|---|---|
| `-d` | в фоне: терминал освобождается, вместо логов печатается идентификатор |
| `-p 5000:5000` | порт 5000 вашей машины на порт 5000 реестра |
| `--name registry` | имя контейнера, чтобы потом остановить по имени |
| `registry:2` | официальный образ реестра, версия 2 |

```
7d3e9f1a2b4c5d6e7f8091a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2
```

Единственная строка: идентификатор запущенного контейнера. Проверить, что работает: `docker ps`, в списке появится `registry`.

На Mac порт 5000 бывает занят системной службой. Тогда `-p 5001:5000` и дальше везде `localhost:5001`.

### `curl http://localhost:5000/v2/_catalog`

Список репозиториев в реестре. Это обычный GET-запрос к HTTP-адресу реестра.

```
{"repositories":[]}
```

Пустой список: пока ничего не отправлено. После `push`:

```
{"repositories":["price-estimate"]}
```

### `docker tag price-estimate:local localhost:5000/price-estimate:2026-11-05-linreg`

Даёт образу второе имя. Ничего не копирует, не собирает и не отправляет.

| Часть | Значение |
|---|---|
| первый аргумент | существующее имя |
| второй аргумент | новое имя в виде `адрес-реестра/имя:тег` |
| `localhost:5000` | адрес реестра; без этой части Docker при `push` пойдёт в Docker Hub |
| `2026-11-05-linreg` | тег, осмысленная версия |

Вывода нет. Проверка: `docker images` покажет один и тот же `IMAGE ID` под двумя именами.

### `docker push localhost:5000/price-estimate:2026-11-05-linreg`

Отправляет образ в реестр, слой за слоем.

```
The push refers to repository [localhost:5000/price-estimate]
5f70bf18a086: Pushed
e2a8b3c1d4f5: Pushed
9c8b7a6f5e4d: Pushed
1a2b3c4d5e6f: Pushed
2026-11-05-linreg: digest: sha256:4e1f... size: 1572
```

Первая строка: куда. Дальше по строке на слой: `Pushed` отправлен, `Layer already exists` уже был в реестре от прошлой отправки. Последняя строка: тег, контрольная сумма образа, размер описания.

Если вместо этого `denied: requested access to the resource is denied`, в имени нет `localhost:5000/`, и Docker пытался отправить в Docker Hub.

### `curl http://localhost:5000/v2/price-estimate/tags/list`

Список тегов одного репозитория.

```
{"name":"price-estimate","tags":["2026-11-05-linreg"]}
```

### `docker image rm localhost:5000/price-estimate:2026-11-05-linreg`

Удаляет образ с таким именем с вашей машины.

```
Untagged: localhost:5000/price-estimate:2026-11-05-linreg
Untagged: localhost:5000/price-estimate@sha256:4e1f...
```

`Untagged` означает, что снято имя. Сами слои остались, потому что на них ещё ссылается имя `price-estimate:local`. Если бы и его не было, появились бы строки `Deleted` для каждого слоя.

### `docker pull localhost:5000/price-estimate:2026-11-05-linreg`

Скачивает образ из реестра.

```
2026-11-05-linreg: Pulling from price-estimate
5f70bf18a086: Already exists
e2a8b3c1d4f5: Already exists
9c8b7a6f5e4d: Already exists
1a2b3c4d5e6f: Already exists
Digest: sha256:4e1f...
Status: Downloaded newer image for localhost:5000/price-estimate:2026-11-05-linreg
localhost:5000/price-estimate:2026-11-05-linreg
```

`Already exists` напротив слоёв: слои физически уже есть на машине, Docker их не качает заново, только восстанавливает имя. На чистой машине вместо этого было бы `Pull complete` для каждого слоя. `Status`: образ с этим именем теперь есть локально.

### `docker stop registry`

Останавливает контейнер по имени.

```
registry
```

Печатает имя остановленного. Контейнер не удалён, его можно запустить снова через `docker start registry`. Чтобы удалить совсем: `docker rm registry`.

---

## Команды из демонстрации на лекции

### `docker run -d --name demo python:3.12-slim sleep 300`

Запускает контейнер, который пять минут ничего не делает.

| Часть | Значение |
|---|---|
| `-d` | в фоне |
| `--name demo` | имя |
| `python:3.12-slim` | образ |
| `sleep 300` | команда внутри контейнера вместо той, что задана в образе: ждать 300 секунд |

Вывод: идентификатор контейнера.

### `docker rm -f demo demo2`

Удаляет контейнеры по именам.

| Часть | Значение |
|---|---|
| `rm` | удалить контейнер |
| `-f` | сначала остановить, если работает; без `-f` работающий контейнер удалить нельзя |

```
demo
demo2
```

Имена удалённых. Образ при этом остаётся: `docker images` покажет его на месте.

---

## Как читать любую ошибку

1. Последняя строка вывода обычно содержит суть: `ERROR`, `denied`, `not found`, `connection refused`.
2. `connection refused` или `connection reset` при запросе к сервису: сервис не запущен, другой порт, или внутри контейнера нет `--host 0.0.0.0`.
3. `port is already allocated`: порт занят другим контейнером, смотрите `docker ps`.
4. `ModuleNotFoundError`: не активировано окружение, нет `(.venv)` в приглашении.
5. `no such file or directory: Dockerfile`: терминал открыт не в той папке.
6. `denied` при `push`: нет `localhost:5000/` в имени образа.
