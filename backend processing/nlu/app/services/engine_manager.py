from typing import List
from enum import Enum
import logging

from app.schemas import Entity, EntityType, Intent
from app.models.forms import FormEntityType, FormIntent

from app.services.keyword import keyword_matching 
from app.core.logging import LogMessages

# contains the list of NLU engines that can be used 
# NOTE: currently only supports keyword-matching
class EngineName(str, Enum):
    KEYWORD = "keyword-matching"
    LSTM = "lstm"   # not implemented
    BERT = "bert"   # not implemented
    

# Model Manager class to support future implementation of ML models
# NOTE: currently only works for keyword-matching
class EngineManager:
    def __init__(self, engine_name: EngineName = EngineName.KEYWORD):
        """
        Initialise instant of the class and use keyword-matching by default
        """
        self.engine_name = engine_name
        self.logger = logging.getLogger("engine_manager")


    def choose_engine(self, engine_name: EngineName):
        """
        Choose engine to be used for NLU 
        """
        self.engine_name = engine_name


    def get_intents(self, text: str, intent_col: List[FormIntent]) -> List[Intent]:
        """
        Process text to get intent based on selected model 
        """
        if self.engine_name == EngineName.KEYWORD:
            return keyword_matching.get_intents(text, intent_col)
        else:
            self.logger.warning(LogMessages.UNSUPPORTED_MODEL(self.engine_name))
            return []
    

    def get_entity_types(self, text: str, entity_type_col: List[FormEntityType]) -> List[EntityType]:
        """
        Process text to get entity based on selected model 
        """
        if self.engine_name == EngineName.KEYWORD:
            return keyword_matching.get_entity_types(text, entity_type_col)
        else:
            self.logger.warning(LogMessages.UNSUPPORTED_MODEL(self.engine_name))
            return []


    def get_entities(self, text: str, entity_type_doc: FormEntityType) -> List[Entity]:
        """
        Process text to get entity based on selected model 
        """
        if self.engine_name == EngineName.KEYWORD:
            return keyword_matching.get_entities(text, entity_type_doc)
        else:
            self.logger.warning(LogMessages.UNSUPPORTED_MODEL(self.engine_name))
            return []


engine_manager = EngineManager()