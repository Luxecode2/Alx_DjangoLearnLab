from bookshelf.models import Book

> > > # Create
> > >
> > > book = Book.objects.create(title="1984", author="George >>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
> > > print(book)

# Retrieve

all_books = Book.objects.all()
print(all_books)

# Update

book.title = "Nineteen Eighty-Four"
book.save()
print(book)

# Delete

book.delete()
print(Book.objects.all())

> > > print(book)
> > > 1984 by George Orwell (1949)
> > >
> > > # Retrieve
> > >
> > > all_books = Book.objects.all()
> > > print(all_books)
> > > <QuerySet [<Book: 1984 by George Orwell (1949)>]>
> > >
> > > # Update
> > >
> > > book.title = "Nineteen Eighty-Four"
> > > book.save()
> > > print(book)
> > > Nineteen Eighty-Four by George Orwell (1949)
> > >
> > > # Delete
> > >
> > > book.delete()
> > > (1, {'bookshelf.Book': 1})
> > > print(Book.objects.all())
> > > <QuerySet []>
