import requests
import json
import hashlib
import os
from datetime import datetime

API_URL = "https://tournamentapi.onrender.com/api/tournamentlist?region=ASIA&platform=Windows"  # ← 監視対象のAPI URL
SNAPSHOT_FILE = "ASIA_event_Windows.json"

def fetch_api_data():
    print("🔄 APIデータを取得中...")
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def load_snapshot():
    if not os.path.exists(SNAPSHOT_FILE):
        return None
    with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_snapshot(data):
    with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def hash_data(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def main():
    try:
        current = fetch_api_data()
        previous = load_snapshot()

        if previous is None or hash_data(current) != hash_data(previous):
            print("✅ 差分あり: スナップショットを更新します。")
            save_snapshot(current)
            with open("ASIA_event_Windows_latest.json", "w", encoding="utf-8") as f:
                json.dump(current, f, indent=2, ensure_ascii=False)

            os.system("git config user.name 'github-actions'")
            os.system("git config user.email 'github-actions@github.com'")
            os.system("git add latest.json api_snapshot.json")
            os.system(f"git commit -m \"🔄 API更新: {datetime.now().isoformat()}\"")
            os.system("git push")
        else:
            print("🟢 APIに変化なし。")
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    main()
