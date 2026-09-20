var Audio = (function () {
  var ctx = null;
  function getCtx() {
    if (ctx) return ctx;
    var Ctx = window.AudioContext || window.webkitAudioContext;
    if (!Ctx) return null;
    try { ctx = new Ctx(); } catch (e) { ctx = null; }
    return ctx;
  }

  function tone(freq, duration, type, volume, when) {
    var c = getCtx();
    if (!c) return;
    if (c.state === 'suspended') { try { c.resume(); } catch (e) {} }
    var t0 = c.currentTime + (when || 0);
    var osc = c.createOscillator();
    var gain = c.createGain();
    osc.type = type || 'square';
    osc.frequency.setValueAtTime(freq, t0);
    gain.gain.setValueAtTime(0, t0);
    gain.gain.linearRampToValueAtTime(volume || 0.15, t0 + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.001, t0 + duration);
    osc.connect(gain).connect(c.destination);
    osc.start(t0);
    osc.stop(t0 + duration + 0.05);
  }

  function correct() {
    tone(660, 0.12, 'square', 0.18, 0);
    tone(880, 0.18, 'square', 0.18, 0.1);
    tone(1320, 0.22, 'square', 0.18, 0.2);
  }
  function wrong() {
    tone(220, 0.18, 'sawtooth', 0.18, 0);
    tone(160, 0.28, 'sawtooth', 0.18, 0.12);
  }
  function tap() { tone(880, 0.05, 'square', 0.1, 0); }
  function fanfare() {
    tone(523, 0.14, 'square', 0.18, 0);
    tone(659, 0.14, 'square', 0.18, 0.12);
    tone(784, 0.14, 'square', 0.18, 0.24);
    tone(1047, 0.3, 'square', 0.2, 0.36);
  }
  function unlock() {
    var c = getCtx();
    if (c && c.state === 'suspended') { try { c.resume(); } catch (e) {} }
  }

  return {
    correct: correct,
    wrong: wrong,
    tap: tap,
    fanfare: fanfare,
    unlock: unlock
  };
})();
