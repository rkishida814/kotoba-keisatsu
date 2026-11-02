# 言葉警察（kotoba-keisatsu）

AI が書いた日本語の文書を、「この文書だけを渡された読み手に分かるか」で一文ずつ調べ、直す Claude Code のスキルです。読み手が見ていない会話への言及、文書の中で定義していない造語、前提を書かずにつなぐ「したがって」、かぎ括弧に入れた比喩、日本語として成り立たない語の組み合わせなどを見つけます。

推敲スキルの [yomiyasu](https://github.com/nanaism/yomiyasu) は、「元にない情報を足さない」を最優先にしています。そのため、こうした箇所を見つけても、直すには情報を足す必要があるので手を付けません。言葉警察はその前の段で、出典（文書の別の節、文書を作ったときの資料、原典）で確かめた情報だけを補って直し、最後に yomiyasu の検査をかけます。

## ファイル

| ファイル | 内容 |
|---|---|
| `SKILL.md` | スキルの手順（対象を決める → 読み手テスト → 直す → yomiyasu で仕上げる → 報告） |
| `checklist.md` | チェック項目（K1〜）。利用者の指摘を一般化して追記していく |
| `scripts/keisatsu_lint.py` | checklist の型のうち、機械的に拾える候補を出す lint |

## 入れ方

```bash
ln -s ~/Documents/programs/kotoba-keisatsu ~/.claude/skills/kotoba-keisatsu
```

Claude Code で「言葉警察でチェックして」と頼むか、`/kotoba-keisatsu ファイル名` と打つと動きます。yomiyasu のプラグインが入っていることが前提です。

lint だけを使うときは、次のように実行します。

```bash
python3 scripts/keisatsu_lint.py 対象ファイル.md
```
