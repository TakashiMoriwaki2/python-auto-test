import os
import requests

# GitHub Secretsから認証情報を取得
WP_USER = os.environ.get("WP_USER")
WP_APP_PASS = os.environ.get("WP_APP_PASS")

# 送信先のURL（yyeventsエンドポイント）
API_URL = "https://entre-news.jp/wp-json/wp/v2/yyevents"

print("=== WordPress REST API 接続テスト ===")
print(f"ユーザー名設定: {'OK' if WP_USER else 'NG'}")
print(f"パスワード設定: {'OK' if WP_APP_PASS else 'NG'}")

# テスト用のデータ（安全のため「下書き」として作成）
payload = {
    "title": "【テスト】APIからの自動投稿テスト",
    "status": "draft",
    "content": "これはGitHub Actionsのテスト投稿です。確認できたらゴミ箱に入れてOKです。"
}

try:
    print(f"\n{API_URL} にデータを送信しています...")
    # APIへPOSTリクエストを送信
    response = requests.post(
        API_URL,
        auth=(WP_USER, WP_APP_PASS),
        json=payload,
        timeout=10
    )

    # 結果の判定
    if response.status_code == 201:
        print("✅ 大成功！WordPressにテスト投稿（下書き）が作成されました。")
        res_data = response.json()
        print(f"投稿ID: {res_data.get('id')}")
    else:
        print(f"❌ 失敗しました。ステータスコード: {response.status_code}")
        print(f"エラー詳細: {response.text}")

except Exception as e:
    print(f"⚠️ 予期せぬエラーが発生しました: {e}")
