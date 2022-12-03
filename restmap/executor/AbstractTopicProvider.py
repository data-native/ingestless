from abc import ABC, abstractclassmethod, abstractstaticmethod, abstractproperty, abstractmethod


class AbstractTopicProvider(ABC):
    """
    TO BE IMPLEMENTED
    """
    # TODO Provide implementation 

    @abstractmethod
    def topic(self, name: str, args: dict):
        raise NotImplementedError

    @abstractmethod
    def use_topic(self, name: str) -> 'AbstractTopicProvider':
        raise NotImplementedError
    
