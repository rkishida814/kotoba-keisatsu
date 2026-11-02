#!/usr/bin/env python3
"""言葉警察の lint。checklist.md の型のうち、機械的に拾える候補だけを出す。

候補は手がかりで、違反の判定ではない。判定は checklist.md の基準で読んで行う。
使い方: python3 keisatsu_lint.py 対象ファイル
"""
import re
import sys
import unicodedata

# (型, 説明, 正規表現)。checklist.md に型を足したら、拾える形はここにも足す。
RULES = [
    ("K1", "日本語として成り立たない語の組み合わせ",
     re.compile(r"重なりながら進")),
    ("K2", "読み手が見ていない会話への言及",
     re.compile(r"という(疑問|質問|問い|指摘|見立て|理解|意見|感覚)"
                r"|答えはここにある|ユーザー(の|は|が)|セッションで|先ほどの|上の議論|前述の議論")),
    ("K3", "定義のない造語・抽象語の候補",
     re.compile(r"上乗せ|に特有の(反応|作用)|としての[^\s、。]{1,8}$")),
    ("K4", "前提を書かずにつなぐ接続語・指示語",
     re.compile(r"^(したがって|つまり|このため|そのため|ゆえに|すなわち)、?"
                r"|のは(この|その)ためである|のは(この|その)ためだ")),
    ("K5", "かぎ括弧に入れた比喩・言い換え",
     re.compile(r"「[ぁ-んァ-ヶ一-龥]{1,3}(る|う|く|ぐ|す|つ|ぬ|ぶ|む)」")),
    ("K6", "主語や場面のない、かぎ括弧の中の断片",
     re.compile(r"「[^」]{1,15}」とは")),
    ("K8", "本文に付けた確度の印",
     re.compile(r"［(確立|有力|未確定)[^］]*］")),
]

# K7 は表の見出し行と節の見出しだけに当てる
K7 = re.compile(r"どうやって|どのように|なぜ|何が|[^。]か$")


def split_sentences(line):
    return [s for s in re.split(r"(?<=。)", line) if s.strip()]


def main(path):
    text = unicodedata.normalize("NFC", open(path, encoding="utf-8").read())
    lines = text.splitlines()
    hits = []
    in_code = False
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line.strip():
            continue
        body = re.sub(r"^\s*(#+|[-*]|\d+\.)\s*", "", line).replace("**", "")
        is_heading = line.lstrip().startswith("#")
        is_table_head = (line.startswith("|") and i < len(lines)
                         and re.match(r"^\|[\s:|-]+\|$", lines[i]))
        if is_heading or is_table_head:
            cells = [c.strip() for c in body.strip("|").split("|")] if is_table_head else [body.strip()]
            for c in cells:
                if K7.search(c):
                    hits.append((i, "K7", "表・見出しの口語の問い", c))
        for s in split_sentences(body):
            s = s.strip()
            for kind, desc, rx in RULES:
                if rx.search(s):
                    hits.append((i, kind, desc, s))
    print(f"言葉警察の lint: 候補 {len(hits)} 件（手がかりであり、違反の判定ではない）")
    for i, kind, desc, s in hits:
        print(f"L{i} [{kind}] {desc}\n  > {s}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("使い方: python3 keisatsu_lint.py 対象ファイル")
    main(sys.argv[1])
