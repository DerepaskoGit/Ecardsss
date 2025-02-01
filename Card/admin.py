from django.contrib import admin
from .models import Module, Flashcard

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    fields = ['user', 'title', 'slug', 'description']
    prepopulated_fields = {'slug':('title', )}

admin.site.register(Flashcard)


