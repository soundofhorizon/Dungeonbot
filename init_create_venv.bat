REM 仮想環境を作成（フォルダ名: venv）
py -3.10.18 -m venv venv

REM 仮想環境を有効化
call venv\Scripts\activate

REM requirements.txt に記載されたライブラリをインストール
pip install -r requirements.txt