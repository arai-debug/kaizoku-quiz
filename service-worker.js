var CACHE = 'onepiece-quiz-v2';
var ASSETS = [
  './',
  './index.html',
  './style.css',
  './storage.js',
  './audio.js',
  './quiz.js',
  './app.js',
  './questions.json',
  './manifest.json'
];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) { return c.addAll(ASSETS); })
  );
  self.skipWaiting();
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) {
        return caches.delete(k);
      }));
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function (e) {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(function (cached) {
      return cached || fetch(e.request).then(function (res) {
        var clone = res.clone();
        caches.open(CACHE).then(function (c) {
          try { c.put(e.request, clone); } catch (err) {}
        });
        return res;
      }).catch(function () { return cached; });
    })
  );
});
