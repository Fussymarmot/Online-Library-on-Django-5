from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200) #название книги
    author = models.CharField(max_length=100) #автор 
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE) #жанр
    description = models.TextField() #описание книги
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)  # Поле для обложки книги

    def __str__(self):
        return self.title