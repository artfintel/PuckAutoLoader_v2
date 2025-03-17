import re

from PuckAutoLoader.devices.Container import Container


class ContainerManager:
    """
    컨테이너 관련 작업(로드, 언로드, 상태 확인 등)을 관리하는 클래스.
    """

    def __init__(self, db_mgr):
        """
        ContainerManager를 데이터베이스 매니저와 함께 초기화.

        Args:
            db_mgr: 데이터베이스와 상호작용하기 위한 DBManager 인스턴스.
        """
        self.db_mgr = db_mgr
        self.refined_container_list = []
        self.update_refined_container_list()

    def get_containers(self, loaded_only=False):
        """
        데이터베이스에서 컨테이너 목록을 가져와 Container 객체로 변환.

        Args:
            loaded_only (bool): 로드된 컨테이너만 가져올지 여부.

        Returns:
            list: Container 객체의 리스트.
        """
        query = (
            "SELECT name, location_id, parent_id FROM lims_container "
            "WHERE status=2"
        )
        if loaded_only:
            query += " AND location_id IS NOT NULL"
        query += " ORDER BY name"

        containers = self.db_mgr.select_db(query)
        print(containers)
        return self._create_containers(containers)

    def _create_containers(self, container_data):
        """
        컨테이너 데이터를 기반으로 Container 객체 리스트 생성.

        Args:
            container_data (list): 데이터베이스에서 가져온 컨테이너 데이터.

        Returns:
            list: Container 객체의 리스트.
        """
        return [Container(name, location_id, parent_id) for name, location_id, parent_id in container_data]

    def load_container(self, name, location_id):
        """
        특정 위치에 컨테이너를 로드.

        Args:
            name (str): 로드할 컨테이너의 이름.
            location_id (int): 컨테이너를 로드할 위치의 ID.
        """
        container_name = self.get_refined_container_name(name)
        self.db_mgr.update_db(
            "UPDATE lims_container SET location_id=%s, parent_id=1 WHERE name=%s AND status=2",
            (location_id, container_name)
        )

    def unload_container(self, name):
        """
        컨테이너의 위치와 부모 ID를 초기화하여 언로드.

        Args:
            name (str): 언로드할 컨테이너의 이름.

        Returns:
            bool: 작업이 성공했는지 여부.
        """
        self.db_mgr.update_db(
            "UPDATE lims_container SET location_id=DEFAULT, parent_id=DEFAULT WHERE name=%s",
            (name,)
        )
        return True

    def unload_container_by_location(self, location_id):
        """
        특정 위치 ID에 따라 컨테이너를 언로드.

        Args:
            location_id (int): 언로드할 위치의 ID.

        Returns:
            bool: 작업이 성공했는지 여부.
        """
        self.db_mgr.update_db(
            "UPDATE lims_container SET location_id=DEFAULT, parent_id=DEFAULT WHERE location_id=%s",
            (location_id,)
        )
        return True

    def check_container(self, name):
        """
        데이터베이스에 컨테이너가 존재하는지 확인.

        Args:
            name (str): 확인할 컨테이너의 이름.

        Returns:
            bool: 컨테이너가 존재하면 True, 그렇지 않으면 False.
        """
        try:
            container_name = self.get_refined_container_name(name)
            return any(
                container.name == container_name for container in self.get_containers()
            )
        except ValueError:
            return False


    def update_refined_container_list(self):
        """
        현재 데이터베이스 상태에 따라 정제된 컨테이너 목록을 업데이트.
        """
        self.refined_container_list = [
            self._clean_text(container.name.upper())
            for container in self.get_containers()
        ]

    def get_refined_container_name(self, name):
        """
        입력된 이름을 기반으로 정제된 컨테이너 이름을 가져옴.

        Args:
            name (str): 원본 컨테이너 이름.

        Returns:
            str: 정제된 컨테이너 이름.

        Raises:
            ValueError: 정제된 리스트에서 컨테이너 이름을 찾을 수 없는 경우.
        """
        cleaned_name = self._clean_text(name.upper())
        index = self.refined_container_list.index(cleaned_name)
        return self.get_containers()[index].name

    @staticmethod
    def _clean_text(original_text):
        """
        문자열에서 모든 비알파벳 및 비숫자 문자를 제거.

        Args:
            original_text (str): 정리할 텍스트.

        Returns:
            str: 정리된 텍스트.
        """
        return re.sub(r"[^a-zA-Z0-9]", "", original_text)
