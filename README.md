# koyodule

博衣こよりのフリーチャット枠（こよじゅーる）のサムネイルを定期的に監視し、変更があれば Discord に通知するツールです。

## 仕組み

1. GitHub Actions が定期的に起動
2. YouTube のサムネイル URL から画像を取得し、前回のハッシュと比較
3. 変更があれば画像付きで Discord に通知

## 必要な Secrets

| 名前 | 内容 |
|---|---|
| `YOUTUBE_VIDEO_ID` | 監視する動画の ID |
| `DISCORD_WEBHOOK_URL` | 通知先の Discord Webhook URL |

## 使用技術

- Python
- GitHub Actions
- Discord Webhook
