import psycopg2


class PostgreSQL:
    conn = None
    cur = None

    def __init__(self) -> None:
        print("Инициализирован объект БД.")

    def connect(self) -> None:
        self.conn = psycopg2.connect('postgresql://postgres:postgres@localhost:54321/sto')  # Создание объекта соединения с базой данных PostgreSQL
        print("Соединение с сервером БД установлено.")

    def init_cursor(self) -> None:
        self.cur = self.conn.cursor()  # Создание объекта курсора для работы с запросами

    def execute_query(self, query: str, fetch_type: str = 'one', commit: bool = True):
        self.cur.execute(query)  # Выполняем запрос
        if fetch_type == 'one':  # Если надо получить одну запись
            result = self.cur.fetchone()
        elif fetch_type == 'all':  # Если надо получить все записи
            result = self.cur.fetchall()
        if commit:  # Если надо зафиксировать изменения
            self.conn.commit()
        return result

    def close_cursor(self) -> None:
        self.cur.close()  # Закрытие курсора

    def close_connection(self) -> None:
        self.conn.close()  # Закрытие соединения
