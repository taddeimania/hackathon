module.exports = (grunt) ->

  require('load-grunt-config')(grunt)

  grunt.task.registerTask 'default', ['coffee', 'concat:lib', 'concat:app', 'less']
  grunt.task.registerTask 'local', ['default', 'watch']
