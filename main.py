import requests
import json
import hashlib
import os
from datetime import datetime

# 監視対象APIとスナップショットファイルの対応リスト
API_TARGETS = [
    {
        "name": "ASIA_Windows",
        "url": "https://tournamentapi.onrender.com/api/tournamentlist?region=ASIA&platform=Windows",
        "snapshot_file": "ASIA_event_Windows.json",
        "latest_file": "ASIA_event_Windows_latest.json"
    },
    {
        "name": "NAE_Windows",
        "url": "https://tournamentapi.onrender.com/api/tournamentlist?region=NAE&platform=Windows",
        "snapshot_file": "NAE_event_Windows.json",
        "latest_file": "NAE_event_Windows_latest.json"
    },
    {
        "name": "NAC_Windows",
        "url": "https://tournamentapi.onrender.com/api/tournamentlist?region=NAC&platform=Windows",
        "snapshot_file": "NAC_event_Windows.json",
        "latest_file": "NAC_event_Windows_latest.json"
    },
    {
        "name": "NAW_Windows",
        "url": "https://tournamentapi.onrender.com/api/tournamentlist?region=NAW&platform=Windows",
        "snapshot_file": "NAW_event_Windows.json",
        "latest_file": "NAW_event_Windows_latest.json"
    },
    {
        "name": "OCE_Windows",
        "url": "https://tournamentapi.onrender.com/api/tournamentlist?region=OCE&platform=Windows",
        "snapshot_file": "OCE_event_Windows.json",
        "latest_file": "OCE_event_Windows_latest.json"
    },
    {
        "name": "ME_Windows",
        "url": "https://tournamentapi.onrender.com/api/tournamentlist?region=ME&platform=Windows",
        "snapshot_file": "ME_event_Windows.json",
        "latest_file": "ME_event_Windows_latest.json"
    },
    {
        "name": "EU_Windows",
        "url": "https://tournamentapi.onrender.com/api/tournamentlist?region=EU&platform=Windows",
        "snapshot_file": "EU_event_Windows.json",
        "latest_file": "EU_event_Windows_latest.json"
    },
    {
        "name": "BR_Windows",
        "url": "https://tournamentapi.onrender.com/api/tournamentlist?region=BR&platform=Windows",
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
        "url": "https://fljpapi.onrender.com/api/v2/cloudstorage/a22d837b6a2b46349421259c0a5411bf",
        "snapshot_file": "DefaultGame.ini.diff",
        "latest_file": "DefaultGame_latest.ini.diff"
    },
    {
        "name": "cloudstorage",
        "url": "https://fljpapi.onrender.com/api/v2/cloudstorage",
        "snapshot_file": "cloudstorage.json",
        "latest_file": "cloudstorage_latest.json"
    },
]

def fetch_api_data(url, name=None):
    print(f"🔄 APIデータを取得中... ({name or url})")
    response = requests.get(url)
    print(f"📥 ステータスコード: {response.status_code}")
    print(f"📥 レスポンステキスト: {response.text[:200]}...")
    response.raise_for_status()
    if name and name.lower().endswith(".ini") or "DefaultGame" in (name or ""):
        return response.text  # INI形式として文字列をそのまま返す
    try:
        return response.json()
    except json.JSONDecodeError as e:
        print(f"❌ JSONデコード失敗: {e}")
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
        json.dump(data, f, indent=2, ensure_ascii=False)

def hash_data(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def main():
    changed = False
    try:
        for target in API_TARGETS:
            current = fetch_api_data(target["url"])
            previous = load_snapshot(target["snapshot_file"])

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
