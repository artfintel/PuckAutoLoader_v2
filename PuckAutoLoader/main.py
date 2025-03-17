import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap, QFont

from PuckAutoLoader.devices.ContainerManager import ContainerManager
from PuckAutoLoader.devices.VideoProcessor import VideoProcessor
from PuckAutoLoader.devices.Video import Video
from PuckAutoLoader.utils.ConfigHandler import ConfigHandler
from PuckAutoLoader.db.DBManager import DBManager
from PuckAutoLoader.ui.main_ui import Main_UI

class VideoApp(QMainWindow):
    """비디오 처리 및 UI 관리를 담당하는 메인 클래스."""

    def __init__(self, src="0"):
        super().__init__()
        self.setWindowTitle("Puck Auto Loader")

        # UI 초기화
        self.ui = Main_UI()
        self.setCentralWidget(self.ui)

        # UI 스타일 설정
        self.styles = {
            "blue": "color: blue; border-style: solid; border-width: 3px; border-color: #1E90FF",
            "red": "color: red; border-style: solid; border-width: 3px; border-color: #DC143C",#FA8072
            "black": "color: black; border-style: solid; border-width: 3px; border-color: #000000",
        }

        # 버튼 연결
        self.ui.filling_btn.clicked.connect(self.filling_mode)
        self.ui.info_btn.clicked.connect(self.toggle_info)
        self.ui.refresh_btn.clicked.connect(self.refresh_db)

        # 바코드 입력 초기화
        self.ui.barcode_input.setReadOnly(True)
        self.ui.barcode_input.setStyleSheet(self.styles["black"])
        self.input_buffer = ""
        self.ui.barcode_input.setFocus()

        # 비디오 프로세서 및 설정 초기화
        self.video_proc = VideoProcessor()
        self.config = ConfigHandler('utils/config.ini').get_config()
        self.video = Video(self.config['CAMERA']['Url'])

        # 비디오 업데이트 타이머 초기화
        self.video_timer = QTimer()
        self.video_timer.timeout.connect(self.update_frame)
        self.video_timer.start(30)  # Update frames every 30 ms

        # 바코드 입력 타이머 초기화
        self.barcode_timer = QTimer()
        self.barcode_timer.timeout.connect(self.auto_submit)
        self.input_timeout = 500  # 0.5 seconds

        # 데이터베이스 매니저 초기화
        self.db_mgr = DBManager(
            self.config['DATABASE']['Host'],
            self.config['DATABASE']['User'],
            self.config['DATABASE']['Password'],
            self.config['DATABASE']['Db']
        )
        self.db_mgr.initialize()

        # 퍽 감지 상태 변수 초기화
        self.detected_flag = 0
        self.loading_puck = ""
        self.unloading_puck = []

        # 컨테이너 매니저 초기화
        self.container_mgr = ContainerManager(self.db_mgr)
        self.container_list = self.container_mgr.get_containers(loaded_only=True)

        # 라벨 타이머 초기화
        self.last_label_timer = QTimer()

    def update_frame(self):
        """UI에 비디오 프레임 업데이트"""
        frame = self.video.read_frame()
        if frame is not None:
            self.puck_detection(frame)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            self.ui.video_label.setPixmap(pixmap)
            self.find_changed_puck()

    def find_changed_puck(self):
        """추가되거나 제거된 퍽을 감지하고 UI 업데이트"""
        detected_pucks = [
            puck for puck in self.video_proc.dewar.puck_locations if puck.detection_status == 1
        ]

        if len(detected_pucks) > len(self.container_list):
            self.handle_puck_addition(detected_pucks, self.container_list, self.styles["blue"])
        elif len(detected_pucks) < len(self.container_list):
            self.handle_puck_removal(detected_pucks, self.container_list, self.styles["red"])
        else:
            self.detected_flag = 0
            self.handle_puck_nothing(self.styles["black"])

    def handle_puck_addition(self, detected_pucks, loaded_containers, style):
        """새 퍽이 감지되면 처리"""
        detected_pucks = [
            puck for puck in detected_pucks
            if not any(puck.location == container.location_id for container in loaded_containers)
        ]
        if detected_pucks:
            self.detected_flag = 1
            self.ui.detected_puck_label.setStyleSheet(style)
            self.ui.detected_puck_label.setText(detected_pucks[0].location_name)
            self.loading_puck = detected_pucks[0]

    def handle_puck_removal(self, detected_pucks, loaded_containers, style):
        """퍽이 제거되면 처리"""
        loaded_containers = [
            container for container in loaded_containers
            if not any(puck.location == container.location_id for puck in detected_pucks)
        ]
        unload_list = " ".join(
            puck.location_name for container in loaded_containers
            for puck in self.video_proc.dewar.puck_locations
            if container.location_id == puck.location
        )
        font_size = max(20, 30 - len(loaded_containers) * 3)
        self.ui.detected_puck_label.setFont(QFont("SansSerif", font_size, QFont.Bold))
        self.detected_flag = -1
        self.ui.detected_puck_label.setStyleSheet(style)
        self.ui.detected_puck_label.setText(unload_list.strip())
        self.unloading_puck = [
            puck for container in loaded_containers
            for puck in self.video_proc.dewar.puck_locations
            if container.location_id == puck.location
        ]

    def handle_puck_nothing(self, style):
        """퍽의 변화가 없을때 처리"""
        self.ui.detected_puck_label.setStyleSheet(style)
        self.ui.detected_puck_label.setText("--")

    def puck_detection(self, frame):
        """현재 프레임에서 퍽의 변화 감지"""
        self.video_proc.puck_detection(frame)

    def keyPressEvent(self, event):
        """바코드 입력 이벤트 처리"""
        key = event.text()
        self.ui.barcode_input.setText("")
        if key.isprintable():
            self.input_buffer += key
            self.restart_timer()
        elif event.key() == 16777220:  # Enter key
            self.auto_submit()

    def restart_timer(self):
        """바코드 입력 타이머 재시작"""
        self.barcode_timer.stop()
        self.barcode_timer.start(self.input_timeout)

    def auto_submit(self):
        """바코드 입력 자동 제출"""
        self.barcode_timer.stop()
        self.submit_input()

    def submit_input(self):
        """바코드 입력 체출 및 처리"""
        if self.input_buffer:
            if self.detected_flag == 1: # 듀어에 추가된 퍽이 있는 경우
                if self.container_mgr.check_container(self.input_buffer):
                    self.container_mgr.load_container(self.input_buffer, self.loading_puck.location)
                    self.update_label(self.ui.state_label, str(self.loading_puck.location_name)+" 위치에 "+str(self.input_buffer) +" 퍽이 등록되었습니다.", 10)
                else:
                    self.update_label(self.ui.state_label, "퍽의 이름이 잘못되었거나 등록되지 않은 이름입니다.", 10)

            elif self.detected_flag == -1: # 듀어에 제거된 퍽이 있는 경우
                for puck in self.unloading_puck:
                    self.container_mgr.unload_container_by_location(puck.location)
                self.update_label(self.ui.state_label, "퍽이 제거되었습니다.", 10)

            else: # 듀어에 퍽의 변화가 없는 경우
                self.update_label(self.ui.state_label, "변경된 퍽이 없습니다.",10)

            self.update_label(self.ui.barcode_input, self.input_buffer, 3)
            #self.ui.barcode_input.setText(self.input_buffer)
            self.input_buffer = ""  # Clear the input buffer
            # 데이터베이스에서 변경된 컨테이너 정보 가져오기
        self.container_list = self.container_mgr.get_containers(loaded_only=True)

    def filling_mode(self):
        """액체질소 필링 모드 처리"""
        self.update_label(self.ui.state_label, "액체질소 필링 상태 켜기.", 5)
        self.video_proc.set_background()
        self.ui.barcode_input.setText("")

    def toggle_info(self):
        """각 퍽의 위치의 픽셀 정보 표시"""
        self.video_proc.info = not self.video_proc.info
        self.update_label(self.ui.state_label, "이미지 분석 값을 수치로 표시합니다.", 5)
        self.ui.barcode_input.setText("")

    def refresh_db(self):
        """데이터베이스 정보 새로 고침"""
        self.update_label(self.ui.state_label, "데이터 데이스 정보를 새로 가져옵니다.", 5)
        self.ui.barcode_input.setText("")
        try:
            self.container_list = self.container_mgr.get_containers(loaded_only=True)
        except Exception as e:
            print(e)

    def update_label(self, label, text, timeout=60):
        """
        라벨 텍스트 업데이트 후 일정 시간 후 초기화 처리
        """
        label.setText(text)

        self.last_label_timer.stop()

        # 새 타이머 설정
        label_timer = QTimer(self)
        label_timer.setSingleShot(True)
        label_timer.timeout.connect(lambda: self.clear_label(label))
        label_timer.start(timeout * 1000)

        self.last_label_timer = label_timer

    def clear_label(self, label):
        """
        라벨 텍스트 초기화
        """
        label.setText("")

    def closeEvent(self, event):
        """창이 닫힐때 리소스 해제"""
        self.video.release()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = VideoApp()
    main_window.show()
    sys.exit(app.exec_())
