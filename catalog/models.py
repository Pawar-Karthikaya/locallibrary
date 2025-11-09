from django.db import models

# Create your models here.
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
import uuid

class Gener(models.Model):
    """Model representing a book gener """
    name = models.CharField(
        max_length = 200,
        unique=True,
        help_text="Enter a book gener (e.g. Science Fiction, French Poetry etc.)"
    )

    def __str__(self):
        """ String for representing model object"""
        return self.name
    
    def get_absolute_url(self):
        return reverse('gener-detail', args=[str(self.id)])
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='gener_name_case_insensitive_unique',
                violation_error_message='Gener already exists with this name (case insensitive).'
            ),
        ]


class Book(models.Model):
    """ Model representing book (but not specific coppy of a book)"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book ')
    isbn = models.CharField(
        'ISBN', max_length=13, unique=True,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )
    gener = models.ManyToManyField(Gener, help_text='Select a gener for this book')

    def __str__(self):
        """ String for representing the Model object """
        return self.title
    
    def get_absolute_url(self):
        """ Returns the url to access a detail record for this book. """
        return reverse('book-detail', args=[str(self.id)])
    def display_gener(self):
        """ Creates a string for the Gener. This is required to display gener in Admin."""
        return ', '.join(gener.name for gener in self.gener.all()[:3])
    display_gener.short_description = 'Gener'

class BookIstance(models.Model):
    """Model representing specific copy of a book (i.e. that can be borrowed from the library)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unque ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the model object"""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representin an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.FloatField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering =  ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    
class Language(models.Model):
    """Model representing a Language (e.g. English, Franch, Japanese etc.)"""
    name = models.CharField(
        max_length=200,
        help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)"
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])
    
    class Meta:
        ordering = ['name']
    
# class  MyModelName(models.Model):

#     my_field_name = models.CharField(max_length=20, help_text='Enter Feald documentation')

#     # meta data
#     class Meta:
#         ordering = ['-my_field_name']


#     def get_absolute_url(self):
#         return reverse("model_detail_value", args=[str(self.id)])
    
#     def __str__(self):
#         return self.my_field_name
    
