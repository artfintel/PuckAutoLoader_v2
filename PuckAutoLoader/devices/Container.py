class Container:
    def __init__(self, name, location_id, parent_id):
        """
        Container 클래스 초기화
        Puck을 DB에서의 명칭인 Container로 사용
        :param name: 컨테이너 이름
        :param location_id:  컨테이너 위치
        :param parent_id:
        """
        super().__init__()

        self.name = name
        self.location_id = location_id
        self.parent_id = parent_id