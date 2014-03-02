module.exports = (grunt) ->

  require('load-grunt-config')(grunt)

  grunt.task.registerTask 'default', ['coffee', 'concat:lib', 'concat:app']
  grunt.task.registerTask 'node', ['coffee', 'concat:node_app']
  grunt.task.registerTask 'local', ['default', 'watch']
