## Objectives

- create analytics page (self-managed automatic form filling web portal)

  - users can create entity types
  - users are able to link these entity types to their form fields
    <br/>
    e.g. Form field allows user to choose what size they want, so linked Entity Type is size Entities under this Entity Type which could be:

    - S (synonyms: s, small, sm)
    - M (synonyms: m, medium, med)
    - L (synonyms: l, large, lg)
      <br/>
      Then, when the transcript is sent to the backend processing, it will return the detected entity. For instance, transcript mentioned "small size" so the result is S (automatically filled form with S)

### Svelte visualization charts

https://charts.carbondesignsystem.com/?path=/story/docs--welcome

<br/>

- Charts like word cloud are useful for user to see what are the common mentioned keywords.
- Probably need some relevancy filtering as there would be many entity types for just one form
  <br/>
  e.g. form may have fields linked to Entity Types like size/colour/collar_type/sleeve_type and might run through the transcripts to see what are the common keywords mentioned which could be relevant to entity types but are not picked up because they are not defined in entities. But at the same time besides knowing the keywords trend, it would be cool to have some sense making visualizations (see if there are any relationships between the entity types)

### TF-IDF (Term Frequency Inverse Document Frequency)

https://www.geeksforgeeks.org/understanding-tf-idf-term-frequency-inverse-document-frequency/

https://medium.com/analytics-vidhya/tf-idf-term-frequency-technique-easiest-explanation-for-text-classification-in-nlp-with-code-8ca3912e58c3

https://www.onely.com/blog/what-is-tf-idf/#:~:text=TF%2DIDF%20simple%20explanation,b)%20Cocaine.

- TF-IDF: Term Frequency Inverse Document Frequency of records.
- TF is a measure of how often a phrase appears in a document (frequency of a word - number of times it appears in a document)
- IDF is about how important that phrase is (measure of how significant that term is in whole corpus)
- It is used to weigh a keyword in any content and assign importance to that keyword **based on the number of times it appears** in document
- It checks how relevant the keyword is throughout the web (referred to as corpus)

Example: When you search for "Coke" on Google, Google may use TF-IDF to figure out if a page titled "COKE" is about:

1. Coca-Cola
2. Cocaine
3. A solid, carbon-rich residue derived from the distillation of crude oil
4. A country in Texas

```
  Wt,d = TFt,d log (N/DFt)
```

Terms:

- `TFt,d`: number of occurrences of t in document d
- `DFt`: number of documents containing the term t
- `N`: total number of documents in the corpus

#### How is TF-IDF score calculated

- Score between 0 and 1
- The **higher the numerical weight value, the rarer the term**
- The **smaller the weight, the more common ther term**

- TF (Term Frequency) example:

  - When you know TF, you are able to see if you are using a term too much/too little
  - When a 100-word document contains the term “cat” 12 times, the TF for the word ‘cat’ is `TFcat = 12/100 = 0.12`

- IDF (inverse document frequency) example:
  - Size of corpus (a body of documents) is 10,000,000 million documents
  - If we assume there are 0.3 million documents that contain the term "cat", then IDF is given by the total number of documents [10,000,000] divided by number of documents containing the term "cat" [300,000]
  - `IDF (cat) = log (10,000,000/300,000) = 1.52`

#### TF-IDF Calculation

Put the TF and IDF calculations together to get a TD-IDF score

- `∴ Wcat = (TF*IDF) cat = 0.12 * 1.52 = 0.182`
- A TF-IDF score of 0.182 is much closer to 0 than 1 (suggest that "cat" is a common term with less weight)

### Data Analytics

1. User form indicate what are the values they want and entities type
2. Text to speech to Transcript (ask questions and automatically fill form)
3. Backend process transcript
4. Gather the keywords (backend keyword list/extract transcript keywords)
5. Display on webpage (charts stats)

- Frontend (HTTP Request - JSON)
- Backend (Extract keyword from transcript - JSON)

### Remove stopwords

https://stackabuse.com/removing-stop-words-from-strings-in-python/

### Text Ranking

https://stevenloria.com/tf-idf/
