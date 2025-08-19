@echo off
REM 仮想環境を有効化
call %~dp0venv\Scripts\activate

REM bot.py を起動
python %~dp0bot.py