import cv2

class Video:
    """OpenCV를 활용하여 비디오 이미지를 가져올 클래스"""
    def __init__(self, source="0"):
        """
        비디오 서버 초기화
        source가 입력되지 않으면 기본 값으로 로컬 비디오를 읽어옴.
        """
        self.capture = cv2.VideoCapture(source)

    def read_frame(self):
        """비디오 소스로 부터 프레임을 가져오기"""
        if self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width = frame.shape[:2]
                frame = cv2.resize(frame, (width // 2, height // 2))  # 이미지를 절반 사이즈로 조절
                frame = self.show_video_roi(frame, 360, 50, 560, 500) # 원하는 영역만 보기
                return frame
        return None

    def release(self):
        """비디오 리소스 해제"""
        if self.capture:
            self.capture.release()

    def show_video_roi(self, frame, x, y, width, height):
        """비디오 프레임의 특정 영역만 가져오기"""
        roi = frame[y:y+height, x:x+width]
        frame = roi.copy()

        return frame