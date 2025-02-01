from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class InviteCodeDb(models.Model):
    invite_code = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='invite')

    def __str__(self):
        return self.invite_code

class Module(models.Model):
    user = models.ManyToManyField(User, blank=True, related_name='modules')

    title = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=80, db_index=True, unique=True)
    description = models.CharField(max_length=500, blank=True)

    def save(self, *args, **kwargs):
        super(Module, self).save(*args, **kwargs)

        if not self.slug:
            self.slug = self.id
            super(Module, self).save(update_fields=['slug'])

    def get_absolute_url(self):
        return reverse('module', kwargs={'module_slug':self.slug})

    def __str__(self):
        return self.title
    
class Flashcard(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='card')

    word_front = models.CharField(max_length=30)
    word_back = models.CharField(max_length=30)
    phrase = models.CharField(max_length=250, blank=True)

    audio = models.FileField(upload_to='uploads_model', blank=True)
    image = models.ImageField(upload_to='uploads_model', blank=True)


    def __str__(self):
        return self.word_front
