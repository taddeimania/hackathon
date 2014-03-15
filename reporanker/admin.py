from django.contrib import admin

from models import Repo, Review


class RepoAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'language', 'star_count', 'watchers_count', 'forks_count', 'open_issue_count']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'repo', 'octocats']


admin.site.register(Repo, RepoAdmin)
admin.site.register(Review, ReviewAdmin)
