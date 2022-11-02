from typing import List

from app.core.helper import pre_process_text, is_subsequence, get_numeric_answer

from app.schemas import Entity, EntityType, Intent
from app.models.forms import FormIntent, FormEntityType

"""
data from mongoDB should preferably be in this format:
intent_col = [
    {
        "intent": intent1,
        "examples": [kw1, kw2, ...],
        "entity_types": [
            {"entity_type": entity_type1, "isRequired": true/false},
            ...
        ]
        "context": {
            "in": [context1, context2, ...], 
            "out": [...]
        }
    },
    ...
]
entity_col = [
    {
        "entity_type": entity_type1,
        "keywords": [kw1, kw2, ...],
        "isNumeric": true/false, 
        "hasMultipleReferences": true/false,
        "entities": [
            {"entity": entity1, "synonyms": [kw1, kw2, ...]},
            ...
        ]
    },
    ...
]
Refer to "app/fake_form_manager/sample_db.mongodb" for an example of what the database should look like. 
NOTE: entity types that expect numeric answers (eg. age) uses a
shared numeric keyword-matching system, so answers keywords are not required 
from the user.
TODO: add in an additional field isLocation for location identification
in the future. 
"""

def get_intents(text: str, intent_col: List[FormIntent]) -> List[Intent]:
    """
    Get the intent from a chunk of text using the dictionary 
    defined by the form manager (saved in mongodb). Infers the intents, 
    entity types and entities in the text, and also returns all matching  
    keywords.
    
    OUTPUT = [
        {
            "intent": intent1, 
            "examples": [kw1, kw2, ...],
            "entity_types": [
                {
                    "entity_type": entity_type1,
                    "keywords": [kw1, kw2, ...],
                    "entities": [
                        {"entity": entity1, "synonyms": [kw1, kw2, ...]},
                        ...
                    ]
                },
                ...
            ]
        },
        ...
    ]
    """

    output = []
    # try to find a match in the list of keywords associated with intent
    for intent_doc in intent_col:
        kw = find_keywords_in_text(intent_doc.examples, text)
        entity_types = get_entity_types(text, intent_doc.entity_types)
        if kw or entity_types:
            intent = Intent(intent=intent_doc.intent, examples=kw, entity_types=entity_types)
            output.append(intent)

    return output


def get_entity_types(text: str, entity_type_col: List[FormEntityType]) -> List[EntityType]:
    """
    Get the entities from a chunk of text using the dictionary 
    defined by the form manager (saved in mongodb). Infers all entity 
    types and entities using the provided intent, and also returns all 
    matching keywords.
    
    OUTPUT = [
        {
            "entity_type": entity_type1,
            "keywords": [kw1, kw2, ...],
            "entities": [
                {"entity": entity1, "synonyms": [kw1, kw2, ...]},
                ...
            ]
        },
        ...
    ]
    """
    output = []
    for entity_type_doc in entity_type_col:
        kw = find_keywords_in_text(entity_type_doc.keywords, text)
        entities = get_entities(text, entity_type_doc)
        if kw or entities:
            entity_type = EntityType(entity_type=entity_type_doc.entity_type, keywords=kw, entities=entities)
            output.append(entity_type)

    return output


def get_entities(text: str, entity_type_doc: FormEntityType) -> List[Entity]:
    """
    Uses the provided entity type to do keyword-matching for entities. 
    Returns a list of matching entities and keywords used to identify them. 
    NOTE: Entities are returned as a ranked list, with the most likely entity
    at the head of the list.

    OUTPUT = [
        {
            "entity": entity1, 
            "synonyms": [kw1, kw2, ...]
        },
        ...
    ]
    """
    if entity_type_doc is None:
        return []

    # if entity type is numeric, expect only one entity and return the numeric value
    if entity_type_doc.isNumeric:
        entity, kw = get_numeric_answer(text)
        if entity is not None:
            return [Entity(entity=entity, synonyms=kw)]

    # for non-numeric entity types, return the ranked list of all matching entities
    output = []
    for entity in entity_type_doc.entities:
        kw = find_keywords_in_text(entity.synonyms, text)
        if kw:
            # janky method of sorting that takes up more storage but computes in O(n),
            # where n is highest number of matching entities
            while len(output) < len(kw):
                output.append(None)
            output.insert(len(kw), Entity(entity=entity.entity, synonyms=kw))

    # ranking for keyword matches among entities
    output = [e for e in reversed(output) if not e is None]

    return output


def find_keywords_in_text(kw_list: List[str], text: str) -> List[str]:
    """
    Checks if any words in the kw_list matches the text. Returns all matches.
    """
    # return empty list if either keyword list or text string is empty
    if not kw_list or not text:
        return []

    text_tokens = pre_process_text(text)
    kw_match_list = []
    for kw in kw_list:
        if is_subsequence(kw.split(" "), text_tokens):
            kw_match_list.append(kw)
    return kw_match_list
