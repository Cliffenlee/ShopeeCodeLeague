import numpy as np
import pandas as pd
import collections
import csv

# read the dataset 
contacts = pd.read_json('./contacts.json')
contacts.tail()

resultDict = {}

def write_to_csv(orderedDict):
    # field names  
    fields = ['ticket_id', 'ticket_trace']  
        
    # data rows of csv file  
    rows = []
    
    for i in range(3):
        # print(f"iteration {i}", orderedDict)
        trace = orderedDict[i][0]
        contactCount = orderedDict[i][1]
        # print("what is this", trace)
        # print("what type is this", type(trace))
        trace = '-'.join(map(str, trace))
        trace += ", " + str(contactCount)
        row = [i, trace]
        rows.append(row)
        
    # name of csv file  
    filename = "#1-YeetCode-Student.csv"
        
    # writing to csv file  
    with open(filename, 'w', newline='') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        csvwriter.writerow(fields)  
            
        # writing the data rows  
        csvwriter.writerows(rows) 

def check_same(orderId, phone, email):
    result = []
    same_order = contacts.loc[( (contacts["Phone"] != "") & (contacts["Phone"] == phone) ) | ( (contacts["Email"] != "") & (contacts["Email"] == email) ) | ( (contacts["OrderId"] != "") & (contacts["OrderId"] == orderId))]
    for order in same_order.iterrows():
        result.append([order[0], order[1]])
    
    return result

def get_children(current_ticket, parent_ticket):   
    # print("im hereee")
    # print(current_ticket) 
    # print("\n\n\n")
    children = check_same(current_ticket["OrderId"], current_ticket["Phone"], current_ticket["Email"])
    count = len(children)
    finalChildren = []
    contactCount = []
    
    currentParents = parent_ticket
    currentParents.append(current_ticket["Id"]) if current_ticket["Id"] not in currentParents else None
    
    # print("current ticket:", current_ticket["Id"])
    # print("parents", parent_ticket)
    # print("dict",resultDict)

    #base case
    if count == 1:
        # print("count is 1")
        finalChildren.append(current_ticket["Id"])
        contactCount.append(current_ticket['Contacts'])
        # print("No children, ticket id: ", current_ticket["Id"], "contact count:", current_ticket['Contacts'])

    else:
        # print("I am", current_ticket["Id"])
        # print("My children are", children)
        for child in children:
            if current_ticket["Id"] == child[0]:
                grandchildrenId = [current_ticket["Id"]]
                contactCount.append(current_ticket['Contacts'])
            else:
                if child[0] not in currentParents:
                    grandchildren = get_children(child[1], currentParents)
                    grandchildrenId = grandchildren[0]
                    # print(f"child id: {child[0]}, contact count:", child[1]["Contacts"])
                    contactCount += grandchildren[1]   
                else:
                    grandchildren = []
                
            for grandchildId in grandchildrenId:
                if grandchildId not in finalChildren:
                    finalChildren.append(grandchildId)

            contacts.drop(contacts[contacts.Id == child[0]].index, inplace=True)
            # print("length is", len(contacts))
            # finalChildren += grandchildrenId

    contacts.drop(contacts[contacts.Id == current_ticket["Id"]].index, inplace=True)
    return [finalChildren, contactCount]

def main():
    while len(contacts) > 0:
    # for i in range (3):
        # print("\r\r")
        # print("current ticket", i)
        ticket = contacts.iloc[0]
        print("parent",ticket['Id'])
        children = get_children(ticket, [])
        finalChildren = children[0]
        contactCount = sum(children[1]) 
        print(finalChildren)
        print(contactCount)
        # contacts.drop(contacts.index[[0]], axis=0, inplace=True)
        # print("finalChildren:", finalChildren )

        for finalChild in finalChildren:
            resultDict[finalChild] = [finalChildren, contactCount]
    

        



main()
orderedDict = collections.OrderedDict(sorted(resultDict.items()))
print(orderedDict)
# print("over here!", orderedDict[1])
# print(orderedDict)
write_to_csv(orderedDict)


    

