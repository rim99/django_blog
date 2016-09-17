from django.db import models

# Create your models here.

class Tag(models.Model):
    tag = models.CharField('Shown in web pages', max_length=100)

    def __str__(self):
        return self.tag

class Blogpost(models.Model):
    title = models.CharField(max_length=100)
    tag = models.ManyToManyField(Tag)
    blog_id = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.title

    @property
    def show_tag(self):
        tag_list = []
        for tag in self.tag.all().order_by('tag'):
            tag_list.append(tag.tag)
        return tag_list
