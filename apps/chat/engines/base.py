from abc import ABC, abstractmethod
from typing import List, Dict


class BaseChatEngine(ABC):
    @abstractmethod
    def generate_reply(self, topic: str, messages: List[Dict]) -> str:
        """
        Generate a reply based on the provided messages.

        :param messages: List of message dictionaries containing 'role' and 'content'.
        :return: Generated reply as a string.
        """
        pass
