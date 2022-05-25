import datetime, re
import googleapiclient.discovery
import google.auth


# ①Google APIの準備をする
SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id = 'hezhenyanben@gmail.com'
# Googleの認証情報をファイルから読み込む
gapi_creds = google.auth.load_credentials_from_file('..\key\manifest-bit-350107-733e47cde6e6.json', SCOPES)[0]
# APIと対話するためのResourceオブジェクトを構築する
service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)

year=2022
month=6
day=2
# 追加するスケジュールの情報を設定
event= {
    # 予定のタイトル
    'summary': 'テスト',
    # 予定の開始時刻(ISOフォーマットで指定)
    'start': {
        'date': f'{year}-{month}-{day}',
        'timeZone': 'Japan'
    },
    # 予定の終了時刻(ISOフォーマットで指定)
    'end': {
        'date': f'{year}-{month}-{day}',
        'timeZone': 'Japan'
    },
}

# 予定を追加する
event = service.events().insert(calendarId = calendar_id, body = event).execute()