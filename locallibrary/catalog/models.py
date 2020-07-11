from django.db import models
from django.urls import reverse # Used to generate URLs
import uuid # required for unique book instances, creates unique ids

"""
How to actually use model classes
"To create a record you can define an instance of the model and then call save()."
e.g. new_language = Language(language='swahili')
    new_language.save() # the dot syntax gets methods and properties from oop objects in Python. I think the save() function is from django's models.Model class

    languages = Language.objects.all()
    for language in languages:
        language.language = language.language.title() # the Python title() function capitalises the first letter of every word
        language.language.save()

n.b. this code is untested
"""

class Genre(models.Model):
    """This model represents a book genre"""
    # max_length will be enforced at the db level, possibly also at the form level
    name= models.CharField(max_length=200, help_text="Enter a book genre(e.g. Science Fiction)")

    def __str__(self):
        """String for representing the genre object. Every model should have some such __str__ method."""
        return self.name

class Language(models.Model):
    language=models.CharField(max_length=200, help_text="Please enter a language")
    # it would be nice to enforce a case-insensitive uniqueness constraint

    def __str__(self):
        return self.language

class Book(models.Model):
    """Model representing a book (but not a specific physical copy of the book)"""

    # this implements a one-to-many relationship from authors (one) to books (many). For now, we've hardcoded 'Author', but this is temporary. If the author gets deleted, this model's author value will become null. Finally, null is permitted for this column.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    # max_length for TextField is only enforced at form level
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")

    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ManyToManyField(Language, help_text='Select a language for this book')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns url to access a detail record for this book"""
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique library ID for this copy of this book')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length = 200)
    due_back = models.DateField(null=True, blank=True)

    # this is a tuple, an ordered, immutable list, containing tuples
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    status = models.CharField(
        max_length = 1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )

    class Meta:
        # determines how query results will be ordered
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        # order first by last name - given identical last names, order by first name
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'