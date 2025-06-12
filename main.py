import requests
import json
import hashlib
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# 監視対象APIとスナップショットファイルの対応リスト
API_TARGETS = [
    {
        "name": "ASIA_Windows",
        "url": os.getenv("URL_ASIA_WINDOWS"),
        "snapshot_file": "ASIA_event_Windows.json",
        "latest_file": "ASIA_event_Windows_latest.json"
    },
    {
        "name": "NAE_Windows",
        "url": os.getenv("URL_NAE_WINDOWS"),
        "snapshot_file": "NAE_event_Windows.json",
        "latest_file": "NAE_event_Windows_latest.json"
    },
    {
        "name": "NAC_Windows",
        "url": os.getenv("URL_NAC_WINDOWS"),
        "snapshot_file": "NAC_event_Windows.json",
        "latest_file": "NAC_event_Windows_latest.json"
    },
    {
        "name": "NAW_Windows",
        "url": os.getenv("URL_NAW_WINDOWS"),
        "snapshot_file": "NAW_event_Windows.json",
        "latest_file": "NAW_event_Windows_latest.json"
    },
    {
        "name": "OCE_Windows",
        "url": os.getenv("URL_OCE_WINDOWS"),
        "snapshot_file": "OCE_event_Windows.json",
        "latest_file": "OCE_event_Windows_latest.json"
    },
    {
        "name": "ME_Windows",
        "url": os.getenv("URL_ME_WINDOWS"),
        "snapshot_file": "ME_event_Windows.json",
        "latest_file": "ME_event_Windows_latest.json"
    },
    {
        "name": "EU_Windows",
        "url": os.getenv("URL_EU_WINDOWS"),
        "snapshot_file": "EU_event_Windows.json",
        "latest_file": "EU_event_Windows_latest.json"
    },
    {
        "name": "BR_Windows",
        "url": os.getenv("URL_BR_WINDOWS"),
        "snapshot_file": "BR_event_Windows.json",
        "latest_file": "BR_event_Windows_latest.json"
    },
    {
        "name": "fortnite-game-ja",
        "url": "https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game?lang=ja",
        "snapshot_file": "fortnite-gameja.json",
        "latest_file": "fortnite-gameja_latest.json"
    },
    {
        "name": "fortnite-game-en",
        "url": "https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game?lang=en",
        "snapshot_file": "fortnite-gameen.json",
        "latest_file": "fortnite-gameen_latest.json"
    },
    {
        "name": "DefaultGame",
        "url": os.getenv("URL_DEFAULTGAME"),
        "snapshot_file": "DefaultGame.ini.diff",
        "latest_file": "DefaultGame_latest.ini.diff"
    },
    {
        "name": "ASIA_PS5",
        "url": os.getenv("URL_ASIA_PS5"),
        "snapshot_file": "ASIA_event_PS5.json",
        "latest_file": "ASIA_event_PS5_latest.json"
    },
    {
        "name": "NAE_PS5",
        "url": os.getenv("URL_NAE_PS5"),
        "snapshot_file": "NAE_event_PS5.json",
        "latest_file": "NAE_event_PS5_latest.json"
    },
    {
        "name": "cloudstorage",
        "url": os.getenv("URL_CLOUDSTORAGE"),
        "snapshot_file": "cloudstorage.json",
        "latest_file": "cloudstorage_latest.json"
    },
]

def fetch_api_data(url, name=None, is_json=True):
    print(f"🔄 APIデータを取得中... ({name or url})")
    response = requests.get(url)
    print(f"📥 ステータスコード: {response.status_code}")
    print(f"📥 レスポンステキスト: {response.text[:200]}...")

    if not response.ok:
        print(f"❌ リクエスト失敗: {response.status_code}")
        return None

    try:
        if is_json:
            return response.json()
        else:
            return response.text
    except json.JSONDecodeError as e:
        print(f"❌ JSONデコード失敗: {e}")
        debug_file = f"{name or 'response'}_debug.txt"
        with open(debug_file, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"📁 デバッグ用に {debug_file} に保存しました")
        return None

def load_snapshot(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        if file_path.endswith(".json"):
            return json.load(f)
        else:
            return f.read()  # iniファイルなどは文字列で読み込む

def save_snapshot(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        if file_path.endswith(".json"):
            json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            f.write(data)

def hash_data(data):
    if isinstance(data, dict) or isinstance(data, list):
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
    elif isinstance(data, str):
        return hashlib.sha256(data.encode()).hexdigest()
    else:
        return hashlib.sha256(str(data).encode()).hexdigest()

def main():
    changed = False
    try:
        for target in API_TARGETS:
            is_json = target["snapshot_file"].endswith(".json")
            current = fetch_api_data(target["url"], name=target["name"], is_json=is_json)
            previous = load_snapshot(target["snapshot_file"])
            if current is None:
                print(f"⚠️ {target['name']} の取得に失敗。スキップします。")
                continue
            if previous is None or hash_data(current) != hash_data(previous):
                print(f"✅ 差分あり: {target['name']} スナップショットを更新します。")
                save_snapshot(target["snapshot_file"], current)
                save_snapshot(target["latest_file"], current)
                changed = True
            else:
                print(f"🟢 {target['name']} に変化なし。")

        if changed:
            print("🔧 Git設定を更新中...")
            os.system("git config user.name 'github-actions'")
            os.system("git config user.email 'github-actions@github.com'")
            os.system("git add *.json *.diff || echo '追加対象なし'")
            os.system(f"git commit -m \"🔄 API更新: {datetime.now().isoformat()}\" || echo 'コミット対象なし'")

            print("🔃 リモートとリベース...")
            os.system("git stash || echo 'stash失敗'")
            os.system("git pull --rebase || echo '⚠️ リベース失敗'")
            os.system("git stash pop || echo 'stash戻し失敗'")

            print("🚀 プッシュ中...")
            os.system("git push || echo '⚠️ プッシュ失敗'")
        else:
            print("✅ すべて最新です。更新なし。")

    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    main()
