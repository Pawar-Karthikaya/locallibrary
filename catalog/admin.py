from django.contrib import admin

# Register your models here.
from .models import Gener, Book, BookIstance, Author, Language

admin.site.register(Gener)
# admin.site.register(Book)
# admin.site.register(BookIstance)
# admin.site.register(Author)
admin.site.register(Language)


# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_gener')



@admin.register(BookIstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')
    
