
Aca encontraremos dos funciones que se encargarán del procesamiento del texto y de la extracción de características

La data sin procesar se encontrara en un .json. Ejemplo de un ticket:
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
Y se transformara a un .csv, donde tendremos el contenido de lo que ha pasado, la clasificación del ticket y el texto procesado (tokens) es el que aparece en el ultimo campo:

```csv
"Good morning my name is XXXX XXXX and I appreciate it if you could help me put a stop to Chase Bank cardmember services. In 2018 I wrote to Chase asking for debt verification and what they sent me a statement which is not acceptable. I am asking the bank to validate the debt. Instead I been receiving mail every month from them attempting to collect a debt. I have a right to know this information as a consumer. Chase account # XXXX XXXX XXXX XXXX Thanks in advance for your help.",

Debt collection + Credit card debt,

morn name appreci chase bank cardmemb servic chase debt verif statement accept bank debt mail month attempt debt right inform consum chase account advanc help
```

El primer archivo a ejecutar es el `textprocessing.py` el cual procesara el texto, realizando:

**- Tokenización:**  Es el proceso de convertir las secuencias de caracteres, oraciones o párrafos en inputs que puedan ser procesados, en este caso palabras sueltas. 

**- Eliminación de stopwords:** consiste en omitir o eliminar palabras redundantes, que no contribuyen en gran medida a entender el texto. Las stopwords carecen de sentido cuando se escriben solas o sin la palabra clave o keyword, como ejemplo están las conjunciones, artículos, preposiciones y adverbios.
    
**- Lematización:** relaciona una palabra flexionada o derivada, es decir, en plural, en femenino, conjugada, etc. con su forma canónica o lema, forma que por convenio se acepta como representante de todas las formas. Por ejemplo: `decir` es el lema de `dije`, `diré` o `dijéramos`, `guapo` es el lema de `guapas`, `mesa` es el lema de `mesas`.

**- Etiquetado POS:** consiste en asociar cada palabra de una frase con su posición en la oración. Alguno de los tag usados son: Sustantivo, Verbo, Pronombre, Preposición, Adverbio, Conjunción, Adjetivo, Artículo


Este archivo utiliza la librería nltk, que posee todas la herramientas antes descritas, para el procesamiento de texto

<sub>

**NOTA:** Es necesario realizar `python -m nltk.downloader stopwords` y `python -m nltk.downloader punkt` luego de la instalación del paquete nltk mediante pip, para la descarga de los paquetes complementarios

</sub>

Si analizamos paso a paso el procesamiento del texto de ejemplo veremos

**- Tokenización:**                   
`['good', 'morning', 'my', 'name', 'is', 'xxxx', 'xxxx', 'and', 'i', 'appreciate', 'it', 'if', 'you', 'could', 'help', 'me', 'put', 'a', 'stop', 'to', 'chase', 'bank', 'cardmember', 'services', '.', 'in', '2018', 'i', 'wrote', 'to', 'chase', 'asking', 'for', 'debt', 'verification', 'and', 'what', 'they', 'sent', 'me', 'a', 'statement', 'which', 'is', 'not', 'acceptable', '.', 'i', 'am', 'asking', 'the', 'bank', 'to', 'validate', 'the', 'debt', '.', 'instead', 'i', 'been', 'receiving', 'mail', 'every', 'month', 'from', 'them', 'attempting', 'to', 'collect', 'a', 'debt', '.', 'i', 'have', 'a', 'right', 'to', 'know', 'this', 'information', 'as', 'a', 'consumer', '.', 'chase', 'account', '#', 'xxxx', 'xxxx', 'xxxx', 'xxxx', 'thanks', 'in', 'advance', 'for', 'your', 'help', '.']`

Vemos que tomo la frase y devolvió un array de las palabras suelta:


**- Eliminación de stopwords:**
`['good', 'morning', 'name', 'xxxx', 'xxxx', 'appreciate', 'could', 'help', 'put', 'stop', 'chase', 'bank', 'cardmember', 'services', '.', '2018', 'wrote', 'chase', 'asking', 'debt', 'verification', 'sent', 'statement', 'acceptable', '.', 'asking', 'bank', 'validate', 'debt', '.', 'instead', 'receiving', 'mail', 'every', 'month', 'attempting', 'collect', 'debt', '.', 'right', 'know', 'information', 'consumer', '.', 'chase', 'account', '#', 'xxxx', 'xxxx', 'xxxx', 'xxxx', 'thanks', 'advance', 'help', '.']`

Elimino palabras como `my` o `is`


**- Lematización:**  
`['good', 'morn', 'name', 'xxxx', 'xxxx', 'appreci', 'could', 'help', 'put', 'stop', 'chase', 'bank', 'cardmemb', 'servic', '.', '2018', 'wrote', 'chase', 'ask', 'debt', 'verif', 'sent', 'statement', 'accept', '.', 'ask', 'bank', 'valid', 'debt', '.', 'instead', 'receiv', 'mail', 'everi', 'month', 'attempt', 'collect', 'debt', '.', 'right', 'know', 'inform', 'consum', '.', 'chase', 'account', '#', 'xxxx', 'xxxx', 'xxxx', 'xxxx', 'thank', 'advanc', 'help', '.'] `      

Miremos el caso de `morning`, que se queda solo con la raíz `morn`; o el caso de `validate`que se queda con la raíz `valid`


**- Etiquetado POS:**
`'morn name appreci chase bank cardmemb servic chase debt verif statement accept bank debt mail month attempt debt right inform consum chase account advanc help'`

A diferencia de lo explicado anteriormente, aca se utiliza el etiquetado POS para filtrar y quedarse solo con los sustantivos, ademas de que transforma el array en un string. El archivo de salida sera `data/data_procesada/tickets_classification_eng_1.csv`


El segundo archivo a archivo a ejecutar es el `feature_extraction.py` el cual tomara el texto procesado y lo clasificara en temas:



TfidfVectorizer y NMF de scikit_learn













.
.
.
.
.
.



Nota:
Otros métodos que se pueden aplicar para el procesamiento del texto son:

Stemming: relaciona los afijos de las palabras para obtener la raíz de la palabra, por ejemplo, going se convierte en go.

Bolsa de palabras: una oración se considera como un conjunto de palabras, sin tener en cuenta la gramática ni el orden de las palabras.

N-gramas: son una secuencia continua de palabras adyacentes en una oración, necesarias para obtener el significado correctamente, por ejemplo, machine learning es un bigrama.

TF (frecuencia del término): es el número de veces que aparece una palabra en un mensaje o una oración; indica la importancia de esa palabra.

Reconocimiento de entidades nombradas: identifica y etiqueta palabras que representan entidades de palabras reales, como personas, organizaciones, lugares, fechas, etc.