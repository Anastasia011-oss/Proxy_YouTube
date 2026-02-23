from abc import ABC, abstractmethod
import time


class ThirdPartyYouTubeLib(ABC):

    @abstractmethod
    def listVideos(self):
        pass

    @abstractmethod
    def getVideoInfo(self, video_id):
        pass

    @abstractmethod
    def downloadVideo(self, video_id):
        pass


class ThirdPartyYouTubeClass(ThirdPartyYouTubeLib):

    def listVideos(self):
        self._simulate_network_latency()
        print("Получение списка видео с YouTube")
        return ["video1", "video2", "video3"]

    def getVideoInfo(self, video_id):
        self._simulate_network_latency()
        print(f"Получение информации о видео {video_id}")
        return {"id": video_id, "title": "Some Video"}

    def downloadVideo(self, video_id):
        self._simulate_network_latency()
        print(f"Скачивание видео {video_id}")

    def _simulate_network_latency(self):
        time.sleep(1)


class CachedYouTubeClass(ThirdPartyYouTubeLib):

    def __init__(self, s: ThirdPartyYouTubeLib):
        self.service = s
        self.list_cache = None
        self.video_cache = {}

    def listVideos(self):
        if self.list_cache is None:
            print("Кэш пуст. Запрос к реальному сервису...")
            self.list_cache = self.service.listVideos()
        else:
            print("Возвращаем список видео из кэша")
        return self.list_cache

    def getVideoInfo(self, video_id):
        if video_id not in self.video_cache:
            print("Информация отсутствует в кэше. Запрос к сервису...")
            self.video_cache[video_id] = self.service.getVideoInfo(video_id)
        else:
            print("Возвращаем информацию из кэша")
        return self.video_cache[video_id]

    def downloadVideo(self, video_id):
        self.service.downloadVideo(video_id)


class YouTubeManager:

    def __init__(self, service: ThirdPartyYouTubeLib):
        self.service = service

    def renderVideoPage(self, video_id):
        info = self.service.getVideoInfo(video_id)
        print(f"Страница видео: {info}")

    def renderListPanel(self):
        videos = self.service.listVideos()
        print(f"Список видео: {videos}")


if __name__ == "__main__":

    real_service = ThirdPartyYouTubeClass()
    cached_service = CachedYouTubeClass(real_service)

    manager = YouTubeManager(cached_service)

    manager.renderListPanel()
    manager.renderVideoPage("video1")

    print("\nПовторный вызов:\n")

    manager.renderListPanel()
    manager.renderVideoPage("video1")