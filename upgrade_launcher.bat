cd /d "%~dp0"

IF NOT EXIST "wechatocr\wechatocr.exe" (
    tar -xf wechatocr.zip
)

call upgrade.bat

call wechatocr.bat
