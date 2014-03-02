module.exports =
  options:
    bare: true
  compile:
    files:
      'appname/static/appname/js/dist/app.min.js': 'appname/static/appname/coffee/*.coffee'
      'node_app_name/src/dist/node_app.min.js': 'node_app_name/src/*.coffee'
