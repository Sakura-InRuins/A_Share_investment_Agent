from abc import abstractmethod
from typing import List, Dict, Optional

from src.llm.types import NotGiven, NOT_GIVEN, CompletionMessage


class BaseClient:
    """ Base class for chat models client. """

    @abstractmethod
    def completions(self,
                    messages: List[Dict[str, str]],
                    model: Optional[str] | NotGiven = NOT_GIVEN,
                    ) -> str:
        """Chat with the model.
        """
