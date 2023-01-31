from enum import Enum

#===================================
class ModelType(Enum):
#===================================
    TRANSFORMER = 'transformer'
    AUTOREG_TRANSFORMER = 'autoreg_transformer'

    def is_autoregressive(self) -> bool:
        """
        Returns: bool: Whether the model is autoregressive.
        """
        return self in {ModelType.AUTOREG_TRANSFORMER}