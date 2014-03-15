from django.db import models

from django.conf import settings


class BaseModel(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Repo(BaseModel):
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    owner_id = models.BigIntegerField()
    owner_name = models.CharField(max_length=255)
    owner_gravatar_url = models.CharField(max_length=1000)
    owner_url = models.CharField(max_length=1000)

    html_url = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)

    star_count = models.BigIntegerField()
    watchers_count = models.BigIntegerField()
    forks_count = models.BigIntegerField()
    language = models.CharField(max_length=255, blank=True, null=True)

    open_issue_count = models.BigIntegerField()

    def __unicode__(self):
        return "<Repo {}>".format(self.full_name)


class Review(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    repo = models.ForeignKey(Repo)

    octocats = models.BigIntegerField(choices=(map(lambda x: (x, x,), range(1, 6))))
    comment = models.TextField(max_length=4000, blank=True, null=True)

    class Meta:
        ordering = ('-date_added', )
