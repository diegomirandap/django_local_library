from django.db import models
from datetime import date
'''
ESQUELETO DA ESTRUTURA COM ALGUMAS MANIPULAÇÕES POSSÍVEIS!!!!!!!!!!!!!!!!!!!

# Create your models here.
class MyModelName(models.Model):
    """Uma típica classe definindo um modelo, derivada da classe Model."""

    # Campos
    my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')
    

    # Metadados
    class Meta:
        ordering = ['-my_field_name']

    # Métodos
    def get_absolute_url(self):
        """Retorna a url para acessar uma instancia específica de MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """ String para representar o objeto MyModelName (no site Admin)."""
        return self.my_field_name
    
# Crie um novo registro usando o construtor do modelo.
record = MyModelName(my_field_name="Instance #1")

# Salve o objeto no banco de dados.
record.save()

# Acessar valores de campo de modelo usando atributos do Python.
print(record.id) # should return 1 for the first record.
print(record.my_field_name) # should print 'Instance #1'

# Altere o registro modificando os campos e, em seguida, chamando save ().
record.my_field_name = "New Instance Name"
record.save()
'''
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200, 
        help_text='Enter a book genre (e.g. Science Fiction)'
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name
'''
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists (case insensitive match)"
            ),
        ]
'''
''''''

from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

class Language(models.Model):
    """Model representing a book language."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text='Enter the books natural language (English, Portugese etc.)'
    )
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access a particular language."""
        return reverse('book-language', args=[str(self.name)])
'''       
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message = "Language already exists (case insensitive match)"
            ),
        ]
'''
''''''

from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey(
        'Author', 
        on_delete=models.SET_NULL,
        null=True
    )
    #on_delete=models.SET_NULL ---> Caso o autro representado seja apagado da base, será substituido por NULL

    summary = models.TextField(
        max_length=1000, 
        help_text='Enter a brief description of the book'
    )

    isbn = models.CharField(
        'ISBN', 
        max_length=13, 
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(
        Genre, 
        help_text='Select a genre for this book'
    )

    language = models.ForeignKey(
        'Language',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        ordering = ['title','author']
    
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

import uuid # Required for unique book instances
from datetime import date
from django.contrib.auth.models import User

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        help_text='Unique ID for this particular book across whole library'
    )
    book = models.ForeignKey(
        'Book', 
        on_delete=models.SET_NULL, 
        null=True
    )
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)#null=disponível

    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)
    
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

    borrower = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
    

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(
        'died', 
        null=True, 
        blank=True
    )

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
    

