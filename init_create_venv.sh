#!/bin/bash
# Python 3.10.18 を指定して仮想環境を作成
python3.10 -m venv venv

# 仮想環境を有効化
source venv/bin/activate

# requirements.txt をもとにライブラリをインストール
pip install -r requirements.txt