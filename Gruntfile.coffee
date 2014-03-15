module.exports = (grunt) ->

  require('load-grunt-config')(grunt)

  grunt.task.registerTask 'default', ['coffee', 'concat:lib', 'less']
  grunt.task.registerTask 'local', ['default', 'watch']
