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

# Как запускать после установки?
1. Запускать нужно все в отедльных папках, что бы логи были у каждого из сервисов.
2. Если мы уже все установили и перезапускали сервер, то нужно еще сделать `nohup sh <(curl -s https://cdn.shinobi.video/installers/shinobi-install.sh) &`.

# Как посмотреть логи?
Логи доступны в файле `nohup.out`. Наиболее простой способ просмотра логов - это использование утилиты less - `less nohup.out`.

# Как начать запись?
Начать запись можно используя 'tools/start_recording.py' Ее настройки и параметры можно посмотреть написав так: `python start_recording.py -h`.

# Как получить итоговые записи?
Записи сохраняются поминутно. Чтобы их объединить, необходимо воспользоваться 'tools/join_videos.py' Ее настройки и параметры можно посмотреть написав так: `python join_videos.py -h`.

# Как добавить новые камеры?
Для этого есть тулза `tools/load_cameras.py`. Ее настройки и параметры можно посмотреть написав так: `python load_cameras.py -h`.

# Running tests steps:
1. Ensure that Installation steps works fine
2. Run `pytest` in `lib/ut` directory

# How to start the server?
0. If you want to get all availiable options, run `python main.py -h`
1. Run `python main.py`,
