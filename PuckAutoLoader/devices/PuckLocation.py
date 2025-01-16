class PuckLocation:
    def __init__(self, coord, background_value, detection_status, location, location_name):
        """
        Puck 클래스 초기화
        :param coord: 좌표값 (예: (x, y))
        :param background_value:  백그라운드 값 (예: 168, 205)
        :param detection_status: 감지 여부 (0 또는 1)
        :param location: 위치 (예: 147, 153 )
        :param location_name: 위치 이름 (예: '1A', '2D')
        :param current_value:  현재 값 (예: 168, 205)
        """
        self.coord = coord
        self.background_value = background_value
        self.detection_status = detection_status
        self.location = location
        self.location_name = location_name
        self.current_value = 0

    def set_current_value(self, value):
        """현재 값 저장"""
        self.current_value = value