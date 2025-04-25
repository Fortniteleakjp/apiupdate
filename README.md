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
