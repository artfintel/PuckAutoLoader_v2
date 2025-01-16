import pymysql

class DatabaseHandler:
    def __init__(self, host, user, password, database, port=3306):
        """
        데이터베이스 핸들러 초기화

        :param host: 데이터베이스 호스트 주소
        :param user: 데이터베이스 사용자 이름
        :param password: 데이터베이스 비밀번호
        :param database: 사용할 데이터베이스 이름
        :param port: 데이터베이스 포트 (기본값: 3306)
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None

    def connect(self):
        """
        데이터베이스 연결을 설정합니다.
        """
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            print("Database connection established.")
        except pymysql.MySQLError as e:
            print(f"Error connecting to the database: {e}")
            raise

    def reconnect(self):
        """
        데이터 베이스 재연결
        :return:
        """

        self.connection.ping(reconnect=True)

    def execute_query(self, query, params=None):
        """
        데이터베이스에 쿼리를 실행합니다.

        :param query: 실행할 SQL 쿼리
        :param params: 쿼리에 전달할 매개변수 (기본값: None)
        :return: 쿼리 결과
        """
        if self.connection is None:
            raise ConnectionError("Database connection is not established.")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                if query.strip().lower().startswith("select"):
                    result = cursor.fetchall()
                    return result
        except pymysql.MySQLError as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            raise

    def close(self):
        """
        데이터베이스 연결을 닫습니다.
        """
        if self.connection:
            self.connection.close()
            print("Database connection closed.")