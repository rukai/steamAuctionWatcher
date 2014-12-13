@ECHO OFF
:loop
    cls
    python auctionWatcher.py
    timeout /t 20
goto loop
