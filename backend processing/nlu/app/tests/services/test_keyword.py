# from app.services.keyword import keyword_matching
# from app.schemas import Entity, EntityType, Intent
# from app.models.forms import FormIntent, FormIntentEntityType, FormEntityType

# def test_get_intent_from_form():
#     sample_intent_form = FormIntent(
#         intent="get_personal_information",
#         examples=["who", "personal details", "personal information"],
#         entity_types=[
#             FormIntentEntityType(entity_type="age", isRequired=True),
#             FormIntentEntityType(entity_type="gender", isRequired=True),
#         ]
#     )
#     sample_text = "Can you give me his personal details?"

#     intent = keyword_matching.get_intent_from_form(sample_intent_form, sample_text)
#     assert type(intent) == Intent
#     assert intent.dict() == {
#         "intent": "get_personal_information", 
#         "examples": ["personal details"], 
#         "entity_types": []
#     }


# def test_get_entity_type_from_form():
#     sample_entity_type_form = FormEntityType(
#         entity_type="age",
#         keywords=["age", "years old", "year old", "how old"],
#         isNumeric=True, 
#         entities=[]
#     )
#     sample_text = "How old is she?"

#     entity_type = keyword_matching.get_entity_type_from_form(sample_entity_type_form, sample_text)
#     assert type(entity_type) == EntityType
#     assert entity_type.dict() == {
#         "entity_type": "age",
#         "keywords": ["how old"],
#         "entities": []
#     }


# def test_get_entities_from_form():
#     sample_entity_type_form = FormEntityType(
#         entity_type="age",
#         keywords=["age", "years old", "year old", "how old"],
#         isNumeric=True, 
#         entities=[]
#     )
#     sample_text = "He is thirty five years old"

#     entity = keyword_matching.get_entities_from_form(sample_entity_type_form, sample_text)
#     for e in entity:
#         assert type(e) == Entity
#     assert entity == [
#         {"entity": "35", "synonyms": ["thirty five"]}
#     ]