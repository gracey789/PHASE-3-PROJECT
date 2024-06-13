
import sqlite3

class MovieDB:
    def __init__(self):
        self.connection = sqlite3.connect('movies.db')
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               title TEXT NOT NULL,
                               director TEXT,
                               year INTEGER,
                               reviews TEXT
                               )''')
        self.connection.commit()
        

    def add_movie(self, title, director, year):
        self.cursor.execute('''INSERT INTO movies (title, director, year)
                               VALUES (?, ?, ?)''', (title, director, year))
        self.connection.commit()
        print(f"Movie '{title}' added.")

    def add_review(self, movie_id, review_text):
        self.cursor.execute('''SELECT reviews FROM movies WHERE id = ?''', (movie_id,))
        current_reviews = self.cursor.fetchone()[0]

        if current_reviews:
            new_reviews = current_reviews + review_text + "\n"
        else:
            new_reviews = review_text + "\n"

        self.cursor.execute('''UPDATE movies SET reviews = ? WHERE id = ?''', (new_reviews, movie_id))
        self.connection.commit()
        print(f"Review added for movie ID {movie_id}.")

    def list_movies(self):
        self.cursor.execute("SELECT * FROM movies")
        return self.cursor.fetchall()

    def delete_movie(self, movie_id):
        self.cursor.execute('''DELETE FROM movies WHERE id = ?''', (movie_id,))
        self.connection.commit()
        print(f"Movie ID {movie_id} deleted.")

    def close(self):
        self.connection.close()


class UserDB :
    def __init__(self):
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               username TEXT NOT NULL,
                               ticket TEXT NOT NULL,
                                ticket_amount INTEGER NOT NULL,
                                gender TEXT NOT NULL
                               )''')
        self.connection.commit()
    
    def add_user(self, username, ticket, ticket_amount, gender):
        self.cursor.execute('''INSERT INTO users (username, ticket, ticket_amount, gender)
                               VALUES (?, ?, ?, ?)''', (username, ticket, ticket_amount, gender))
        self.connection.commit()
        print(f"User '{username}' added.")

    def list_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()
    
    def close(self):
        self.connection.close()

    def get_user(self, username):
        self.cursor.execute('''SELECT * FROM users WHERE username = ?''', (username,))
        return self.cursor.fetchone()
    
    def get_ticket(self, ticket):
        self.cursor.execute('''SELECT * FROM users WHERE ticket = ?''', (ticket,))
        return self.cursor.fetchone()
    
    def get_ticket_amount(self, ticket):
        self.cursor.execute('''SELECT ticket_amount FROM users WHERE ticket = ?''', (ticket,))
        return self.cursor.fetchone()

    def update_ticket_amount(self, ticket, ticket_amount):
        self.cursor.execute('''UPDATE users SET ticket_amount = ? WHERE ticket = ?''', (ticket_amount, ticket))
        self.connection.commit()
        print(f"Ticket amount updated for ticket {ticket}.")

    def update_gender(self, ticket, gender):
        self.cursor.execute('''UPDATE users SET gender = ? WHERE ticket = ?''', (gender, ticket))
        self.connection.commit()
        print(f"Gender updated for ticket {ticket}.")

    def delete_user(self, user_id):
        self.cursor.execute('''DELETE FROM users WHERE ticket = ?''', (user_id,))
        self.connection.commit()
        print(f"User deleted for ticket {user_id,}.")

    def delete_all_users(self):
        self.cursor.execute('''DELETE FROM users''')
        self.connection.commit()
        print(f"All users deleted.")

    def delete_all_tickets(self):
        self.cursor.execute('''DELETE FROM tickets''')
        self.connection.commit()
        print(f"All tickets deleted.")

    def delete_all_movies(self):
        self.cursor.execute('''DELETE FROM movies''')
        self.connection.commit()
        print(f"All movies deleted.")

    def delete_all_reviews(self):
        self.cursor.execute('''DELETE FROM reviews''')
        self.connection.commit()
        print(f"All reviews deleted.")

    def delete_all(self):
        self.delete_all_users()
        self.delete_all_tickets()
        self.delete_all_movies()
        self.delete_all_reviews()

    def close(self):
        self.connection.close()
        


def main_menu():
    while True:
        print("\n1. Movie Operations")
        print("2. User Operations")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            movie_operations()
        elif choice == '2':
            user_operations()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again")

def movie_operations():
    db = MovieDB()
    while True:
        print("\n1. Add Movie")
        print("2. Delete Movie")
        print("3. Add Review to Movie")
        print("4. List Movies")
        print("5. Back to Main Menu")
        choice = input("Enter choice: ")

        if choice == '1':
            add_movie(db)
        elif choice == '2':
            delete_movie(db)
        elif choice == '3':
            add_review(db)
        elif choice == '4':
            list_movies(db)
        elif choice == '5':
            db.close()
            break
        else:
            print("Invalid choice. Please try again")

def add_movie(db):
    title = input("Enter movie title: ")
    director = input("Enter director name: ")
    year = int(input("Enter release year: "))
    db.add_movie(title, director, year)

def delete_movie(db):
    movie_id = input("Enter Movie ID to delete: ")
    if movie_id.isdigit():
        db.delete_movie(int(movie_id))
    else:
        print("Invalid movie ID. Please enter a number.")

def add_review(db):
    movie_id = input("Enter movie ID to review: ")
    if movie_id.isdigit():
        review_text = input("Enter your review: ")
        db.add_review(int(movie_id), review_text)
    else:
        print("Invalid movie ID. Please enter a number.")

def list_movies(db):
    movies = db.list_movies()
    for movie in movies:
        print(f"Movie ID: {movie[0]}, Title: {movie[1]}, Director: {movie[2]}, Year: {movie[3]}")
        if movie[4]:  
            print("Reviews:")
            for review in movie[4].splitlines():
                print(f"  - {review}")

def user_operations():
    db = UserDB()
    while True:
        print("\n1. Add User")
        print("2. Delete User")
        print("3. List Users")
        print("4. Back to Main Menu")
        choice = input("Enter choice: ")

        if choice == '1':
            add_user(db)
        elif choice == '2':
            delete_user(db)
        elif choice == '3':
            list_users(db)
        elif choice == '4':
            db.close()
            break
        else:
            print("Invalid choice. Please try again")

def add_user(db):
    username = input("Enter username: ")
    ticket = input("Enter ticket: ")
    ticket_amount = input("Enter ticket amount: ")
    gender = input("Enter gender: ")
    db.add_user(username, ticket, ticket_amount, gender)
    print(f"User '{username}' added.")

def delete_user(db,):
    username = input("Enter username to delete: ")
    db.delete_user(username)


def list_users(db):
    users = db.list_users()
    if users:
        for user in users:
            print(f"Username: {user[0]}")
    else:
        print("No users found.")

def delete_ticket(user_id):
    db = UserDB()
    db.delete_ticket(user_id)
    db.close()

if __name__ == '__main__':
    main_menu()   