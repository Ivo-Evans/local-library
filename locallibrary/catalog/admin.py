from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# literally registering the tables (really, models) with the admin site
admin.site.register(Genre)
admin.site.register(Language)

class BookInline(admin.StackedInline):
    model = Book

# for unchanged admin behaviour just put pass in the class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # tuple with criteria to display on site
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')] # for the form. Tuple means inline formatting
    inlines = [BookInline]

admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

# the decorator pattern does exactly the same as the function call version above
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display= ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]
    # display_genre is a function defined in the model
    # Note: Getting the genre may not be a good idea here, because of the "cost" of the database operation (many-many). We're showing you how because calling functions in your models can be very useful for other reasons — for example to add a Delete link next to every item in the list.

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

