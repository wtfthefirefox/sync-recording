# Документация
## Целевая аудитория
Основным заказчиком является Медиа центр МИЭМ, а так же другие медиа центры, которые хотят непрерывно записывать какие-либо комнаты с большим количеством камер и при этом с возможностью выбора аудио с одной из камер.

## Струтура проекта
* `lib` - весь основоной код API.
* `lib/ut` - тесты ручек и именно здесь нужно запускать тесты.
* `tools` - вспомогательные скрипты.

# Как установить?
0. `git clone https://github.com/wtfthefirefox/sync-recording.git`
1. `sudo su`
2. `sh <(curl -s https://cdn.shinobi.video/installers/shinobi-install.sh)`
3. `pip install -r requirements.txt`

# Первоначальная настройка shinobi
1. Переходим на `http://YOUR_SHINOBI_SERVER_IP_ADDRESS:8080/super`, где YOUR_SHINOBI_SERVER_IP_ADDRESS - ip shinobi.
2. Логинимся под admin@shinobi.video и admin данными.
3. Создаем нового супер пользователя.

# Как создать/получить API:
1. Открыть меню шиноби
2. На панели выбрать "API Keys"
3. Выберите нужные разрешения для API ключа и создайте его

# Как узнать Group Key
1. Открыть меню шиноби(http://YOUR_SHINOBI_SERVER_IP_ADDRESS:8080)
2. Найти слева в меню и открыть Account settings 
3. В начале страницы можно найти Group Key

Переходим в папку проекта и запустаем скрипт для установки используемых пакетов.

`pip install -r requirements.txt`

Убеждаемся, что все тесты корректно работают:
1. `cd lib/ut`
2. `pytest`

## Добавление комнат в shinobi
С помощью скрипта `tools/load_cameras.py` возможно добавлять свои камеры с нужным конфигом.
Подробное описание каждого из параметров можно найти в документации к API Shinobi:
<https://docs.shinobi.video/api/add-edit-or-delete-a-monitor>

Пример запуска функции:
```
python load_cameras.py --ip IP  --api API_KEY --group_key GROUP_KEY --from_json True --input_json rooms.json
```
`IP` - это ip shinobi<br/>
`API_KEY` - ключ API в shinobi<br/>
`GROUP_KEY` - ключ группы в shinobi<br/>
`rooms.json` - путь к файлу с камера

# Как запускать после установки?
1. Запускать нужно все в отедльных папках, что бы логи были у каждого из сервисов.
2. Если мы уже все установили и перезапускали сервер, то нужно еще сделать `nohup sh <(curl -s https://cdn.shinobi.video/installers/shinobi-install.sh) &`.

# Как посмотреть логи?
Логи доступны в файле `nohup.out`. Наиболее простой способ просмотра логов - это использование утилиты less - `less nohup.out`.

# Как начать запись?
Начать запись можно используя 'tools/start_recording.py' Ее настройки и параметры можно посмотреть написав так: `python start_recording.py -h`.

# Как получить итоговые записи?
Записи сохраняются поминутно. Чтобы их объединить, необходимо воспользоваться `tools/join_videos.py` Ее настройки и параметры можно посмотреть написав так:
```
python join_videos.py --placeholder PLACEHORLDER_PATH --folder SHINOBI_PATH --audio_file VIDEO_PATH
```
`PLACEHORLDER_PATH` - это путь к картинке 'Нет сигнала'<br/>
`SHINOBI_PATH` - это путь к главная папке, в которой хранятся папки с записями<br/>
`VIDEO_PATH` - это путь к фалу, с которого нужно взять аудио

## А где в итоге все запускается?
Сама shinobi будет доступна на `http://your_ip:8080`, а апи доступна соотвественно на `http://your_ip:8081`.

## API
1. GET /api/v1/health_check/{camera_id} - проверяем жива ли камера / комната, где camera_id это id камеры или комнаты.
2. POST /api/v1/record_start/ + тело запроса: {"room_id": room_id} - ручка для старта записи и ее нельзя отпускать пока не завершена запись, где room_id это id комнаты.
3. POST /api/v1/record_stop/ + тело запроса: {"room_id": room_id} - ручка для окончания записи, где room_id это id комнаты результат записи будет лежать в export_dir переменной указанной в [конфиге](../settings.yaml).
4. GET api/v1/download/file/{file_name} - ручка для получения скачивания сделанных записей, где file_name - имя файла для скачивания
