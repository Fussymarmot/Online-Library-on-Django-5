from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Book, Genre
from .forms import BookForm
from django.db.models import Q


def book_list(request):
    query_title = request.GET.get('q_title')  # Поиск по названию книги
    query_author = request.GET.get('q_author')  # Поиск по автору
    genre_filter = request.GET.get('genre')  # Фильтр по жанру
    books = Book.objects.all()

    # Фильтрация по названию книги
    if query_title:
        books = books.filter(title__icontains=query_title)

    # Фильтрация по автору
    if query_author:
        books = books.filter(author__icontains=query_author)

    # Фильтрация по жанру (по ID жанра)
    if genre_filter:
        try:
            genre = Genre.objects.get(name=genre_filter)  # Получаем объект жанра по имени
            books = books.filter(genre=genre)  # Фильтруем книги по найденному жанру
        except Genre.DoesNotExist:
            books = books.none()  # Если жанр не найден, возвращаем пустой список книг

    # Пагинация: показываем 10 книг на странице
    paginator = Paginator(books, 10)  # 10 — количество книг на одной странице
    page_number = request.GET.get('page')  # Текущая страница из запроса
    page_obj = paginator.get_page(page_number)  # Получаем объекты для текущей страницы

    context = {
        'books': page_obj,  # Передаем объект страницы вместо полного списка
        'page_obj': page_obj,  # Для пагинации в шаблоне
        'query_title': request.GET.get('q_title', ''),
        'query_author': request.GET.get('q_author', ''),
        'genre_filter': genre_filter,
        'genres': Genre.objects.all(),  # Передаем все жанры для отображения в фильтре
    }
    return render(request, 'books/book_list.html', context)


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)  # Обработка файлов
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Перенаправление на список книг
    else:
        form = BookForm()

    return render(request, 'books/add_book.html', {'form': form})