
import spacy
import csv
from spacy import displacy
# example = "jln.tirta tawar, br. junjungan, ubud, barat jalan dajan rurung"

nlp = spacy.load("./address.model")


count = 0
result_dict = {}
# outputFile = 

with open('output.csv', mode='a', newline='') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    employee_writer.writerow(["id", "POI/street"])
    
    with open("test.csv", encoding="utf8") as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        next(csvReader, None)
        for row in csvReader:
            address = row[1]
            doc = nlp(address)
            POI = ""
            STREET = ""

            for token in doc:
                if token.ent_type_ == "POI":
                    POI += token.orth_ + " "
                elif token.ent_type_ == "STREET":
                    STREET += token.orth_ + " "

            POI = POI[:-1]
            STREET = STREET[:-1]
            OUTPUTSTRING = POI + "/" + STREET
            # result_dict[count] = POI + "/" + STREET
            # print(count)
            employee_writer.writerow([count, OUTPUTSTRING])
            count += 1
        

# print([(token,
#         token.ent_type_,
#         token.lemma_.lower(),
#         token.is_stop)
#       for token in doc])



# print(doc)
# displacy.render(doc, style='ent')
# displacy.render(doc, style='ent', jupyter=False)
# html =  displacy.render(doc, style='ent', page=True)
# print("HTML markup: ", html)
# with open("./output.html", 'w+', encoding="utf-8") as fp:
#     fp.write(html)
#     fp.close()
