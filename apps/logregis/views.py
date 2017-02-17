from django.shortcuts import render, redirect
from .models import User, Book, Author, Review
from django.contrib import messages
import bcrypt

# ==============================================================================
#                                   Render
# ==============================================================================

# ---------------------------
#       Index Route
# ---------------------------

def index(request):
    if 'user_id' in request.session:
        return redirect('/success')

    return render(request, 'logregis/index.html')

# ---------------------------
#       Register
# ---------------------------

def register(request):
    if 'user_id' in request.session:
        return redirect('/success')
    return render(request, 'logregis/register.html')

# ---------------------------
#       Login_Success
# ---------------------------

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.filter(id = request.session['user_id'])
    book = Book.objects.all().order_by('-created_at')
    book_list = [book[0],book[1],book[2]]
    review = Review.objects.all().order_by('-created_at')
    unique_book_id = []
    unique_review = []
    count = 0
    for i in review:
        if i.book.id not in unique_book_id:
            if count < 3:
                unique_book_id.append(i.book.id)
                unique_review.append(i)
                count += 1


    context = { 'user': user[0], 'book':book, 'reviews':unique_review, 'book_list': book_list}
    return render(request, 'logregis/success.html', context)

# ---------------------------
#       Adding_Book
# ---------------------------

def add_book(request):
    if 'user_id' not in request.session:
        return redirect('/')
    author = Author.objects.all()
    print len(author)
    if len(author) <= 1:
        author_name = author[0].name
        context = {'author_name':author_name}
        return render(request, 'logregis/add_book.html', context)
    context = {'authors':author}
    print context
    return render(request, 'logregis/add_book.html', context)

# ---------------------------
#           View Book
# ---------------------------

def view_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    book = Book.objects.filter(id = book_id)
    if len(book) <= 0:
        return render(request, 'logregis/no_book.html')
    reviews = Review.objects.filter(book__id = book_id).order_by("-created_at")
    if len(reviews) < 1:
        context = {'book':book[0], 'reviews': reviews[0]}
        return render(request, 'logregis/view_book.html', context)

    context = {'book':book[0], 'reviews': reviews}
    return render(request, 'logregis/view_book.html', context)

# ---------------------------
#           View User
# ---------------------------

def view_user(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.filter(id = user_id)
    if len(user) <= 0:
        return render(request, 'logregis/no_user.html')
    print user
    reviews = Review.objects.filter(user__id = user_id)

    books = Review.objects.filter(user__id = user_id)
    book_list = []
    for books in books:
        if books.book not in book_list:
            book_list.append(books.book)

    print book_list
    context = {'user':user[0], 'total_reviews': len(reviews), 'book_list': book_list}

    return render(request, 'logregis/view_user.html', context)

# ==============================================================================
#                                   Process
# ==============================================================================

# ---------------------------
#       Registration
# ---------------------------

def registration(request):
    if 'user_id' in request.session:
        return redirect('/success')

    if request.method == 'POST':
        reg_data = User.objects.reg_validator(request.POST)
        if reg_data[0]:
            request.session['user_id'] = reg_data[1].id
            return redirect('/success')

        for error in reg_data[1]:
            messages.add_message(request, messages.INFO ,error)
    return redirect('/register')

# ---------------------------
#           Login
# ---------------------------

def login(request):
    if 'user_id' in request.session:
        return redirect('/success')

    if request.method == 'POST':
        login_data = User.objects.login_validate(request.POST)

        if login_data[0]:
            request.session['user_id'] = login_data[1].id
            return redirect('/success')

        for error in login_data[1]:
            messages.add_message(request, messages.INFO ,error)
    return redirect('/')

# ---------------------------
#           Logout
# ---------------------------

def logout(request):
    if 'user_id' in request.session:
        messages.add_message(request, messages.INFO ,"You're Successfully Logged Out")
    else:
        messages.add_message(request, messages.INFO ,"You're Already logged Out")
    request.session.flush()
    return redirect('/')

# ---------------------------
#        Adding_Book
# ---------------------------

def adding_book(request):
    if 'user_id' not in request.session:
        return redirect('/')

    if request.method == 'POST':
        user_id = request.session['user_id']
        B1 = Book.objects.adding_book(request.POST, user_id)
        if not B1[0]:
            for error in B1[1]:
                messages.add_message(request, messages.INFO ,error)
            return redirect('/add_book')

        return redirect('/books/{}'.format(B1[1].id))
    return redirect('/add_book')

# ---------------------------
#        Adding Review
# ---------------------------

def adding_review(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')

    if request.method == 'POST':
        user_id = request.session['user_id']
        B1 = Review.objects.adding_review(book_id, user_id, request.POST)
        for error in B1[1]:
            messages.add_message(request, messages.INFO ,error)
        return redirect('/books/{}'.format(book_id))
