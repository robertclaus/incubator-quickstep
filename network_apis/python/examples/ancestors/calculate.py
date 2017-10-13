import quickstep as q
import pandas as pd

def addAncestors(individual,decendant,relationList,ancestorList):
    # search for decendants of the passed in decendant and add them as ancestors for the individual
    grandDecendantRelationshipIndexes=relationList['parent'].str.contains(decendant)
    grandDecendantRelationshipList=relationList[grandDecendantRelationshipIndexes]
    for index,grandDecendantRelationship in grandDecendantRelationshipList.iterrows():
        grandDecendantName=grandDecendantRelationship['child']
        ancestorList=addAncestors(individual,grandDecendantName,relationList,ancestorList)

    #add parent/child to ancestorList if not present already
    return ancestorList.append({'individual':individual,'decendant':decendant},ignore_index=True)


#Not the fastest implementation but demonstrates working with data that is pulled from the quickstep database
if __name__ == '__main__':
    relationships=q.sql_to_table("SELECT parent,child FROM parentChildRelationship;")
    ancestors=pd.DataFrame({},columns=['individual','decendant'])

    print(relationships)
    print(' ')

    for index,row in relationships.iterrows():
        ancestors=addAncestors(row['parent'],row['child'],relationships,ancestors)

    print(ancestors)
