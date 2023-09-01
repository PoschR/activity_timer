from abc import ABC, abstractmethod


class SpotLight(ABC):
    @abstractmethod
    def light_on_me(self):
        pass

    @abstractmethod
    def light_leaves_me(self):
        pass
