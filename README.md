# Secretary_bot
秘書チャットアプリのコードです

## ファイル、ディレクトリ説明
- set_up.py…附属アプリの実装
- app.py…Flaskサーバの設定
- com.py…附属アプリのシステム
- weather_data…天気予報のための地域コード
- text_file…webページのテキスト化の保存先と豆知識ファイル
- templates…CSVファイル
- system…チャットアプリのシステム

## 実装している機能
- 予定の管理
- 天気予報
- 通知機能
- webページ抽出
- 文章要約[^1]
- 感情表現による返信[^1]
- メッセージ読み上げ機能[^2]
- 豆知識機能
- 曜日提示機能
- 通知機能
- Twitterトレンド提示機能[^3]  
各機能の詳しい使用方法は「使い方.txt」を御覧ください。
また各種必要なライブラリは各自でインストールお願いします。

[^1]:この機能はこちらのリポジトリのプログラムでモデルの生成実装が必要です。   
文章要約(https://github.com/ganbon/summary_model)   
感情表現(https://github.com/ganbon/emotion_model)  
[^2]:[Softalk](http://www.vector.co.jp/soft/winnt/art/se412443.html)というソフトのインストールが必要です。
[^3]:TwitterAPIの登録が必要です。

## 機能に参照したもの一覧
- Softalk:(http://www.vector.co.jp/soft/winnt/art/se412443.html)
- 天気予報 API（livedoor 天気互換）:(https://weather.tsukumijima.net/)
- 豆知識の収集元:(https://hq-improve.com/zatsugaku/) 
- アイコン:(http://flat-icon-design.com/)
## Author
Twitter:(https://twitter.com/g75hca)