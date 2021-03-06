from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

# Create your models here.


class Genre(models.Model):
    """Model representing a book genre."""

    name = models.CharField(max_length=200, help_text="Enter a book genre, e.g. 'Science Fiction'.")

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book (not a specific copy."""

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description.")
    isbn = models.CharField('ISBN', max_length=13, help_text="13 Characters.")
    genre = models.ManyToManyField(Genre, help_text="Select a genre for the book.")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Creates a string for the genre."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model representing a specific copy of a book."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Auswahl von Stati, die später als choices genutzt werden koennen
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        # Wonach Ergebnisse bei einer Abfrage geordnet werden.
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return '%s (%s)' % (self.id, self.book.title)


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '%s, %s' % (self.last_name, self.first_name)


class Language(models.Model):
    """Model representing a language."""

    name = models.CharField(max_length=200, help_text="Enter the books language.")

    def __str__(self):
        return self.name
