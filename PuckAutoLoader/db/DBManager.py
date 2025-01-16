from PuckAutoLoader.db.DatabaseHandler import DatabaseHandler

class DBManager:
    def __init__(self, host, user, password, database, port=3306):
        """
        DatabaseHandler를 사용하기 위한 DBManager 초기화
        :param host: 데이터베이스 호스트 주소
        :param user: 데이터베이스 사용자 이름
        :param password: 데이터베이스 비밀번호
        :param database: 사용할 데이터베이스 이름
        :param port: 데이터베이스 포트 (기본값: 3306)
        """
        super().__init__()

        self.db_handler = DatabaseHandler(host, user, password, database, port)

    def initialize(self):
        """
        데이터베이스 연결 초기화
        """
        self.db_handler.connect()

        print("DB에 연결되었습니다.")

    def reconnect(self):
        """
        데이터베이스 재연결
        :return:
        """
        self.db_handler.reconnect()

    def select_db(self, select_query):
        """
        select_query = "select name, location_id, parent_id from lims_container where status=2 order by name"
        results = db.execute_query(select_query)
        :param select_query: 탐색 쿼리
        :return:
        """

        results = self.db_handler.execute_query(select_query)
        # for row in results:
        #     print(row)
        return results

    def insert_db(self, insert_query, insert_value):
        """
        예졔
        insert_query = "INSERT INTO users (name, age) VALUES (%s, %s)"
        db.execute_query(insert_query, ("Alice", 30))
        :param insert_query: 삽입 쿼리
        :param insert_value: 삽입 옵션
        :return:
        """
        self.db_handler.execute_query(insert_query, insert_value)

    def update_db(self, update_query, update_value):
        """
        update_query = "UPDATE users SET age = %s WHERE name = %s"
        db.execute_query(update_query, (35, "Alice"))
        :param update_query: 수정 쿼리
        :param update_value: 쿼리 옵션
        :return:
        """
        self.db_handler.execute_query(update_query, update_value)

    def close(self):
        """
        데이터베이스 연결 닫기
        :return:
        """
        self.db_handler.close()
