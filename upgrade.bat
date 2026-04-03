cd /d "%~dp0"

gitbigfileftp.exe /DownloadRemote /NoTipInfo /NoCheckFile .
IF %ERRORLEVEL% EQU 0 (
    echo 程序成功执行，返回值为 0
) ELSE (
    echo 程序执行出现问题，返回值为 %ERRORLEVEL%
    timeout /T 5 /NOBREAK >nul
    gitbigfileftp.exe /DownloadRemote /NoTipInfo /NoCheckFile .
)
