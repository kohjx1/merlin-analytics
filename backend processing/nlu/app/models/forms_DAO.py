import requests
import os
import logging
from typing import Dict, List
from fastapi import HTTPException

from app.core.logging import LogMessages
from app.models.forms import FormIntent, FormEntityType, FormEntity

"""
Implement DAO layer for communication between the Form Manager and the NLU module
"""

class FormDAO:
    def __init__(self):
        self.logger = logging.getLogger("DAO")
        self.FORM_MANAGER_URL = os.getenv("FORM_MANAGER_URL")   # form manager URL

    ###################################################################
    # MODIFY THIS SECTION IF DATA STRUCTURE FROM FORM MANAGER CHANGES 
    ###################################################################
    def cast_as_FormIntent(self, intent_doc: Dict, entity_type_col: List[FormEntityType]) -> FormIntent:
        """
        Cast the raw intent document as a FormIntent object
        """
        entity_types = []
        for entity_type in intent_doc["entity_types"]:
            entity_types.append( self.access_entity_type(entity_type_col, entity_type["entity_type"]) )

        return FormIntent(
            intent=intent_doc["intent"],
            examples=intent_doc["examples"],
            entity_types=entity_types
        )


    def cast_as_FormEntityType(self, entity_type_doc: Dict) -> FormEntityType:
        """
        Cast the raw entity type document as a FormEntityType object
        """
        # get list of associated entities for each entity type
        entities = []
        for entity in entity_type_doc["entities"]:
            entities.append(
                self.cast_as_FormEntity(entity)
            )

        return FormEntityType(
            entity_type=entity_type_doc["entity_type"],
            keywords=entity_type_doc["keywords"],
            isNumeric=entity_type_doc["isNumeric"],
            entities=entities
        )


    def cast_as_FormEntity(self, entity_doc: Dict) -> FormEntity:
        """
        Cast the raw entity document as a FormEntity object
        """
        return FormEntity(
            entity=entity_doc["entity"],
            synonyms=entity_doc["synonyms"]
        )

    ###################################################################
    # END OF SECTION                                                  
    ###################################################################

    def access_intents(self, context: str = None) -> List[FormIntent]:
        """
        Request a list of intent documents from Form Manager and cast it to a 
        list of FormIntent models
        """
        try:
            if context is not None:
                r = requests.get(self.FORM_MANAGER_URL + "/intents/" + context)
            else:
                r = requests.get(self.FORM_MANAGER_URL + "/intents")
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error(LogMessages.REQUEST_EXCEPTION(e))
            raise HTTPException(status_code=400, detail="Unable to establish connection with Form Manager")
        except Exception as e:
            self.logger.error(LogMessages.FATAL_EXCEPTION(e))
            raise HTTPException(status_code=400, detail="Fatal exception encountered while trying to establish connection with Form Manager") 
        
        result = []
        entity_type_col = self.access_entity_types()
        if r.json():
            try:
                for doc in r.json():
                    result.append(self.cast_as_FormIntent(doc, entity_type_col))
            except KeyError as e:
                self.logger.error(LogMessages.DAO_ERROR(e))

        return result
        

    def access_intent(self, intents_col: List[FormIntent], intent: str) -> FormIntent:
        """
        Get a single matching intent document 
        """
        for i in intents_col:
            if i.intent == intent:
                return i

        return None


    def access_entity_types(self) -> List[FormEntityType]:
        """
        Request a list of entity type documents from Form Manager and cast 
        it to a list of FormEntityType models
        """
        try:
            r = requests.get(self.FORM_MANAGER_URL + "/entity-types") 
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error(LogMessages.REQUEST_EXCEPTION(e))
            raise HTTPException(status_code=400, detail="Unable to establish connection with Form Manager")
        except Exception as e:
            self.logger.error(LogMessages.FATAL_EXCEPTION(e))
            raise HTTPException(status_code=400, detail="Fatal exception encountered while trying to establish connection with Form Manager")
        
        result = []
        if r.json():
            try:
                for doc in r.json():
                    result.append(self.cast_as_FormEntityType(doc))
            except KeyError as e:
                self.logger.error(LogMessages.DAO_ERROR(e))
                raise HTTPException(status_code=400, detail="Unable to access requested entries from Form Manager")

        return result


    def access_entity_types_by_intent(self, intents_col: List[FormIntent], intent: str) -> List[FormEntityType]:
        """
        Get list of entity types associated with intent
        """
        intent_form = self.access_intent(intents_col, intent)
        if intent_form is None:
            return []
        return [x for x in intent_form.entity_types]


    def access_entity_type(self, forms: List[FormEntityType], entity_type: str) -> FormEntityType:
        """
        Get a single matching entity type document 
        """
        for form in forms:
            if form.entity_type == entity_type:
                return form

        return None

form_DAO = FormDAO()