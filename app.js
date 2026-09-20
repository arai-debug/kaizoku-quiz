(function () {
  var screens = {
    title: document.getElementById('screen-title'),
    menu: document.getElementById('screen-menu'),
    game: document.getElementById('screen-game'),
    result: document.getElementById('screen-result')
  };

  var state = {
    mode: 'つよい',
    genres: [],
    count: 10,
    questions: [],
    index: 0,
    score: 0,
    answered: false
  };

  // ===== 画面切替 =====
  function show(name) {
    for (var k in screens) screens[k].classList.remove('active');
    screens[name].classList.add('active');
    window.scrollTo(0, 0);
  }

  // ===== メニュー初期化 =====
  function loadPrefs() {
    var p = Storage.getPrefs();
    if (p) {
      if (p.mode) state.mode = p.mode;
      if (typeof p.count === 'number') state.count = p.count;
      if (p.genres) state.genres = p.genres;
    }
    if (!state.genres.length) state.genres = Quiz.getGenres();
  }
  function savePrefs() {
    Storage.setPrefs({ mode: state.mode, count: state.count, genres: state.genres });
  }

  function renderMenu() {
    // 難易度
    var diffBtns = document.querySelectorAll('.diff-card');
    for (var i = 0; i < diffBtns.length; i++) {
      var b = diffBtns[i];
      if (b.getAttribute('data-mode') === state.mode) b.classList.add('selected');
      else b.classList.remove('selected');
    }
    // ジャンル
    var allGenres = Quiz.getGenres();
    var genreBox = document.getElementById('genre-options');
    genreBox.innerHTML = '';
    var allBtn = document.createElement('button');
    allBtn.className = 'genre-btn';
    allBtn.textContent = 'ぜんぶ';
    allBtn.setAttribute('data-genre', '__all__');
    if (state.genres.length === allGenres.length) allBtn.classList.add('selected');
    allBtn.addEventListener('click', function () {
      Audio.tap();
      state.genres = allGenres.slice();
      savePrefs();
      renderMenu();
    });
    genreBox.appendChild(allBtn);
    for (var g = 0; g < allGenres.length; g++) {
      (function (genre) {
        var btn = document.createElement('button');
        btn.className = 'genre-btn';
        btn.textContent = genre;
        if (state.genres.indexOf(genre) >= 0 && state.genres.length < allGenres.length) {
          btn.classList.add('selected');
        }
        btn.addEventListener('click', function () {
          Audio.tap();
          // 単一ジャンル選択モード
          state.genres = [genre];
          savePrefs();
          renderMenu();
        });
        genreBox.appendChild(btn);
      })(allGenres[g]);
    }
    // もんだいかず
    var countBtns = document.querySelectorAll('.count-card');
    for (var c = 0; c < countBtns.length; c++) {
      var cb = countBtns[c];
      if (parseInt(cb.getAttribute('data-count'), 10) === state.count) cb.classList.add('selected');
      else cb.classList.remove('selected');
    }
    // ベストスコア
    document.getElementById('best-score').textContent = Storage.getBestScore();
  }

  // ===== ゲーム =====
  function startGame() {
    state.questions = Quiz.build({ mode: state.mode, genres: state.genres, count: state.count });
    state.index = 0;
    state.score = 0;
    state.answered = false;
    document.getElementById('progress-total').textContent = state.questions.length;
    renderQuestion();
  }

  function renderQuestion() {
    state.answered = false;
    var q = state.questions[state.index];
    document.getElementById('progress-current').textContent = state.index + 1;
    document.getElementById('current-score').textContent = state.score;
    document.getElementById('progress-fill').style.width =
      ((state.index) / state.questions.length * 100) + '%';
    document.getElementById('q-difficulty').textContent = q.difficulty;
    document.getElementById('q-genre').textContent = q.genre;
    document.getElementById('question-text').textContent = q.question;

    var box = document.getElementById('choices');
    box.innerHTML = '';
    var marks = ['A', 'B', 'C', 'D'];
    for (var i = 0; i < q.choices.length; i++) {
      (function (choice, mark) {
        var btn = document.createElement('button');
        btn.className = 'choice-btn';
        var m = document.createElement('span');
        m.className = 'choice-mark';
        m.textContent = mark;
        var t = document.createElement('span');
        t.textContent = choice;
        btn.appendChild(m);
        btn.appendChild(t);
        btn.addEventListener('click', function () {
          if (state.answered) return;
          handleAnswer(btn, choice);
        });
        box.appendChild(btn);
      })(q.choices[i], marks[i]);
    }
    document.getElementById('feedback').hidden = true;
  }

  function handleAnswer(button, choice) {
    state.answered = true;
    var q = state.questions[state.index];
    var correct = choice === q.answer;
    var allBtns = document.querySelectorAll('#choices .choice-btn');
    for (var i = 0; i < allBtns.length; i++) {
      var b = allBtns[i];
      // 正解ボタンの判定:textContent に answer が含まれる
      var span = b.querySelectorAll('span')[1];
      if (span && span.textContent === q.answer) b.classList.add('correct');
      else if (b === button) b.classList.add('wrong');
      b.classList.add('disabled');
    }
    if (correct) {
      state.score++;
      document.getElementById('current-score').textContent = state.score;
      Audio.correct();
    } else {
      Audio.wrong();
    }

    var fb = document.getElementById('feedback');
    var bang = document.getElementById('feedback-bang');
    bang.textContent = correct ? 'ドン!!' : 'ガーン!!';
    bang.className = 'feedback-bang ' + (correct ? 'correct' : 'wrong');
    document.getElementById('feedback-explanation').textContent = correct
      ? q.explanation
      : 'せいかいは「' + q.answer + '」!! ' + q.explanation;
    fb.hidden = false;

    // 進捗バー更新
    document.getElementById('progress-fill').style.width =
      ((state.index + 1) / state.questions.length * 100) + '%';
  }

  function nextQuestion() {
    if (state.index + 1 >= state.questions.length) {
      showResult();
      return;
    }
    state.index++;
    renderQuestion();
  }

  // ===== 結果 =====
  function showResult() {
    var total = state.questions.length;
    var rank = Quiz.getRank(state.score, total);
    document.getElementById('result-rank').textContent = rank.label;
    document.getElementById('result-emoji').textContent = rank.emoji;
    document.getElementById('result-score').textContent = state.score;
    document.getElementById('result-total').textContent = total;
    document.getElementById('result-comment').textContent = rank.comment;

    // 星ゲージ(5段階)
    var stars = Math.round(rank.ratio * 5);
    var starText = '';
    for (var i = 0; i < 5; i++) starText += i < stars ? '⭐' : '☆';
    document.getElementById('result-stars').textContent = starText;

    // バナー文言
    var banner = document.getElementById('result-banner');
    if (rank.ratio >= 1.0) banner.textContent = 'PERFECT!!';
    else if (rank.ratio >= 0.6) banner.textContent = 'NICE!!';
    else banner.textContent = 'FINISH!!';

    // ベスト更新
    var prevBest = Storage.getBestScore();
    var newBest = false;
    if (state.score > prevBest) {
      Storage.setBestScore(state.score);
      newBest = true;
    }
    document.getElementById('result-newbest').hidden = !newBest;

    if (rank.ratio >= 0.6) Audio.fanfare();
    show('result');
  }

  // ===== イベント =====
  function bind() {
    document.body.addEventListener('click', function (e) {
      var t = e.target;
      while (t && t !== document.body) {
        var action = t.getAttribute && t.getAttribute('data-action');
        if (action) {
          Audio.unlock();
          Audio.tap();
          if (action === 'go-title') show('title');
          else if (action === 'go-menu') { renderMenu(); show('menu'); }
          else if (action === 'go-game') { startGame(); show('game'); }
          return;
        }
        var mode = t.getAttribute && t.getAttribute('data-mode');
        if (mode) {
          Audio.tap();
          state.mode = mode;
          savePrefs();
          renderMenu();
          return;
        }
        var count = t.getAttribute && t.getAttribute('data-count');
        if (count) {
          Audio.tap();
          state.count = parseInt(count, 10);
          savePrefs();
          renderMenu();
          return;
        }
        t = t.parentNode;
      }
    });

    document.getElementById('btn-next').addEventListener('click', function () {
      Audio.tap();
      nextQuestion();
    });
  }

  // ===== 起動 =====
  function init() {
    Quiz.load().then(function () {
      loadPrefs();
      bind();
    }).catch(function (err) {
      document.getElementById('screen-title').innerHTML =
        '<div style="color:#fff;text-align:center;padding:40px;font-weight:900;">'
        + 'もんだいデータが よみこめませんでした。<br><br>'
        + '(ローカルでひらく場合は<br>python3 -m http.server で起動してください)'
        + '<br><br><small>' + err + '</small></div>';
    });
  }
  init();
})();
