# Fortnite API Auto Update Bot 🔄

このリポジトリは、Fortnite関連APIのレスポンスの変化を自動的に検出し、差分ファイルを作成してGitHubへ自動プッシュするBotを構成しています。

## 🛠 主な機能

- 指定された複数のAPIエンドポイントのレスポンスを定期的に取得
- 最新のスナップショットと比較して差分を検出
- 差分がある場合は `.json` または `.ini.diff` ファイルとして保存
- 自動でGitにコミット & GitHubにプッシュ
- 差分がなければ「変化なし」としてスキップ
- JSONでない形式（例：`.ini`）も対応（ファイル保存+diff出力）

## 📂 ディレクトリ構成

```bash
.
├── .github/
│   └── workflows/
│       └── main.yml       # GitHub Actions用のワークフロー設定
├── main.py                # メインスクリプト（API取得と差分検出）
├── requirements.txt       # 必要なPythonパッケージ
├── *.json                 # 最新APIレスポンスのスナップショットファイル
├── *.ini.diff             # .ini形式の差分ファイル（オプション）
└── README.md              # このファイル


## ⚙️ 使用技術

- Python 3
- GitHub Actions
- requests
- difflib
- JSON / テキスト比較

## 🔄 動作フロー

1. `main.py` をGitHub Actionsで定期実行
2. 各APIからデータ取得
3. 前回スナップショットとの比較
4. 差分ありなら `.json` / `.diff` を保存
5. 自動Git操作（`add`, `commit`, `pull --rebase`, `push`）

## 📝 設定ファイル例（main.py内）

```python
API_TARGETS = [
    {
        "name": "DefaultGame",
        "url": "https://example.com/api/v1/gameconfig",
        "snapshot_file": "DefaultGame.ini",
        "latest_file": "DefaultGame_latest.ini"
    },
    {
        "name": "cloudstorage",
        "url": "https://example.com/api/v2/cloudstorage",
        "snapshot_file": "cloudstorage.json",
        "latest_file": "cloudstorage_latest.json"
    }
]

🤖 開発・管理者
制作 / [@Leakplayer](https://x.com/LeakPlayer)

何か問題があれば [Issue](https://github.com/Fortniteleakjp/apiupdate/issues) からご報告ください。
