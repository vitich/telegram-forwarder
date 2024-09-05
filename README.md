# telegram-forwarder
The script checks the last message on the public channel every 10 seconds and forwards the last message to the private channel or group.

1) Download this repo.<br />
```
git clone https://github.com/vitich/telegram-forwarder.git
cd telegram-forwarder
```
3) Get your api_id and api_hash on https://my.telegram.org/apps<br />

4) Modify ENVs in Dockerfile.<br />

5) Build the project.<br />
```
docker build -t telegram-forwarder .
```
6) Run it in interactive mode for the first time.<br />
```
docker run -it -v $(pwd)/session:/app/session --restart always --name telegram-forwarder telegram-forwarder
```
It will ask your telegram account phone number.<br />
Then enter the code from telegram and your password.<br />

7) Next time you can start/stop the container <br />
```
docker start telegram-forwarder
```
8) You can look in the log like this
```
docker logs -f telegram-forwarder
```
