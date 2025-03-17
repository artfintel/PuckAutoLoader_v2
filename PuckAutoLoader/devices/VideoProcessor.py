import cv2 as cv
from PuckAutoLoader.devices.Dewar import Dewar


class VideoProcessor:
    def __init__(self):
        """
        VideoProcessor 초기화
        - Dewar 클래스 인스턴스 생성
        - 기본 감지 박스 크기 및 오프셋 설정
        - 퍽 정보 표시 플래그 초기화
        """
        super().__init__()

        self.dewar = Dewar()
        self.detection_box = 25
        self.offset = 10
        self.info = True

    def puck_detection(self, frame):
        """
        퍽 감지를 수행하는 함수
        :param frame: 비디오 프레임 이미지
        :return: 연산이 완료된 이미지 프레임
        """
        img_gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

        for puck_location in self.dewar.puck_locations:
            coord = tuple(map(int, puck_location.coord))
            puck_location.current_value = int(
                self.calculate_average(img_gray, coord, self.detection_box)
            )
            if puck_location.background_value - puck_location.current_value < self.offset:
                cv.circle(frame, coord, 40, (220, 20, 60), 2)
                puck_location.detection_status = 0
            else:
                cv.circle(frame, coord, 40, (30, 144, 256), 2) #(0, 0, 255)
                puck_location.detection_status = 1

            # 퍽 위치 이름 표시
            cv.putText(
                frame, puck_location.location_name.upper(),
                (coord[0] - 22, coord[1] - 10),
                cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2
            )

            # 퍽 정보 표시
            if self.info:
                value_diff = puck_location.background_value - puck_location.current_value
                if value_diff < self.offset:
                    cv.putText(
                        frame, str(value_diff),
                        (coord[0] - 15, coord[1] + 20),
                        cv.FONT_HERSHEY_SIMPLEX, 0.5, (220, 20, 60), 2
                    )
                else:
                    cv.putText(
                        frame, str(value_diff),
                        (coord[0] - 15, coord[1] + 20),
                        cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 205), 2
                    )

        return frame

    def set_background(self):
        """
        Dewar의 백그라운드 값을 재설정합니다.
        """
        self.dewar.set_background()

    @staticmethod
    def calculate_average(image, center, size):
        """
        특정 영역의 픽셀 값 평균을 계산

        :param image: numpy 배열 형태의 이미지 (H, W)
        :param center: 영역의 중심 좌표 (x, y)
        :param size: 정사각형 영역의 한 변 크기
        :return: 영역 픽셀 값 평균
        """
        x, y = center
        region = image[y - size:y + size, x - size:x + size]
        return region.mean()
