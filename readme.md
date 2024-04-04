# Как установить?
0. `git clone https://github.com/wtfthefirefox/sync-recording.git`
1. `sudo su`
2. `sh <(curl -s https://cdn.shinobi.video/installers/shinobi-install.sh)`
3. `pip install -r requirements.txt`

# Первоначальная настройка shinobi
TBA

# Как запускать после установки?
0. Запускать нужно все в отедльных папках, что бы логи были у каждого из сервисов.
1. Запускаем сервер `nohup python main.py -p port &`, где port - это порт на котором будет работать сервер.
2. Если мы уже все установили и перезапускали сервер, то нужно еще сделать `nohup sh <(curl -s https://cdn.shinobi.video/installers/shinobi-install.sh) &`.

# Как посмотреть логи?
Логи доступны в файле `nohup.out`. Наиболее простой способ просмотра логов - это использование утилиты less - `less nohup.out`.

# Как добавить новые камеры?
Для этого есть тулза `tools/load_cameras.py`. Ее настройки и параметры можно посмотреть написав так: `python load_cameras.py -h`.

# Running tests steps:
1. Add cameras using load_camera.py
2. Configure address, api_key, group_key and rooms variables in recording.py using values from your ShinobiCCTV server.
3. Customize main() function. You can configure time recording, room and some video joining params.


# How to start the server?
0. If you want to get all availiable options, run `python main.py -h`
1. Run `python main.py`,
