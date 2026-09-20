# かいぞく クイズ

ファンが作った非公式の海賊まんがクイズ(娘さん向け・675問)。集英社および原作者とは関係ありません。**iPhone 6s でも動くよう、Streamlit ではなく素の HTML+JS+CSS** で作り直し済み。

## 起動方法

```bash
cd ~/AI準備室/家族/onepiece_quiz_app
python3 -m http.server 8000
```

スマホから:同じ Wi-Fi で

```
http://<このPCのIPアドレス>:8000
```

を開く。IP は `ipconfig getifaddr en0`(Mac)で確認できます。

## ホーム画面に追加(iPhone)

Safari で開く → 共有 → 「ホーム画面に追加」 → アプリのように起動できる(PWA)。

## 特徴

- 675 問(かんたん / ふつう / むずかしい × 15 ジャンル)
- ポップアニメ調デザイン(コミック風アウトライン+ハーフトーン)
- 正解で「ドン!!」 不正解で「ガーン!!」
- BGM なし、効果音は WebAudio で合成(外部ファイル不要)
- ベストスコア保存(localStorage)
- オフライン対応(Service Worker)
- iPhone 6s(iOS 15)で動作確認

## ファイル構成

```
onepiece_quiz_app/
├── index.html          画面構造
├── style.css           ポップアニメ調デザイン
├── quiz.js             出題・採点・称号
├── app.js              画面遷移とゲームフロー
├── storage.js          ベストスコア・設定保存
├── audio.js            WebAudio 効果音
├── questions.json      675問データ
├── manifest.json       PWA 設定
├── service-worker.js   オフラインキャッシュ
└── icons/              アイコン(SVG)
```

## 問題追加

`questions.json` に同じ形式で追記するだけ。

```json
{
  "difficulty": "ふつう",
  "genre": "キャラクター",
  "question": "...",
  "choices": ["A", "B", "C", "D"],
  "answer": "B",
  "explanation": "..."
}
```

## 旧版

`app.py` は Streamlit 版。iPhone 6s では動かないため非推奨。残してあるだけ。
