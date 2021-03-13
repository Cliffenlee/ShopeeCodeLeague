
# with open(r"./massRaw.txt", "r") as read_file:
#     for line in read_file:
#         entities = []
#         data = json.loads(line)
#         text = data[0]
#         start_offset = data[1]
#         end_offset = data[2]
#         label = "STREET" if data[3] == 3 else "POI"

#         entities.append((start_offset, end_offset,label))
#         spacy_entry = (entry['text'], {"entities": entities})