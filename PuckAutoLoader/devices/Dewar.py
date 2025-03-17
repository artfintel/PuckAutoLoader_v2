from PuckAutoLoader.devices.PuckLocation import PuckLocation
from PuckAutoLoader.utils.ConfigHandler import ConfigHandler


class Dewar:
    def __init__(self, config_file='utils/puck_info.ini'):
        """
        Dewar 클래스 초기화

        :param config_file: 퍽 설정 정보를 포함한 INI 파일 경로
        """
        self.background_offset = -10
        self.config = ConfigHandler(config_file).get_config()
        self.puck_locations = [PuckLocation((0, 0), 0, 0, 0, "") for _ in range(29)]
        self._initialize_puck_locations()

    def _initialize_puck_locations(self):
        """
        설정 파일에서 퍽 위치 정보를 가져와 초기화
        """
        for i, puck_location in enumerate(self.puck_locations):
            puck_location.background_value = int(self.config.items('BACKGROUND')[i][1]) + self.background_offset
            puck_location.location = int(self.config.items('LOCATION')[i][1])
            puck_location.location_name = self.config.items('BACKGROUND')[i][0].upper()
            puck_location.coord = tuple(map(int, self.config.items('Coordinate')[i][1].split(',')))

    def set_background(self):
        """
        현재 퍽의 값을 백그라운드 값으로 설정
        설정 파일을 업데이트하여 저장
        """
        for puck_location in self.puck_locations:
            if puck_location.detection_status == 0:
                location_name = puck_location.location_name
                current_value = puck_location.current_value

                self.config['BACKGROUND'][location_name] = str(current_value)
                puck_location.background_value = current_value + self.background_offset

        with open('utils/puck_info.ini', 'w') as config_file:
            self.config.write(config_file)
