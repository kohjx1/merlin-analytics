"""
Perform Intent Classification (IC) and Named Entity Recognition (NER) using 2 separate pre-trained BERT models
IC model takes in sentences (referred to as examples in the db), each corresponding to a user-defined intent, 
during training. 
NER model takes in sentences with each word tagged to either an entity type or null (these words are referred to 
as keywords in the db) during training.
NOTE: still unsure about how to further classify identified entity types into entities. Do we use simple keyword-
matching with user-defined synonyms or create another model that compares word embedding similarity?
"""