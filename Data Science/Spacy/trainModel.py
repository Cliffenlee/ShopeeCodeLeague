import json
import spacy
import random
import json


from spacy.tokens import Doc
from spacy.training import Example

# labeled_data = []
# with open(r"./labelled.jsonl", "r") as read_file:
#     for line in read_file:
#         data = json.loads(line)
#         labeled_data.append(data)

# TRAINING_DATA = []

# for entry in labeled_data:
#     entities = []
#     # print(entry)
#     for e in entry['annotations']:
#         entities.append((e["start_offset"], e["end_offset"],"STREET" if e["label"] == 3 else "POI"))
#     spacy_entry = (entry['text'], {"entities": entities})
#     TRAINING_DATA.append(spacy_entry)

# print(TRAINING_DATA)

TRAINING_DATA = []

with open(r"./finalboss.txt", "r") as read_file:
    for line in read_file:
        entities = []
        data = json.loads(line)
        text = data[0]
        object_list = data[1]

        for label_object in object_list:
            start_offset = label_object[0]
            end_offset = label_object[1]
            label = label_object[2]
            entities.append((start_offset, end_offset,label))
        
        spacy_entry = (text, {"entities": entities})
        TRAINING_DATA.append(spacy_entry)

# print(TRAINING_DATA)

# ('pangkalan lareh kel.ikurkoto koto panjang.kec koto tangah kota padang', {'entities': [(0, 15, 'POI')]})
# ('prim warna dan rekan kembang jeruk iv, tlogosari kulon', {'entities': [(21, 36, 'street')]})
nlp = spacy.blank("en")
ner = nlp.create_pipe("ner")
nlp.add_pipe("ner")
ner.add_label("STREET")
ner.add_label("POI")
# Start the training
nlp.begin_training()
# Loop for 40 iterations
for itn in range(40):
    # Shuffle the training data
    random.shuffle(TRAINING_DATA)
    losses = {}
    examples = []
# Batch the examples and iterate over them
    for batch in spacy.util.minibatch(TRAINING_DATA, size=2):
        for text, entities in batch:
            # texts = [text for text, entities in batch]
            # annotations = [entities for text, entities in batch]
            doc = nlp.make_doc(text)
            # spacy.training.offsets_to_biluo_tags(doc, entities)
            example = Example.from_dict(doc, entities)
            examples.append(example)
# Update the model
        nlp.update(examples, losses=losses, drop=0.3)
        print(losses)
        example = []

nlp.to_disk("/address.model")