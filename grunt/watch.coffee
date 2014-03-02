module.exports =
  scripts:
    files: [
      'appname/static/appname/coffee/*.coffee'
    ]
    tasks: ['dev']
    options:
      interrupt: true
      debounceDelay: 250
