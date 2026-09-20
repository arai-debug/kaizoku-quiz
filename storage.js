var Storage = (function () {
  var KEY_BEST = 'onepiece_best_score';
  var KEY_PREFS = 'onepiece_prefs';

  function getBestScore() {
    try {
      var v = localStorage.getItem(KEY_BEST);
      return v ? parseInt(v, 10) || 0 : 0;
    } catch (e) { return 0; }
  }
  function setBestScore(score) {
    try { localStorage.setItem(KEY_BEST, String(score)); } catch (e) {}
  }
  function getPrefs() {
    try {
      var v = localStorage.getItem(KEY_PREFS);
      return v ? JSON.parse(v) : null;
    } catch (e) { return null; }
  }
  function setPrefs(prefs) {
    try { localStorage.setItem(KEY_PREFS, JSON.stringify(prefs)); } catch (e) {}
  }

  return {
    getBestScore: getBestScore,
    setBestScore: setBestScore,
    getPrefs: getPrefs,
    setPrefs: setPrefs
  };
})();
