
Aca encontraremos dos funciones que se encargarán del procesamiento del texto y de la extracción de características

La data sin procesar se encontrara en un .json:
```json
{
        "_id": "3229299",
        "_index": "complaint-public-v2",
        "_score": 0.0,
        "_source": {
            "company": "JPMORGAN CHASE & CO.",
            "company_public_response": null,
            "company_response": "Closed with explanation",
            "complaint_id": "3229299",
            "complaint_what_happened": "Good morning my name is XXXX XXXX and I appreciate it if you could help me put a stop to Chase Bank cardmember services. \nIn 2018 I wrote to Chase asking for debt verification and what they sent me a statement which is not acceptable. I am asking the bank to validate the debt. Instead I been receiving mail every month from them attempting to collect a debt. \nI have a right to know this information as a consumer. \n\nChase account # XXXX XXXX XXXX XXXX Thanks in advance for your help.",
            "consumer_consent_provided": "Consent provided",
            "consumer_disputed": "N/A",
            "date_received": "2019-05-01T12:00:00-05:00",
            "date_sent_to_company": "2019-05-01T12:00:00-05:00",
            "issue": "Written notification about debt",
            "product": "Debt collection",
            "state": "GA",
            "sub_issue": "Didn't receive enough information to verify debt",
            "sub_product": "Credit card debt",
            "submitted_via": "Web",
            "tags": "Servicemember",
            "timely": "Yes",
            "zip_code": "319XX"
        },
        "_type": "complaint"
    }
```
Y se transformara a un .csv, donde tendremos el contenido de lo que ha pasado, la clasificación del ticket y el texto procesado (palabras claves):

```csv
"Good morning my name is XXXX XXXX and I appreciate it if you could help me put a stop to Chase Bank cardmember services. In 2018 I wrote to Chase asking for debt verification and what they sent me a statement which is not acceptable. I am asking the bank to validate the debt. Instead I been receiving mail every month from them attempting to collect a debt. I have a right to know this information as a consumer. Chase account # XXXX XXXX XXXX XXXX Thanks in advance for your help.",

Debt collection + Credit card debt,

morn name appreci chase bank cardmemb servic chase debt verif statement accept bank debt mail month attempt debt right inform consum chase account advanc help
```

This class is used to process the text,
contains methods to tokenize, remove stopwords, lemmatize and pos_tagging the text
then, this data transformed to a dataframe and saved to a CSV file
The idea is to use this class in the pipeline to feature extration process