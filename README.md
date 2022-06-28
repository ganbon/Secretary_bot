# Secretary_bot
秘書チャットアプリのコードです

## 開発環境
- Windows10
- anaconda-4.11.0

## 仮想環境配布
conda_env の`conda_env.yml`に Anaconda 環境構築ファイルを配布しています。
構築手順は以下のとおりです  
- conda_envにある`edit_envpath.py`を実行
- コマンド`conda env create -f conda_env.yml`を実行

## ファイル、ディレクトリ説明
- set_up.py…附属アプリの実装
- app.py…Flask サーバの設定
- com.py…附属アプリのシステム
- weather_data…天気予報のための地域コード
- text_file…web ページのテキスト化の保存先と豆知識ファイル
- templates…HTML ファイル
- static…CSS、js ファイル
- image…画像データ
- csv_data…CSV ファイル
- system…チャットアプリのシステム

## 実装している機能
- 予定の管理
- 天気予報
- 通知機能
- web ページ抽出
- 文章要約[^1]
- 感情表現による返信[^1]
- メッセージ読み上げ機能[^2]
- 豆知識機能
- 曜日提示機能
- 通知機能
- Twitter トレンド提示機能[^3]
- Moodle の予定取得(学生限定)
- Google Calendar との連携[^4]  
  各機能の詳しい使用方法は「explanation.md」を御覧ください。また各種必要なライブラリは各自でインストールお願いします。

[^1]:
    この機能はこちらのリポジトリのプログラムでモデルの生成実装が必要です。  
    文章要約(https://github.com/ganbon/summary_model)  
    感情表現(https://github.com/ganbon/emotion_model)

[^2]: [Softalk](http://www.vector.co.jp/soft/winnt/art/se412443.html)というソフトのインストールが必要です。
[^3]: TwitterAPI の登録が必要です。
[^4]: Google Calendar API の設定が必要です。

## 機能に参照したもの一覧
- Softalk:(http://www.vector.co.jp/soft/winnt/art/se412443.html)
- 天気予報 API（livedoor 天気互換）:(https://weather.tsukumijima.net/)
- 豆知識の収集元:(https://hq-improve.com/zatsugaku/)
- アイコン:(http://flat-icon-design.com/)

## Author
Twitter:(https://twitter.com/g75hca)
