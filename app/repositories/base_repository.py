from abc import ABC, abstractmethod

class Create(ABC):
    @abstractmethod
    def create(self, entity):
        pass

class Update(ABC):
    @abstractmethod
    def update(self, entity):
        pass

class Delete(ABC):
    @abstractmethod
    def delete(self, entity):
        pass

class Read(ABC):
    @abstractmethod
    def get_by_id(self, entity_id):
        pass

    @abstractmethod
    def read_all(self):
        pass