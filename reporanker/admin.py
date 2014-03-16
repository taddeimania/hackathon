from django.contrib import admin

from models import Repo, Review, ReviewOpinion


class RepoAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'language', 'star_count', 'watchers_count', 'forks_count', 'open_issue_count']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'repo', 'octocats']

class ReviewOpinionAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'helpful']

admin.site.register(Repo, RepoAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewOpinion, ReviewOpinionAdmin)
