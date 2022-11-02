# Natural Language Understanding
NLU service that provides the intent/slot classification using rules or deep learning for fulfilment.
The implementation provides a RPC server that provides an endpoint for `/infer`. The server expects a query param and returns intents and entities as a JSON response.

## API endpoints:
#### <mark>PUT</mark> /infer/setup/{engine}
Define the NLU engine to be used moving forward. Currently only supports keyword-matching.

#### <mark>GET</mark> /infer/intent/{text}
Perform NLU on the provided text, returning all matching intents, entity types, and entities. Accepts context as an optional query parameter to narrow the search to only within the context (useful when form has been selected). 

#### <mark>GET</mark> /infer/entity-type/{text}
Perform NLU on the provided text, returning all matching entity types and entities. Accepts intent as an optional query parameter to narrow the search to only within the intent (useful in the future when intent becomes more granular).

#### <mark>GET</mark> /infer/entity/{text}
Perform NLU on the provided text, returning all matching entity types and entities. Accepts entity type as a required query parameter to narrow the search to only within the entity type (useful in cases where the operator asks a question and is expecting a answer from the caller).

## Docker Container Layout:
```
app
  |-main.py
  |-api
  |  |-dependencies
  |  |  |-form_manager.py
  |  |-routers
  |     |-setup.py
  |     |-intents.py
  |     |-entity_types.py
  |     |-entities.py
  |-services
  |  |-engine_manager.py
  |  |-keyword
  |  |  |-keyword_matching.py
  |  |-lstm
  |  |  |-lstm.py
  |  |  |-lstm_training.py
  |-schemas
  |  |-intents.py
  |  |-entities.py
  |  |-entity_types.py
  |-models
  |  |-forms.py
  |  |-forms_DAO.py
  |-core
  |  |-helper.py
  |  |-logging.py
  |-tests
  |  |-api
  |  |  |-test_setup.py
  |  |  |-test_intent.py
  |  |  |-test_entity.py
  |  |  |-test_entity_type.py
  |  |-core
  |     |-test_keyword.py
scripts
  |-nltk_dependencies.sh
  |-nltk_dependencies.txt
resources
  |-nltk_data
requirements.txt
```
