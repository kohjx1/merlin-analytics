from typing import List, Optional
from app.models.forms import FormEntityType, FormIntent

from app.models.forms_DAO import form_DAO

"""
Facilitate HTTP requests between the Form Manager and the NLU module
"""

def get_intent_col(context: Optional[str] = None) -> List[FormIntent]:
    return form_DAO.access_intents(context)


def get_entity_type_col(intent: Optional[str] = None) -> List[FormEntityType]:
    if intent is None:
        return form_DAO.access_entity_types()
    
    intent_col = form_DAO.access_intents()
    return form_DAO.access_entity_types_by_intent(intent_col, intent)


def get_entity_type_doc(entity_type: str) -> FormEntityType:
    entity_type_col = form_DAO.access_entity_types()
    return form_DAO.access_entity_type(entity_type_col, entity_type)