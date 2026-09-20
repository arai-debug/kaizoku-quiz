import random
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="ワンピース クイズアプリ",
    page_icon="🏴‍☠️",
    layout="wide",
)

QUESTION_COUNT = 100
LIGHTWEIGHT_MODE = True


QUESTION_BANK = [
    {
        "difficulty": "かんたん",
        "genre": "悪魔の実",
        "question": "ルフィが食べた悪魔の実の名前は？",
        "choices": ["ゴムゴムの実", "メラメラの実", "オペオペの実", "ヒトヒトの実"],
        "answer": "ゴムゴムの実",
        "explanation": "物語の始まりでルフィが食べた実として有名だね。",
        "image": "gomu_gomu.png",
    },
    {
        "difficulty": "かんたん",
        "genre": "海賊団",
        "question": "麦わらの一味の剣士はだれ？",
        "choices": ["サンジ", "ゾロ", "ウソップ", "フランキー"],
        "answer": "ゾロ",
        "explanation": "三刀流を使うロロノア・ゾロが剣士だよ。",
    },
    {
        "difficulty": "かんたん",
        "genre": "海賊団",
        "question": "ナミの得意なことは？",
        "choices": ["料理", "航海", "医療", "船大工"],
        "answer": "航海",
        "explanation": "ナミは麦わらの一味の航海士として海を導いているよ。",
    },
    {
        "difficulty": "かんたん",
        "genre": "海賊団",
        "question": "サンジが主に担当している役割は？",
        "choices": ["船医", "考古学者", "コック", "音楽家"],
        "answer": "コック",
        "explanation": "サンジは料理担当。戦いでも足技がかっこいいね。",
    },
    {
        "difficulty": "かんたん",
        "genre": "海賊団",
        "question": "チョッパーの職業は？",
        "choices": ["船長", "船医", "操舵手", "狙撃手"],
        "answer": "船医",
        "explanation": "チョッパーは仲間たちを治してくれる大事な船医。",
    },
    {
        "difficulty": "かんたん",
        "genre": "キャラクター",
        "question": "ルフィの夢は何？",
        "choices": ["海軍大将になる", "世界一の剣豪になる", "海賊王になる", "宝石王になる"],
        "answer": "海賊王になる",
        "explanation": "ルフィはずっと海賊王を目指して旅をしているよ。",
    },
    {
        "difficulty": "かんたん",
        "genre": "海賊団",
        "question": "麦わらの一味の船大工はだれ？",
        "choices": ["ブルック", "ジンベエ", "フランキー", "ロビン"],
        "answer": "フランキー",
        "explanation": "フランキーはサウザンドサニー号を作った船大工だよ。",
    },
    {
        "difficulty": "かんたん",
        "genre": "セリフ・表現",
        "question": "ブルックがよく使うあいさつや決めぜりふに近いものは？",
        "choices": ["スーパー！", "ヨホホホ！", "見聞色！", "失礼する！"],
        "answer": "ヨホホホ！",
        "explanation": "ブルックらしい笑い声としておなじみだね。",
    },
    {
        "difficulty": "かんたん",
        "genre": "海賊団",
        "question": "ロビンが得意としている学問は？",
        "choices": ["天文学", "考古学", "建築学", "医学"],
        "answer": "考古学",
        "explanation": "ロビンは歴史の本文を読み解く考古学者だよ。",
    },
    {
        "difficulty": "かんたん",
        "genre": "海賊団",
        "question": "ウソップの戦い方としていちばん近いのは？",
        "choices": ["剣術", "狙撃", "相撲", "魚人空手"],
        "answer": "狙撃",
        "explanation": "ウソップは遠くからねらう狙撃手として活躍するよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "エピソード",
        "question": "アラバスタ王国の王女はだれ？",
        "choices": ["しらほし", "ビビ", "レベッカ", "プリン"],
        "answer": "ビビ",
        "explanation": "ネフェルタリ・ビビはアラバスタ編で大活躍したね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "悪魔の実",
        "question": "空島で神として君臨していた人物は？",
        "choices": ["エネル", "クロコダイル", "モリア", "シーザー"],
        "answer": "エネル",
        "explanation": "ゴロゴロの実の力を使う強敵だったよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "海賊団",
        "question": "ウォーターセブンで一味が新しい船を手に入れた後の船の名前は？",
        "choices": ["ゴーイングメリー号", "サウザンドサニー号", "レッドフォース号", "モビーディック号"],
        "answer": "サウザンドサニー号",
        "explanation": "フランキーたちの技術がつまった新しい船だよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "エピソード",
        "question": "エニエス・ロビーでロビンを取り戻すために一味が戦った組織は？",
        "choices": ["王下七武海", "CP9", "革命軍", "海軍本部科学班"],
        "answer": "CP9",
        "explanation": "CP9との戦いは名場面がたくさんあるね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "エピソード",
        "question": "頂上戦争でルフィが助けようとした義兄はだれ？",
        "choices": ["サボ", "エース", "シャンクス", "コビー"],
        "answer": "エース",
        "explanation": "ポートガス・D・エースを救うためにルフィは全力で進んだよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "エピソード",
        "question": "魚人島で古代兵器ポセイドンの力を持つのはだれ？",
        "choices": ["ハンコック", "しらほし", "たしぎ", "コアラ"],
        "answer": "しらほし",
        "explanation": "しらほし姫には特別な力があることが明かされたね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "エピソード",
        "question": "ドレスローザでルフィが共闘した片足の剣闘士の正体は？",
        "choices": ["キュロス", "バルトロメオ", "キャベンディッシュ", "イデオ"],
        "answer": "キュロス",
        "explanation": "レベッカの父であり、王国のために戦っていたよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "海賊団",
        "question": "ホールケーキアイランド編でサンジの家族が属する一族は？",
        "choices": ["ネフェルタリ家", "ヴィンスモーク家", "ドンキホーテ家", "光月家"],
        "answer": "ヴィンスモーク家",
        "explanation": "ジェルマ66を率いるヴィンスモーク家との関係が描かれたね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "エピソード",
        "question": "ワノ国でルフィたちが力を合わせて倒した四皇は二人。カイドウともう一人は？",
        "choices": ["ビッグ・マム", "シャンクス", "白ひげ", "バギー"],
        "answer": "ビッグ・マム",
        "explanation": "ワノ国編は大きな節目になった戦いだったよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "キャラクター",
        "question": "ルフィ、エース、サボの三人の関係として正しいのは？",
        "choices": ["実の兄弟", "海軍の同期", "義兄弟", "同じ船の船員"],
        "answer": "義兄弟",
        "explanation": "三人は杯を交わして兄弟のちぎりを結んだね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "エピソード",
        "question": "ポーネグリフを読める麦わらの一味のメンバーはだれ？",
        "choices": ["ナミ", "ロビン", "チョッパー", "ジンベエ"],
        "answer": "ロビン",
        "explanation": "歴史の本文を読み解けるロビンの存在はとても重要だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "ゾロが幼いころから目標としていた幼なじみの名前は？",
        "choices": ["ノジコ", "くいな", "たしぎ", "ひな"],
        "answer": "くいな",
        "explanation": "くいなとの約束が、世界一の剣豪を目指す原点だね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "エピソード",
        "question": "ルフィが修行した島の名前として正しいのは？",
        "choices": ["女ヶ島", "ルスカイナ", "パンクハザード", "ゾウ"],
        "answer": "ルスカイナ",
        "explanation": "レイリーとともに覇気を学んだ場所だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "ローのフルネームは？",
        "choices": ["トラファルガー・D・ワーテル・ロー", "ユースタス・D・キッド", "マーシャル・D・ティーチ", "モンキー・D・ドラゴン"],
        "answer": "トラファルガー・D・ワーテル・ロー",
        "explanation": "ワノ国やドレスローザでも活躍した人気キャラだね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "海賊団",
        "question": "光月おでんがかつて乗った海賊船の組み合わせとして正しいのは？",
        "choices": ["白ひげ海賊団とロジャー海賊団", "百獣海賊団と赤髪海賊団", "キッド海賊団とハートの海賊団", "バギー海賊団と黒ひげ海賊団"],
        "answer": "白ひげ海賊団とロジャー海賊団",
        "explanation": "おでんは伝説級の二つの海賊団に関わっていたよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "エピソード",
        "question": "しらほし姫が会話できる特別な存在は？",
        "choices": ["海王類", "ズニーシャ", "ニュース・クー", "島クジラ"],
        "answer": "海王類",
        "explanation": "それが古代兵器ポセイドンに関わる力なんだ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "エピソード",
        "question": "ルフィたちがワノ国に入る前に立ち寄った巨大な象の背中の国は？",
        "choices": ["エルバフ", "ゾウ", "パンクハザード", "スリラーバーク"],
        "answer": "ゾウ",
        "explanation": "ミンク族が暮らす不思議な場所だったね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "海賊団",
        "question": "バルトロメオが特に熱烈に応援している海賊団は？",
        "choices": ["赤髪海賊団", "麦わらの一味", "白ひげ海賊団", "ロジャー海賊団"],
        "answer": "麦わらの一味",
        "explanation": "バルトロメオは筋金入りの麦わらファンだよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "エピソード",
        "question": "ワノ国で将軍だった黒炭オロチが恐れていた光月家の印は？",
        "choices": ["三日月", "満月", "朝日", "星"],
        "answer": "三日月",
        "explanation": "反撃の合図として印が強く意識されていたね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "海賊団",
        "question": "麦わらの一味に正式加入した元王下七武海はだれ？",
        "choices": ["くま", "ジンベエ", "クロコダイル", "ドフラミンゴ"],
        "answer": "ジンベエ",
        "explanation": "頼れる操舵手として一味に加わったよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "セリフ・表現",
        "question": "ドラム島でヒルルクが残した有名なせりふとして正しいものは？",
        "choices": [
            "人の夢は終わらねェ！",
            "人はいつ死ぬと思う？",
            "この戦争を終わらせに来た！",
            "愛してくれてありがとう！",
        ],
        "answer": "人はいつ死ぬと思う？",
        "explanation": "ヒルルクの名場面としてとても印象に残るせりふだね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "悪魔の実",
        "question": "エースが食べた悪魔の実は？",
        "choices": ["メラメラの実", "スナスナの実", "マグマグの実", "ヒエヒエの実"],
        "answer": "メラメラの実",
        "explanation": "炎を操る能力で、エースを象徴する力だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "悪魔の実",
        "question": "ローの能力として正しい悪魔の実は？",
        "choices": ["イトイトの実", "オペオペの実", "ジキジキの実", "バラバラの実"],
        "answer": "オペオペの実",
        "explanation": "手術のように空間を扱える、とても特別な能力だね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "ロジャーが処刑された町の名前は？",
        "choices": ["シェルズタウン", "ローグタウン", "アルバーナ", "ナノハナ"],
        "answer": "ローグタウン",
        "explanation": "始まりと終わりの町として知られているよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "海賊王ゴール・D・ロジャーの船の名前は？",
        "choices": ["オーロ・ジャクソン号", "サウザンドサニー号", "モビーディック号", "レッドフォース号"],
        "answer": "オーロ・ジャクソン号",
        "explanation": "ロジャー海賊団の船として有名だね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "海賊団",
        "question": "白ひげ海賊団の船の名前は？",
        "choices": ["モビーディック号", "ノストラカステロ号", "ポーラータング号", "クイーン・ママ・シャンテ号"],
        "answer": "モビーディック号",
        "explanation": "白ひげ海賊団の象徴的な船だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "エピソード",
        "question": "空島で鐘を鳴らすことに深く関わる黄金の鐘は何を伝える象徴だった？",
        "choices": ["友情", "約束", "復讐", "王位継承"],
        "answer": "約束",
        "explanation": "カルガラとノーランドの物語につながる、とても大切な象徴だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "エピソード",
        "question": "スリラーバーク編でルフィの影を入れられたのはだれ？",
        "choices": ["オーズ", "リューマ", "アブサロム", "ペローナ"],
        "answer": "オーズ",
        "explanation": "巨大な体で暴れるオーズはとても強敵だったね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "革命軍のリーダーで、ルフィの父でもある人物は？",
        "choices": ["モンキー・D・ガープ", "モンキー・D・ドラゴン", "シルバーズ・レイリー", "センゴク"],
        "answer": "モンキー・D・ドラゴン",
        "explanation": "世界政府に対抗する革命軍を率いているよ。",
    },
]

QUESTION_BANK += [
    {
        "difficulty": "ふつう",
        "genre": "キャラクター",
        "question": "ルフィに麦わら帽子を預けた四皇はだれ？",
        "choices": ["白ひげ", "シャンクス", "カイドウ", "ビッグ・マム"],
        "answer": "シャンクス",
        "explanation": "ルフィが大切にしている麦わら帽子はシャンクスとの約束の証だよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "エピソード",
        "question": "アラバスタ編で敵として立ちはだかった秘密結社は？",
        "choices": ["CP9", "革命軍", "バロックワークス", "ジェルマ66"],
        "answer": "バロックワークス",
        "explanation": "クロコダイルが率いる秘密結社として登場したね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "悪魔の実",
        "question": "クロコダイルの悪魔の実は？",
        "choices": ["スナスナの実", "モクモクの実", "ドクドクの実", "メラメラの実"],
        "answer": "スナスナの実",
        "explanation": "砂を自在に操る自然系の能力だよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "キャラクター",
        "question": "しらほし姫の父はだれ？",
        "choices": ["ネプチューン", "オトヒメ", "ジャック", "フィッシャー・タイガー"],
        "answer": "ネプチューン",
        "explanation": "魚人島の王として娘たちを見守っているね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "海賊団",
        "question": "サボが所属している組織は？",
        "choices": ["海軍", "革命軍", "白ひげ海賊団", "九蛇海賊団"],
        "answer": "革命軍",
        "explanation": "サボは革命軍の重要人物として活躍しているよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "海賊団",
        "question": "ローが率いる海賊団は？",
        "choices": ["キッド海賊団", "ハートの海賊団", "ファイアタンク海賊団", "オンエア海賊団"],
        "answer": "ハートの海賊団",
        "explanation": "トラファルガー・ローはハートの海賊団の船長だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "悪魔の実",
        "question": "ユースタス・キッドの悪魔の実は？",
        "choices": ["ジキジキの実", "バラバラの実", "ガシャガシャの実", "キロキロの実"],
        "answer": "ジキジキの実",
        "explanation": "磁力を使った豪快な戦い方が印象的だね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "悪魔の実",
        "question": "ドフラミンゴの悪魔の実は？",
        "choices": ["バネバネの実", "イトイトの実", "ホビホビの実", "トントンの実"],
        "answer": "イトイトの実",
        "explanation": "糸を使って攻撃も操作もできる危険な能力だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "エースの実の父はだれ？",
        "choices": ["モンキー・D・ドラゴン", "エドワード・ニューゲート", "ゴール・D・ロジャー", "シルバーズ・レイリー"],
        "answer": "ゴール・D・ロジャー",
        "explanation": "海賊王の血を引いていることが物語で明かされたね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "キャラクター",
        "question": "ルフィの祖父はだれ？",
        "choices": ["センゴク", "ガープ", "レイリー", "スモーカー"],
        "answer": "ガープ",
        "explanation": "海軍の英雄として知られるモンキー・D・ガープだよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "キャラクター",
        "question": "頂上戦争のころの海軍元帥はだれ？",
        "choices": ["赤犬", "青キジ", "センゴク", "黄猿"],
        "answer": "センゴク",
        "explanation": "当時の海軍本部をまとめていた元帥だね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "エピソード",
        "question": "エニエス・ロビーで世界政府の旗を撃ち抜いたのはだれ？",
        "choices": ["ゾロ", "そげキング", "サンジ", "フランキー"],
        "answer": "そげキング",
        "explanation": "ロビンを取り戻す覚悟を示す名場面だったね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "キャラクター",
        "question": "ビビのフルネームに入る王家の名前は？",
        "choices": ["ドンキホーテ", "ネフェルタリ", "ヴィンスモーク", "シャーロット"],
        "answer": "ネフェルタリ",
        "explanation": "アラバスタ王国の王女として登場したね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "海賊団",
        "question": "ラブーンがずっと待ち続けていた海賊団は？",
        "choices": ["ロジャー海賊団", "ルンバー海賊団", "赤髪海賊団", "巨兵海賊団"],
        "answer": "ルンバー海賊団",
        "explanation": "ブルックと深くつながる大切な海賊団だよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "海賊団",
        "question": "ブルックが昔所属していた海賊団は？",
        "choices": ["ルンバー海賊団", "ハートの海賊団", "百獣海賊団", "キッド海賊団"],
        "answer": "ルンバー海賊団",
        "explanation": "ラブーンとの約束を果たそうとしていたね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "悪魔の実",
        "question": "ペローナの悪魔の実は？",
        "choices": ["ホロホロの実", "ホビホビの実", "ゴーストゴーストの実", "ユキユキの実"],
        "answer": "ホロホロの実",
        "explanation": "ネガティブホロウで相手の気力を下げる能力だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "悪魔の実",
        "question": "ゲッコー・モリアの悪魔の実は？",
        "choices": ["カゲカゲの実", "ヨミヨミの実", "ホロホロの実", "ドクドクの実"],
        "answer": "カゲカゲの実",
        "explanation": "影を奪って操る恐ろしい能力だったね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "Mr.2 ボン・クレーの本名は？",
        "choices": ["ギャルディーノ", "ベンサム", "ダズ・ボーネス", "ジェム"],
        "answer": "ベンサム",
        "explanation": "インペルダウンでも大活躍した人気キャラだよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "海賊団",
        "question": "CP9を率いていた司令官はだれ？",
        "choices": ["スパンダム", "スパンダイン", "ルッチ", "カク"],
        "answer": "スパンダム",
        "explanation": "エニエス・ロビー編で一味の前に立ちはだかったね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "悪魔の実",
        "question": "ロブ・ルッチの悪魔の実は？",
        "choices": ["ネコネコの実 モデル 豹", "イヌイヌの実 モデル 狼", "ウマウマの実", "ウシウシの実 モデル 麒麟"],
        "answer": "ネコネコの実 モデル 豹",
        "explanation": "豹の姿で圧倒的な強さを見せたね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "悪魔の実",
        "question": "カクの悪魔の実は？",
        "choices": ["ウシウシの実 モデル 麒麟", "ゾウゾウの実", "ネコネコの実 モデル 豹", "トリトリの実 モデル 隼"],
        "answer": "ウシウシの実 モデル 麒麟",
        "explanation": "キリンになった見た目とのギャップが印象的だったよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "エネルの故郷として知られる空島の名前は？",
        "choices": ["スカイピア", "ビルカ", "バルジモア", "ウェザリア"],
        "answer": "ビルカ",
        "explanation": "エネルの過去に関わる重要な地名だね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "キャラクター",
        "question": "ウォーターセブンの市長でもある人物はだれ？",
        "choices": ["パウリー", "アイスバーグ", "トム", "ガレーラ"],
        "answer": "アイスバーグ",
        "explanation": "ガレーラカンパニーとも深く関わっているよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "フランキーの本名は？",
        "choices": ["カティ・フラム", "アイスバーグ", "トム", "パウリー"],
        "answer": "カティ・フラム",
        "explanation": "本名が明かされる場面も印象的だったね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "エピソード",
        "question": "ニコ・ロビンの故郷として知られる島は？",
        "choices": ["オハラ", "ドラム島", "バナロ島", "シロップ村"],
        "answer": "オハラ",
        "explanation": "歴史研究で有名だった島として知られているよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "シルバーズ・レイリーの異名は？",
        "choices": ["冥王", "鬼人", "天夜叉", "海侠"],
        "answer": "冥王",
        "explanation": "ロジャー海賊団の副船長として伝説級の人物だね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "ジュラキュール・ミホークの異名は？",
        "choices": ["海賊狩り", "鷹の目", "白猟", "死の外科医"],
        "answer": "鷹の目",
        "explanation": "世界最強の剣士として知られるミホークらしい異名だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "白ひげの本名は？",
        "choices": ["シャーロット・リンリン", "エドワード・ニューゲート", "マーシャル・D・ティーチ", "カイドウ"],
        "answer": "エドワード・ニューゲート",
        "explanation": "四皇のひとりとして海を揺らした大海賊だね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "黒ひげの本名は？",
        "choices": ["マーシャル・D・ティーチ", "エドワード・ウィーブル", "シリュウ", "アバロ・ピサロ"],
        "answer": "マーシャル・D・ティーチ",
        "explanation": "世界を大きく動かす危険人物として存在感が大きいよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "エピソード",
        "question": "カイドウ撃破後、ワノ国の将軍になったのはだれ？",
        "choices": ["錦えもん", "モモの助", "ヤマト", "おでん"],
        "answer": "モモの助",
        "explanation": "光月家の意志を継ぎ、ワノ国を導く存在になったね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "光月おでんの妻の名前は？",
        "choices": ["日和", "トキ", "くれは", "おつる"],
        "answer": "トキ",
        "explanation": "時を超える力を持つ人物として物語の重要な鍵になったよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "赤鞘九人男で「狐火」の異名を持つのはだれ？",
        "choices": ["傳ジロー", "錦えもん", "河松", "イゾウ"],
        "answer": "錦えもん",
        "explanation": "炎を斬る剣技でも印象を残しているね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "巨大な象として知られるズニーシャの背中にある国は？",
        "choices": ["ワノ国", "ゾウ", "エルバフ", "魚人島"],
        "answer": "ゾウ",
        "explanation": "ミンク族が暮らす不思議な場所だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "悪魔の実",
        "question": "シャーロット・カタクリの悪魔の実は？",
        "choices": ["モチモチの実", "ペロペロの実", "ビスビスの実", "クリクリの実"],
        "answer": "モチモチの実",
        "explanation": "見聞色の強さとあわせてとても手強い相手だったね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "ビッグ・マムの本名は？",
        "choices": ["シャーロット・プリン", "シャーロット・リンリン", "シャーロット・スムージー", "シャーロット・モンドール"],
        "answer": "シャーロット・リンリン",
        "explanation": "四皇として新世界に君臨した海賊だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "ジェルマ66を率いるサンジの父はだれ？",
        "choices": ["イチジ", "ジャッジ", "ヨンジ", "ニジ"],
        "answer": "ジャッジ",
        "explanation": "ヴィンスモーク家の当主として描かれたね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "ヴィンスモーク家の長女はだれ？",
        "choices": ["プリン", "レイジュ", "ノジコ", "日和"],
        "answer": "レイジュ",
        "explanation": "サンジの姉として優しさも見せてくれたよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "ヴィンスモーク家の長男はだれ？",
        "choices": ["イチジ", "ニジ", "ヨンジ", "サンジ"],
        "answer": "イチジ",
        "explanation": "数字の並びで覚えると分かりやすいね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "ヴィンスモーク家の次男はだれ？",
        "choices": ["ニジ", "イチジ", "ヨンジ", "レイジュ"],
        "answer": "ニジ",
        "explanation": "サンジの兄弟のひとりとして登場したよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "ヴィンスモーク家の四男はだれ？",
        "choices": ["ヨンジ", "ニジ", "イチジ", "レイジュ"],
        "answer": "ヨンジ",
        "explanation": "兄弟の中でも見た目が印象に残りやすいね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "海賊団",
        "question": "ドレスローザ王国の王家の名前は？",
        "choices": ["リク王家", "ネフェルタリ家", "ヴィンスモーク家", "ドンキホーテ家"],
        "answer": "リク王家",
        "explanation": "ドレスローザ編の重要な背景として描かれたね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "エピソード",
        "question": "ドレスローザのコロシアムでメラメラの実を手に入れたのはだれ？",
        "choices": ["バージェス", "サボ", "バルトロメオ", "レベッカ"],
        "answer": "サボ",
        "explanation": "エースの意志を継ぐような熱い場面だったね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "悪魔の実",
        "question": "シュガーの悪魔の実は？",
        "choices": ["ホビホビの実", "ホロホロの実", "バリバリの実", "アトアトの実"],
        "answer": "ホビホビの実",
        "explanation": "ドレスローザの支配構造に大きく関わる能力だったよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "悪魔の実",
        "question": "バルトロメオの悪魔の実は？",
        "choices": ["バネバネの実", "バリバリの実", "ベリベリの実", "バラバラの実"],
        "answer": "バリバリの実",
        "explanation": "バリアで仲間を守る印象的な能力だね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "キャベンディッシュのもう一つの人格の名前は？",
        "choices": ["ハクバ", "カマソ", "デュバル", "ペドロ"],
        "answer": "ハクバ",
        "explanation": "眠ったあとに現れる危険な人格として知られているよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "藤虎の本名は？",
        "choices": ["ボルサリーノ", "イッショウ", "アラマキ", "サカズキ"],
        "answer": "イッショウ",
        "explanation": "海軍大将としてドレスローザ編でも強い印象を残したね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "緑牛の本名は？",
        "choices": ["イッショウ", "クザン", "アラマキ", "コング"],
        "answer": "アラマキ",
        "explanation": "海軍大将のひとりとして登場しているよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "海賊団",
        "question": "コビーが所属している海軍の機密部隊は？",
        "choices": ["CP0", "SWORD", "ジェルマ66", "王下七武海"],
        "answer": "SWORD",
        "explanation": "海軍の中でも特別な立場にある部隊だね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "キャラクター",
        "question": "パンクハザード編で危険なガス兵器を作っていた科学者は？",
        "choices": ["ベガパンク", "シーザー", "ジャッジ", "クイーン"],
        "answer": "シーザー",
        "explanation": "ガスガスの実の能力者としても登場したよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "バーソロミュー・くまの異名は？",
        "choices": ["海侠", "暴君", "冥王", "死の外科医"],
        "answer": "暴君",
        "explanation": "七武海の一人としても知られていたね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "海賊団",
        "question": "バーソロミュー・くまがかつて所属していた組織は？",
        "choices": ["革命軍", "CP9", "白ひげ海賊団", "巨兵海賊団"],
        "answer": "革命軍",
        "explanation": "くまの背景を知る上でとても大切な設定だよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "悪魔の実",
        "question": "ボア・ハンコックの悪魔の実は？",
        "choices": ["ヘビヘビの実", "メロメロの実", "スベスベの実", "ホロホロの実"],
        "answer": "メロメロの実",
        "explanation": "相手を石化させる印象的な能力だね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "悪魔の実",
        "question": "マゼランの悪魔の実は？",
        "choices": ["ドクドクの実", "モクモクの実", "ヌマヌマの実", "ガスガスの実"],
        "answer": "ドクドクの実",
        "explanation": "インペルダウンで非常に恐れられた毒の能力だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "インペルダウンの副署長はだれ？",
        "choices": ["サディちゃん", "ハンニャバル", "ドミノ", "シリュウ"],
        "answer": "ハンニャバル",
        "explanation": "コミカルさと責任感の両方が印象に残るキャラだね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "イワンコフの異名として有名なのは？",
        "choices": ["海賊狩り", "奇跡の人", "天夜叉", "白猟"],
        "answer": "奇跡の人",
        "explanation": "革命軍の幹部としても強い存在感があるよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "悪魔の実",
        "question": "モネの悪魔の実は？",
        "choices": ["ユキユキの実", "ヒエヒエの実", "モクモクの実", "ホロホロの実"],
        "answer": "ユキユキの実",
        "explanation": "パンクハザード編で登場した雪の能力だね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "海賊団",
        "question": "たしぎが所属している組織は？",
        "choices": ["革命軍", "海軍", "CP0", "ハートの海賊団"],
        "answer": "海軍",
        "explanation": "スモーカーの部下として行動することも多いね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "海賊団",
        "question": "スモーカーが所属している組織は？",
        "choices": ["海軍", "革命軍", "バロックワークス", "九蛇海賊団"],
        "answer": "海軍",
        "explanation": "ルフィを追う海兵として早い段階から登場したよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "キャラクター",
        "question": "ヒナの異名は？",
        "choices": ["檻のヒナ", "白猟のヒナ", "氷のヒナ", "黒檻のヒナ"],
        "answer": "檻のヒナ",
        "explanation": "オリオリの実の能力とも結びつく異名だね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "キャラクター",
        "question": "ガープの海軍での階級として正しいものは？",
        "choices": ["元帥", "大将", "中将", "少将"],
        "answer": "中将",
        "explanation": "海軍の英雄としても知られているよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "キャラクター",
        "question": "シャンクスが失ったのはどちらの腕？",
        "choices": ["右腕", "左腕", "両腕ではない", "どちらでもない"],
        "answer": "左腕",
        "explanation": "ルフィを助けたときに失った大切な腕だね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "キャラクター",
        "question": "ナミとノジコを育てた女性の名前は？",
        "choices": ["くれは", "ベルメール", "トキ", "オルビア"],
        "answer": "ベルメール",
        "explanation": "アーロンパーク編でもとても大切な存在として描かれたね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "キャラクター",
        "question": "ノジコとナミの関係としていちばん近いものは？",
        "choices": ["実の姉妹", "育ての姉妹", "いとこ", "同級生"],
        "answer": "育ての姉妹",
        "explanation": "血はつながっていなくても強い家族の絆があるよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "キャラクター",
        "question": "アーロンはどの種族？",
        "choices": ["巨人族", "魚人族", "小人族", "ミンク族"],
        "answer": "魚人族",
        "explanation": "アーロンパーク編の大きなテーマにも関わる設定だね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "キャラクター",
        "question": "ジンベエの得意な戦い方は？",
        "choices": ["人魚柔術", "魚人空手", "六式", "覇王色"],
        "answer": "魚人空手",
        "explanation": "水を利用した強力な技が特徴だよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "海賊団",
        "question": "九蛇海賊団の船長はだれ？",
        "choices": ["ヤマト", "ハンコック", "しらほし", "コアラ"],
        "answer": "ハンコック",
        "explanation": "女ヶ島アマゾン・リリーの皇帝としても知られているよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "エピソード",
        "question": "女ヶ島が舞台になる編の名前は？",
        "choices": ["魚人島編", "アマゾン・リリー編", "パンクハザード編", "ジャヤ編"],
        "answer": "アマゾン・リリー編",
        "explanation": "シャボンディ諸島のあとにルフィが流れ着いた場所だね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "エピソード",
        "question": "チョッパーが仲間になる島は？",
        "choices": ["オハラ", "ドラム島", "シロップ村", "リトルガーデン"],
        "answer": "ドラム島",
        "explanation": "ヒルルクとくれはのエピソードも胸に残るね。",
    },
    {
        "difficulty": "ふつう",
        "genre": "エピソード",
        "question": "アーロンとの決戦が行われた場所を含む編は？",
        "choices": ["アーロンパーク編", "空島編", "ドレスローザ編", "ワノ国編"],
        "answer": "アーロンパーク編",
        "explanation": "ナミの過去と決意が描かれた重要な編だよ。",
    },
    {
        "difficulty": "ふつう",
        "genre": "エピソード",
        "question": "ドリーとブロギーが登場する島は？",
        "choices": ["ジャヤ", "リトルガーデン", "パンクハザード", "スリラーバーク"],
        "answer": "リトルガーデン",
        "explanation": "巨人族の誇り高い戦士たちが印象的だったね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "エピソード",
        "question": "空島へ行く前にルフィたちが立ち寄った島の名前は？",
        "choices": ["ジャヤ", "ゾウ", "女ヶ島", "パンクハザード"],
        "answer": "ジャヤ",
        "explanation": "ベラミーや黒ひげとも関わる重要な場所だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "エピソード",
        "question": "フォクシー海賊団とのデービーバックファイトが描かれた編は？",
        "choices": ["ロングリングロングランド編", "スリラーバーク編", "ゾウ編", "魚人島編"],
        "answer": "ロングリングロングランド編",
        "explanation": "コミカルだけど印象に残る勝負が多かったね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "海賊団",
        "question": "ハートの海賊団の潜水艦の名前は？",
        "choices": ["ポーラータング号", "サウザンドサニー号", "ノストラ・カステロ号", "ヴィクトリアパンク号"],
        "answer": "ポーラータング号",
        "explanation": "ローたちらしい特徴的な船だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "海賊団",
        "question": "キッド海賊団の船の名前は？",
        "choices": ["ヴィクトリアパンク号", "ポーラータング号", "レッドフォース号", "モビーディック号"],
        "answer": "ヴィクトリアパンク号",
        "explanation": "キッド海賊団の船名として覚えておくと強いね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "海賊団",
        "question": "ビッグ・マム海賊団の船の名前は？",
        "choices": ["クイーン・ママ・シャンテ号", "モビーディック号", "オーロ・ジャクソン号", "サーベル・オブ・ジーベック号"],
        "answer": "クイーン・ママ・シャンテ号",
        "explanation": "ホールケーキアイランド編で存在感のある船だったね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "海賊団",
        "question": "ファイアタンク海賊団の船の名前は？",
        "choices": ["ノストラ・カステロ号", "レッドフォース号", "ヴィクトリアパンク号", "モビーディック号"],
        "answer": "ノストラ・カステロ号",
        "explanation": "カポネ・ベッジの海賊団の船だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "海賊団",
        "question": "赤髪海賊団の船の名前は？",
        "choices": ["レッドフォース号", "ポーラータング号", "ゴーイングメリー号", "クイーン・ママ・シャンテ号"],
        "answer": "レッドフォース号",
        "explanation": "シャンクスたちの船としてとても有名だね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "セリフ・表現",
        "question": "黒ひげの有名なせりふ「人の夢は終わらねェ！」を言った人物は？",
        "choices": ["ルフィ", "エース", "黒ひげ", "シャンクス"],
        "answer": "黒ひげ",
        "explanation": "ジャヤ編での印象的な場面としてよく語られるね。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "セリフ・表現",
        "question": "「愛してくれてありがとう」と言い残した人物はだれ？",
        "choices": ["エース", "白ひげ", "おでん", "ベルメール"],
        "answer": "エース",
        "explanation": "頂上戦争のとても切ない名場面だよ。",
    },
    {
        "difficulty": "むずかしい",
        "genre": "セリフ・表現",
        "question": "「この戦争を終わらせに来た」と言って現れたのはだれ？",
        "choices": ["ドラゴン", "シャンクス", "カイドウ", "レイリー"],
        "answer": "シャンクス",
        "explanation": "頂上戦争の流れを一気に変えた名登場シーンだね。",
    },
]


RANKS = [
    (1.0, "海賊王級"),
    (0.8, "四皇級"),
    (0.6, "新世界の実力者"),
    (0.4, "グランドライン通"),
    (0.0, "東の海の挑戦者"),
]


PRESET_CONFIGS = {
    "おためし": ["かんたん", "ふつう", "むずかしい"],
    "つよい": ["ふつう", "むずかしい"],
    "達人": ["むずかしい"],
}


def build_quiz(question_count: int = QUESTION_COUNT):
    selected_genres = st.session_state.get("selected_genres")
    selected_difficulties = st.session_state.get("selected_difficulties")
    if selected_genres:
        pool = [q for q in QUESTION_BANK if q["genre"] in selected_genres]
    else:
        pool = QUESTION_BANK[:]
    if selected_difficulties:
        pool = [q for q in pool if q["difficulty"] in selected_difficulties]
    random.shuffle(pool)
    return pool[: min(question_count, len(pool))]


def get_image_path(image_name: str | None) -> Path | None:
    if not image_name:
        return None
    candidate = Path(__file__).parent / "assets" / image_name
    if candidate.exists():
        return candidate
    return None


def reset_quiz():
    for key in list(st.session_state.keys()):
        if key.startswith("question_"):
            del st.session_state[key]
    st.session_state.quiz = build_quiz()
    st.session_state.answers = {}
    st.session_state.submitted = False
    st.session_state.current_question = 1


def sync_quiz_to_filters():
    signature = (
        tuple(sorted(st.session_state.selected_difficulties)),
        tuple(sorted(st.session_state.selected_genres)),
    )
    if st.session_state.get("filter_signature") != signature:
        st.session_state.filter_signature = signature
        reset_quiz()


def get_rank(score: int) -> str:
    total_questions = max(1, len(st.session_state.quiz))
    ratio = score / total_questions
    for minimum, label in RANKS:
        if ratio >= minimum:
            return label
    return RANKS[-1][1]


if "quiz" not in st.session_state:
    st.session_state.selected_genres = sorted({item["genre"] for item in QUESTION_BANK})
    st.session_state.selected_preset = "達人"
    st.session_state.selected_difficulties = PRESET_CONFIGS["達人"]
    st.session_state.selected_genre_mode = "全ジャンル"
    st.session_state.filter_signature = None
    reset_quiz()


st.title("ワンピース クイズ")
st.caption("iPhone 6sでも遊びやすい軽量表示です。")
st.write(f"出題数: {len(st.session_state.quiz)}問")
st.write(f"モード: {st.session_state.selected_preset}")

all_genres = sorted({item["genre"] for item in QUESTION_BANK})
st.subheader("設定")

mode_labels = ["達人", "つよい", "おためし"]
selected_preset = st.selectbox(
    "モード",
    options=mode_labels,
    index=mode_labels.index(
        st.session_state.selected_preset
        if st.session_state.selected_preset in mode_labels
        else "達人"
    ),
)

if selected_preset != st.session_state.selected_preset and selected_preset in PRESET_CONFIGS:
    st.session_state.selected_preset = selected_preset
    st.session_state.selected_difficulties = PRESET_CONFIGS[selected_preset]

mode_descriptions = {
    "達人": "むずかしい問題だけが出ます。",
    "つよい": "ふつうとむずかしいが出ます。",
    "おためし": "かんたんからむずかしいまで全部出ます。",
}
st.caption(mode_descriptions[st.session_state.selected_preset])

genre_options = ["全ジャンル"] + all_genres
selected_genre_mode = st.selectbox(
    "ジャンル",
    options=genre_options,
    index=genre_options.index(st.session_state.selected_genre_mode)
    if st.session_state.selected_genre_mode in genre_options
    else 0,
)

normalized_genres = all_genres if selected_genre_mode == "全ジャンル" else [selected_genre_mode]
if (
    normalized_genres != st.session_state.selected_genres
    or selected_genre_mode != st.session_state.selected_genre_mode
):
    st.session_state.selected_genre_mode = selected_genre_mode
    st.session_state.selected_genres = normalized_genres

sync_quiz_to_filters()

st.caption(f"出題: {selected_genre_mode}")

if len(st.session_state.quiz) < QUESTION_COUNT:
    st.warning(f"選んだ条件の問題数がまだ{QUESTION_COUNT}問未満なので、今回はある分だけ出題しています。")

total_questions = len(st.session_state.quiz)
if total_questions == 0:
    st.error("このモードとジャンルの組み合わせには、まだ問題がありません。")
    st.info("ジャンルを『全ジャンル』にするか、モードを『つよい』または『おためし』に変えてみてください。")
    st.stop()

current_index = min(st.session_state.current_question, total_questions)
current_item = st.session_state.quiz[current_index - 1]

st.write(f"いまの問題: 第{current_index}問 / {total_questions}問")
st.write(f"答えた数: {len(st.session_state.answers)}問")
st.progress(current_index / max(1, total_questions))
st.caption(f"{current_item['difficulty']} ・ {current_item['genre']}")
st.subheader(f"第{current_index}問")
image_path = get_image_path(current_item.get("image"))
if image_path and not LIGHTWEIGHT_MODE:
    st.image(str(image_path), use_container_width=True)
st.write(current_item["question"])
st.session_state.answers[current_index] = st.radio(
    label=f"Q{current_index}",
    options=current_item["choices"],
    index=None,
    key=f"question_{current_index}",
    label_visibility="collapsed",
)
if st.session_state.submitted:
    user_answer = st.session_state.answers.get(current_index)
    is_correct = user_answer == current_item["answer"]
    if is_correct:
        st.success("正解！")
    else:
        st.error(f"正解は「{current_item['answer']}」だよ。")
    st.caption(current_item["explanation"])

current_answered = bool(st.session_state.answers.get(current_index))

nav_left, nav_mid, nav_right = st.columns([1, 1.2, 1])
with nav_left:
    if st.button("前の問題", use_container_width=True, disabled=current_index == 1):
        st.session_state.current_question = max(1, current_index - 1)
        st.rerun()
with nav_mid:
    if current_index < total_questions:
        if st.button("次の問題へ", type="primary", use_container_width=True, disabled=not current_answered):
            st.session_state.current_question = min(total_questions, current_index + 1)
            st.rerun()
    else:
        if st.button("答え合わせ", type="primary", use_container_width=True, disabled=len(st.session_state.answers) < total_questions):
            st.session_state.submitted = True
with nav_right:
    if st.button(f"新しい{total_questions}問で遊ぶ", use_container_width=True):
        reset_quiz()
        st.rerun()

if not current_answered:
    st.info("この問題の答えを選ぶと次へ進めるよ。")

if not st.session_state.submitted:
    remaining = total_questions - len(st.session_state.answers)
    if remaining > 0:
        st.caption(f"あと{remaining}問こたえると結果が見られます。")

if st.session_state.submitted and not LIGHTWEIGHT_MODE:
    with st.expander("答えを見直す"):
        for review_index, review_item in enumerate(st.session_state.quiz, start=1):
            user_answer = st.session_state.answers.get(review_index)
            is_correct = user_answer == review_item["answer"]
            mark = "○" if is_correct else "×"
            st.markdown(f"**{mark} 第{review_index}問** {review_item['question']}")
            st.caption(f"あなたの答え: {user_answer} / 正解: {review_item['answer']}")
            st.caption(review_item["explanation"])

if st.session_state.submitted:
    score = sum(
        1
        for index, item in enumerate(st.session_state.quiz, start=1)
        if st.session_state.answers.get(index) == item["answer"]
    )
    rank = get_rank(score)
    total_questions = len(st.session_state.quiz)
    st.write("")
    st.markdown("## 結果発表")
    st.metric("スコア", f"{score} / {total_questions}")
    st.success(f"称号: {rank}")
    if score == total_questions:
        st.balloons()
        st.markdown("**全問正解！ これはもう海賊王級！**")
    elif score >= max(7, int(total_questions * 0.7)):
        st.markdown("**かなり詳しいね。新世界でも通用するレベル！**")
    elif score >= max(4, int(total_questions * 0.4)):
        st.markdown("**いい感じ！ まだまだ伸びる余地あり！**")
    else:
        st.markdown("**次はもっと上を目指そう。もう1回遊ぶと覚えやすいよ。**")
