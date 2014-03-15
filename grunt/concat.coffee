module.exports =
  lib:
    src: ['reporanker/static/reporanker/js/lib/jquery-1.11.0.js']
    dest: 'reporanker/static/reporanker/js/dist/lib.min.js'
  app:
    src: [
      'reporanker/static/reporanker/js/dist/app.min.js'
    ]
    dest: 'reporanker/static/reporanker/js/dist/app.concat.min.js'
