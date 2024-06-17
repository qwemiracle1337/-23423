import psycopg2
from psycopg2 import sql

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="library_db_new",
            user="postgres",
            password="ugebug00",
            host="localhost",
            port="5433"
        )
        return conn
    except Exception as e:
        print("Ошибка подключения к базе данных:", e)
        return None

def add_reader(last_name, phone_number, library_card_number, reading_hall_id):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            # Проверяем существование читального зала
            cur.execute("""
                SELECT COUNT(*) FROM ReadingHalls WHERE ID = %s;
            """, (reading_hall_id,))
            count = cur.fetchone()[0]
            if count == 0:
                print("Ошибка: Читального зала с указанным ID не существует.")
            else:
                # Добавляем читателя
                cur.execute("""
                    INSERT INTO Readers (LastName, PhoneNumber, LibraryCardNumber, ReadingHallID)
                    VALUES (%s, %s, %s, %s);
                """, (last_name, phone_number, library_card_number, reading_hall_id))
                conn.commit()
                print("Читатель успешно добавлен.")
        except Exception as e:
            print("Ошибка при добавлении читателя:", e)
        finally:
            cur.close()
            conn.close()


def add_reading_hall(reading_hall_id, number, name, capacity):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO ReadingHalls (ID, Number, Name, Capacity)
                VALUES (%s, %s, %s, %s);
            """, (reading_hall_id, number, name, capacity))
            conn.commit()
            cur.close()
        except Exception as e:
            print("Ошибка при добавлении читального зала:", e)
        finally:
            conn.close()

reading_hall_id = input("Введите ID читального зала: ")
number = input("Введите номер зала: ")
name = input("Введите название зала: ")
capacity = input("Введите вместимость зала: ")

add_reading_hall(reading_hall_id, number, name, capacity)

def assign_book_to_reader(book_id, reader_id):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO AssignedBooks (BookID, ReaderID, DateAssigned)
                VALUES (%s, %s, CURRENT_DATE);
            """, (book_id, reader_id))
            conn.commit()
            cur.close()
        except Exception as e:
            print("Ошибка при закреплении книги за читателем:", e)
        finally:
            conn.close()

def add_book(author, title, publication_year, code):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Books (Author, Title, PublicationYear, Code)
                VALUES (%s, %s, %s, %s);
            """, (author, title, publication_year, code))
            conn.commit()
            cur.close()
        except Exception as e:
            print("Ошибка при добавлении книги:", e)
        finally:
            conn.close()

def delete_old_book(book_id):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                DELETE FROM Books WHERE ID = %s;
            """, (book_id,))
            conn.commit()
            cur.close()
        except Exception as e:
            print("Ошибка при удалении книги:", e)
        finally:
            conn.close()

def update_book_code(book_id, new_code):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE Books SET Code = %s WHERE ID = %s;
            """, (new_code, book_id))
            conn.commit()
            cur.close()
        except Exception as e:
            print("Ошибка при обновлении шифра книги:", e)
        finally:
            conn.close()

def get_books_by_author(author):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT Title FROM Books WHERE Author = %s;
            """, (author,))
            books = cur.fetchall()
            cur.close()
            return books
        except Exception as e:
            print("Ошибка при получении книг по автору:", e)
        finally:
            conn.close()

def get_book_code(title):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT Code FROM Books WHERE Title = %s;
            """, (title,))
            code = cur.fetchone()
            cur.close()
            return code
        except Exception as e:
            print("Ошибка при получении шифра книги:", e)
        finally:
            conn.close()

def get_books_assigned_to_reader(reader_id):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT Books.Title FROM AssignedBooks
                JOIN Books ON AssignedBooks.BookID = Books.ID
                WHERE AssignedBooks.ReaderID = %s;
            """, (reader_id,))
            books = cur.fetchall()
            cur.close()
            return books
        except Exception as e:
            print("Ошибка при получении книг, закрепленных за читателем:", e)
        finally:
            conn.close()

if __name__ == "__main__":
    while True:
        print("\nМеню:")
        print("1. Добавить нового читателя")
        print("2. Закрепить книгу за читателем")
        print("3. Добавить новую книгу")
        print("4. Удалить старую книгу")
        print("5. Обновить шифр книги")
        print("6. Получить книги по автору")
        print("7. Получить шифр книги по названию")
        print("8. Получить книги, закрепленные за читателем")
        print("9. Выйти")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            last_name = input("Введите фамилию читателя: ")
            phone_number = input("Введите номер телефона: ")
            library_card_number = input("Введите номер читательского билета: ")
            reading_hall_id = input("Введите ID читального зала: ")
            add_reader(last_name, phone_number, library_card_number, reading_hall_id)
        
        elif choice == "2":
            book_id = input("Введите ID книги: ")
            reader_id = input("Введите ID читателя: ")
            assign_book_to_reader(book_id, reader_id)
        
        elif choice == "3":
            author = input("Введите автора книги: ")
            title = input("Введите название книги: ")
            publication_year = input("Введите год издания: ")
            code = input("Введите шифр книги: ")
            add_book(author, title, publication_year, code)
        
        elif choice == "4":
            book_id = input("Введите ID книги: ")
            delete_old_book(book_id)
        
        elif choice == "5":
            book_id = input("Введите ID книги: ")
            new_code = input("Введите новый шифр книги: ")
            update_book_code(book_id, new_code)
        
        elif choice == "6":
            author = input("Введите автора: ")
            books = get_books_by_author(author)
            print("Книги автора", author, ":", books)
        
        elif choice == "7":
            title = input("Введите название книги: ")
            code = get_book_code(title)
            print("Шифр книги", title, ":", code)
        
        elif choice == "8":
            reader_id = input("Введите ID читателя: ")
            books_assigned = get_books_assigned_to_reader(reader_id)
            print("Книги, закрепленные за читателем", reader_id, ":", books_assigned)
        
        elif choice == "9":
            break
        
        else:
            print("Неверный выбор, попробуйте снова.")
