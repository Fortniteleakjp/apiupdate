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
]

def fetch_api_data(url):
    print(f"🔄 APIデータを取得中... ({url})")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def load_snapshot(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

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
            os.system("git config user.name 'github-actions'")
            os.system("git config user.email 'github-actions@github.com'")
            os.system("git add *.json")
            os.system(f"git commit -m \"🔄 API更新: {datetime.now().isoformat()}\" || echo 'コミット対象なし'")
            os.system("git push || echo 'プッシュ対象なし'")
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    main()
