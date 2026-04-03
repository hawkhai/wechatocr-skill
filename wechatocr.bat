cd /d "%~dp0"

cd wechatocr\serv\runtime
start infserv64.exe
timeout /t 1 >nul

cd ..\..\..
wechatocr\wechatocr.exe %*
