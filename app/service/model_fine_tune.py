import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import json
import os

db = DocBin()
project_root = os.environ.get("PROJECT_ROOT")

# download the model ...RUN BELOW COMMAND
# !python -m spacy download en_core_web_lg

nlp=spacy.load('en_core_web_lg')

file = open(f"{project_root}/data/annotations.json")
training_data = json.load(file)

for text,annotation in tqdm(training_data["annotations"]):
    doc = nlp.make_doc(text)
    entities=[]
    for start, end, label in annotation["entities"]:
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is not None:
            entities.append(span)
            
    doc.ents = entities
    db.add(doc)
    
    db.to_disk("training_data_doc.spacy")

# setup the pipeline with configuration to start to train your data ...RUN BELOW COMMANDs
# !python -m spacy init config config.cfg --lang en --pipeline ner --optimize efficiency --force

# !python -m spacy train config.cfg --output output --paths.train training_data_doc.spacy --paths.dev training_data_doc.spacy


# load saved model from the dir
nlp_news = spacy.load('output/model-best')

# run a quick test
doc = nlp_news(''' Vladimir Putin has led Russia's Victory Day commemorations with a parade in Red Square and heightened security after days of Ukrainian strikes targeting the capital.

China's Xi Jinping joined Putin as the Russian president told thousands of soldiers and more than 20 international leaders that Russia remembered the lessons of World War Two.

Putin used his speech to tie the war to today's full-scale invasion of Ukraine, and said all of Russia was behind what he called the "special military operation" - now well into its fourth year.

For the first time, a column of trucks carrying various combat drones took part in the Victory Day parade, apparently because of their widescale use in Ukraine.''')

# beautify the result
result =(spacy.displacy.render(doc, style="ent"))

