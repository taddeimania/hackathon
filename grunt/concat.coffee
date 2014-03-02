module.exports =
  lib:
    src: ['appname/static/appname/js/lib/jquery-1.9.1.js']
    dest: 'appname/static/appname/js/dist/lib.min.js'
  app:
    src: [
      'appname/static/appname/js/dist/app.min.js'
    ]
    dest: 'appname/static/appname/js/dist/app.concat.min.js'
  node_app:
    src: [
      # other files to concat for node app... underscore et all
      'node_app_name/src/dist/node_app.min.js'
    ]
    dest: 'appname/static/appname/js/dist/app.concat.min.js'
