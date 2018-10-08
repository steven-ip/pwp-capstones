class User(object):
    def __init__(self, name, email):
        if email.find("@") < 0 or (not email.endswith(".com") and not email.endswith(".edu") and not email.endswith(".org")):
            raise Exception('Invalid email ' + email)
        else:
            self.name = name
            self.email = email
            self.books = {} # Book -> rating

    def get_email(self):
        return self.email

    def change_email(self, address):
        old_email = self.email
        self.email = address
        print("Email {old_email} changed to {new_email}".format(old_email=old_email, new_email=self.email))

    def __repr__(self):
        return "User {name}, email: {email}, books read: {book_read}".format(name=self.name, email=self.email, book_read=str(len(self.books)))

    def __eq__(self, other_user):
        if isinstance(other_user, User) and self.name == other_user.name and self.email == other_user.email:
            return True
        else: return False

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        total = 0
        count = 0
        for r in self.books.values():
            try:
                total += float(r)
                count += 1
            except: pass
        return total / count if count > 0 else 0

class Book():
    def __init__(self, title, isbn, price=0):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        self.isbn = isbn
        print("ISBN updated to {}".format(self.isbn))

    def add_rating(self, rating):
        try:
            if rating >= 0 and rating <= 4:
                self.ratings.append(rating)
            else:
                print("Invalid Rating")
        except: pass

    def __eq__(self, other_book):
        if isinstance(other_book, Book) and self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else: return False

    def get_average_rating(self):
        totalrate = 0
        for rating in self.ratings:
            totalrate += rating
        return totalrate / len(self.ratings) if len(self.ratings) > 0 else 0

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return "Book: {title}, {isbn}".format(title=self.title, isbn=self.isbn)

class Fiction(Book):
    def __init__(self, title, author, isbn, price=0):
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price=0):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)

class TomeRater:
    def __init__(self):
        self.users = {} # email -> User
        self.books = {} # Book -> no. of reader

    def __repr__(self):
        return "Tome Rater no. of users {nuser}, no. of books {nbook}".format(nuser=len(self.users), nbook=len(self.books))

    def __eq__(self, other_tr):
        eqflag = True
        if not isinstance(other_tr, TomeRater): eqflag = False
        if len(self.users) != len(other_tr.users): eqflag = False
        if len(self.books) != len(other_tr.books): eqflag = False
        for email in self.users:
            if other_tr.users.get(email) is None:
                eqflag = False
            else:
                if self.users[email] != other_tr.users.get(email):
                    eqflag = False
        for book in self.books:
            if other_tr.books.get(book) is None:
                eqflag = False
            else:
                if self.books[book] != other_tr.books[book]:
                    eqflag = False
        return eqflag

    def exist_isbn(self, isbn):
        exist = False
        for book in self.books:
            if book.get_isbn() == isbn:
                exist = True
        return exist

    def create_book(self, title, isbn, price=0):
        return Book(title, isbn, price)

    def create_novel(self, title, author, isbn, price=0):
        return Fiction(title, author, isbn, price)

    def create_non_fiction(self, title, subject, level, isbn, price=0):
        return Non_Fiction(title, subject, level, isbn, price)

    def add_book_to_user(self, book, email, rating=None):
        if email not in self.users:
            print("No user with email {email}!".format(email=email))
        else:
            self.users[email].read_book(book, rating)
            book.add_rating(rating)
            if book in self.books:
                self.books[book] += 1
            else:
                if self.exist_isbn(book.get_isbn()):
                    raise Exception("ISBN already exist {}".format(book.get_isbn()))
                else:
                    self.books[book] = 1
    
    def add_user(self, name, email, user_books=None):
        user = self.users.get(email)
        if user:
            raise Exception("User already added: {}".format(user))
        else:
            self.users[email] = User(name, email)
        if user_books:
            for book in user_books:
                self.add_book_to_user(book, email)

    def print_catalog(self):
        for book in self.books:
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def most_read_book(self): # function name provided from instruction
        return self.get_most_read_book()

    def get_most_read_book(self):
        #maxread = -1
        #maxbook = None
        #for book in self.books:
        #    if self.books[book] > maxread:
        #        maxread = self.books[book]
        #        maxbook = book
        #return maxbook
        books = self.get_n_most_read_books(1)
        return books[0] if len(books) > 0 else None

    def get_n_most_read_books(self, n):
        mostbooks = []
        read_books = {} # no. of reader -> Book list
        for book in self.books:
            read = self.books[book]
            if read in read_books:
                read_books[read].append(book)
            else:
                read_books[read] = [book]
        for r in sorted(read_books, reverse=True):
            for book in read_books[r]:
                if len(mostbooks) < n:
                    mostbooks.append(book)
                else: break
        return mostbooks

    def highest_rated_book(self):
        highrate = -1
        highbook = None
        for book in self.books:
            if book.get_average_rating() > highrate:
                highrate = book.get_average_rating()
                highbook = book
        return highbook

    def most_positive_user(self):
        highrate = -1
        highuser = None
        for user in self.users.values():
            if user.get_average_rating() > highrate:
                highrate = user.get_average_rating()
                highuser = user
        return highuser

    def get_n_most_prolific_readers(self, n):
        mostusers = []
        nbook_users = {} # no. of books read -> User list
        for user in self.users.values():
            nbook = len(user.books)
            if nbook in nbook_users:
                nbook_users[nbook].append(user)
            else:
                nbook_users[nbook] = [user]
        for nbook in sorted(nbook_users, reverse=True):
            for user in nbook_users[nbook]:
                if len(mostusers) < n:
                    mostusers.append(user)
                else: break
        return mostusers

    def get_n_most_expensive_books(self, n):
        exp_books = []
        price_books = {} # price -> Book list
        for book in self.books:
            price = book.price
            if price in price_books:
                price_books[price].append(book)
            else:
                price_books[price] = [book]
        for pr in sorted(price_books, reverse=True):
            for book in price_books[pr]:
                if len(exp_books) < n:
                    exp_books.append(book)
                else: break
        return exp_books

    def get_worth_of_user(self, user_email):
        cost = 0
        user = self.users.get(user_email)
        if user:
            for book in user.books:
                cost += book.price
        return cost
