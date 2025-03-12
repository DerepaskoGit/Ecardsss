from django.db import models, connection
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class InviteCodeDb(models.Model):
    invite_code = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='invite')

    def __str__(self):
        return self.invite_code

class Module(models.Model):
    user = models.ManyToManyField(User, blank=True, related_name='modules')

    title = models.CharField(max_length=50, db_index=True)
    description = models.CharField(max_length=500, blank=True)
    slug = models.SlugField(max_length=80, db_index=True, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = self.id
            super(Module, self).save(update_fields=['slug'])
        
        tabel_name = f'Module_{self.id}'
        with connection.cursor() as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {tabel_name} (
                    id SERIAL PRIMARY KEY,
                    type_card VARCHAR(20) CHECK (type_card IN ('simple', 'phrase', 'test')),
                    word_front VARCHAR(20),
                    word_back VARCHAR(20),
                    phrase_front VARCHAR(200),
                    phrase_back VARCHAR(200),
                    image BYTEA,
                    audio_word_front BYTEA,
                    audio_word_back BYTEA,
                    audio_phrase_front BYTEA,
                    audio_phrase_back BYTEA
                )
            """)
        
    def get_absolute_url(self):
        return reverse('module', kwargs={'module_slug':self.slug})

    def __str__(self):
        return self.title
    
@receiver(pre_delete, sender=Module)
def delete_module_table(sender, instance, **kwargs):
    tabel_name = f'Module_{instance.id}'
    
    with connection.cursor() as cursor:
        cursor.execute(f'DROP TABLE IF EXISTS {tabel_name};')
