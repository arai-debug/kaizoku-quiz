var Quiz = (function () {
  var allQuestions = [];
  var loaded = false;

  var MODE_DIFFICULTIES = {
    'おためし': ['かんたん', 'ふつう', 'むずかしい', 'げきむず'],
    'つよい': ['ふつう', 'むずかしい', 'げきむず'],
    'たつじん': ['むずかしい', 'げきむず']
  };

  var RANKS = [
    [1.0, '海賊王級', '👑', 'ぜんもんせいかい!! まさに海賊王!!'],
    [0.8, '四皇級', '🔥', '新世界でも通用するつよさ!!'],
    [0.6, '新世界の実力者', '⚔️', 'なかなかやるな…!!'],
    [0.4, 'グランドライン通', '⚓', 'もう少しで実力者!!'],
    [0.0, '東の海の挑戦者', '🌊', 'これからこれから!! もう一回!!']
  ];

  function load() {
    if (loaded) return Promise.resolve(allQuestions);
    return fetch('questions.json')
      .then(function (res) { return res.json(); })
      .then(function (data) {
        allQuestions = data;
        loaded = true;
        return allQuestions;
      });
  }

  function getGenres() {
    var set = {};
    for (var i = 0; i < allQuestions.length; i++) set[allQuestions[i].genre] = true;
    var arr = [];
    for (var k in set) arr.push(k);
    arr.sort();
    return arr;
  }

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function build(opts) {
    var difficulties = MODE_DIFFICULTIES[opts.mode] || MODE_DIFFICULTIES['つよい'];
    var genres = opts.genres && opts.genres.length ? opts.genres : getGenres();
    var pool = [];
    for (var i = 0; i < allQuestions.length; i++) {
      var q = allQuestions[i];
      if (difficulties.indexOf(q.difficulty) >= 0 && genres.indexOf(q.genre) >= 0) {
        pool.push(q);
      }
    }
    pool = shuffle(pool);
    var count = Math.min(opts.count || 10, pool.length);
    var picked = pool.slice(0, count);
    // 選択肢もシャッフル
    var result = [];
    for (var k = 0; k < picked.length; k++) {
      var item = picked[k];
      var copied = {
        difficulty: item.difficulty,
        genre: item.genre,
        question: item.question,
        answer: item.answer,
        explanation: item.explanation,
        choices: shuffle(item.choices)
      };
      result.push(copied);
    }
    return result;
  }

  function getRank(score, total) {
    var ratio = total > 0 ? score / total : 0;
    for (var i = 0; i < RANKS.length; i++) {
      if (ratio >= RANKS[i][0]) {
        return { ratio: ratio, label: RANKS[i][1], emoji: RANKS[i][2], comment: RANKS[i][3] };
      }
    }
    var last = RANKS[RANKS.length - 1];
    return { ratio: ratio, label: last[1], emoji: last[2], comment: last[3] };
  }

  return {
    load: load,
    getGenres: getGenres,
    build: build,
    getRank: getRank
  };
})();
