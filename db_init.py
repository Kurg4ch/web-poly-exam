# electronic_library/db_init.py

# Импортируем app напрямую, а db из extensions.py
from app import app
from extensions import db # <-- Изменено
from models import Role, User, Genre, Book, Cover # Добавил Cover, чтобы db.create_all() ее видел

# Импорты для данных
from werkzeug.security import generate_password_hash
from datetime import datetime
import os # Для удаления файла db

with app.app_context():
    # Удаляем старую базу данных, если существует, для чистого запуска
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    if os.path.exists(db_path):
        print(f"Удаление существующей базы данных: {db_path}")
        os.remove(db_path)
    else:
        # Убедимся, что папка instance существует, если файл db не существует
        instance_dir = os.path.dirname(db_path)
        if not os.path.exists(instance_dir):
            os.makedirs(instance_dir)


    print("Создание таблиц базы данных...")
    db.create_all() # Создаем все таблицы
    print("Таблицы созданы.")

    # Проверяем, существуют ли уже роли
    if not Role.query.first():
        admin_role = Role(name='admin', description='Суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг')
        moderator_role = Role(name='moderator', description='Может редактировать данные книг и производить модерацию рецензий')
        user_role = Role(name='user', description='Может оставлять рецензии')
        db.session.add_all([admin_role, moderator_role, user_role])
        db.session.commit()
        print("Роли добавлены.")
    else:
        print("Роли уже существуют.")

    # Добавляем тестового администратора, если его нет
    if not User.query.filter_by(login='admin').first():
        admin_role = Role.query.filter_by(name='admin').first()
        admin_user = User(
            login='admin',
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович',
            role=admin_role
        )
        admin_user.set_password('adminpass') # Пароль для администратора
        db.session.add(admin_user)
        db.session.commit()
        print("Тестовый администратор добавлен: login=admin, password=adminpass")
    else:
        print("Тестовый администратор уже существует.")

    # Добавляем тестового пользователя
    if not User.query.filter_by(login='user').first():
        user_role = Role.query.filter_by(name='user').first()
        test_user = User(
            login='user',
            first_name='Петр',
            last_name='Петров',
            patronymic='Петрович',
            role=user_role
        )
        test_user.set_password('userpass') # Пароль для пользователя
        db.session.add(test_user)
        db.session.commit()
        print("Тестовый пользователь добавлен: login=user, password=userpass")
    else:
        print("Тестовый пользователь уже существует.")

    # Добавляем тестового модератора
    if not User.query.filter_by(login='moderator').first():
        moderator_role = Role.query.filter_by(name='moderator').first()
        test_moderator = User(
            login='moderator',
            first_name='Сергей',
            last_name='Сергеев',
            patronymic='Сергеевич',
            role=moderator_role
        )
        test_moderator.set_password('modpass') # Пароль для модератора
        db.session.add(test_moderator)
        db.session.commit()
        print("Тестовый модератор добавлен: login=moderator, password=modpass")
    else:
        print("Тестовый модератор уже существует.")

    # Добавляем несколько тестовых жанров
    test_genres = ['Фантастика', 'Детектив', 'Фэнтези', 'Научная литература', 'Классика', 'Роман', 'Исторический', 'Драма']
    for genre_name in test_genres:
        if not Genre.query.filter_by(name=genre_name).first():
            new_genre = Genre(name=genre_name)
            db.session.add(new_genre)
            db.session.commit()
            print(f"Жанр '{genre_name}' добавлен.")
        else:
            print(f"Жанр '{genre_name}' уже существует.")

    # Добавим тестовую книгу (для удобства, если нет данных)
    if not Book.query.first():
        try:
            fantasy_genre = Genre.query.filter_by(name='Фэнтези').first()
            if not fantasy_genre:
                fantasy_genre = Genre(name='Фэнтези')
                db.session.add(fantasy_genre)
                db.session.commit()

            test_book = Book(
                title='Магический Замок',
                short_description='Краткое описание магического замка. Здесь много интересного текста **жирным шрифтом** и *курсивом*. Можно использовать списки: \n* Элемент 1\n* Элемент 2',
                publication_year=2020,
                publisher='Фэнтези-издательство',
                author='Анна Грин',
                pages=350
            )
            db.session.add(test_book)
            db.session.flush() # Для получения ID книги

            test_book.genres.append(fantasy_genre)
            db.session.commit()
            print("Тестовая книга добавлена.")
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при добавлении тестовой книги: {e}")
    else:
        print("Тестовая книга уже существует.")

    print("База данных инициализирована.")