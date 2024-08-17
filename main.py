

import pandas as pd
import numpy as np

##EXPLAIN will explain what happens
EXPLAIN = False

RUN_MERGE = False
DEBUG = False
READ_UNCHANGED = False
TITLE_CHANGING = False




titleNewPath = 'changedTitleCsv'
originalPath = 'unchangedCSV'


##FILENAMES ARE CHANGED TO PROTECT COMPANY BUT WILL ADD MOCK DATA
# file1 = originalPath + '/A'
# file2 = originalPath + '/B'
# file3 = originalPath + '/C'

master = pd.read_csv(file1)
brochure = pd.read_csv(file3)
emailUpdates = pd.read_csv(file2)

print(master.shape)
print(brochure.shape)
print(emailUpdates.shape)

goal1 = 'Merge -------- Data into Master, carrying Master titles\nIf FN,LN is in Brochure&Master then Pull Brochure, else use master format'
masterTitles = 'FirstName,Mid,LastName,Degree,Affiliation,PrimaryAddress1,PrimaryAddress2,PrimaryCity,State,Primary Zip'
masterTitles = masterTitles.split(',')

SHOWCHANGE = False
SHOWSINGLECHANGE = False
SHOWMERGE = True


if EXPLAIN:
    SHOWCHANGE= True
    SHOWMERGE = True

def Merge1(m, b):
    notInMaster = []
    ensure_all_added = []
    numberNotInMaster = 0
    numberMatches = 0

    match = False
    for i in range(len(b['LastName'])):
        if b['LastName'][i] in list(m['LastName']):
            m_index = list(m['LastName']).index(b['LastName'][i])
            if b['FirstName'][i] == m['FirstName'][m_index]:
                match = True
                numberMatches += 1
                singleChangeLog1(m, m_index) if SHOWSINGLECHANGE else 0

                for title in masterTitles:
                    m.loc[m_index, title] = b.iloc[i][title]

                if SHOWSINGLECHANGE:
                    singleChangeLog1(m, m_index)
                    return

                ensure_all_added.append(i)
            else:
                match = False
        if not match:
            ensure_all_added.append(i)
            notInMaster.append(b.iloc[[i]])
            numberNotInMaster += 1

    changeLog(ensure_all_added, b, numberMatches, numberNotInMaster, m) if SHOWCHANGE else 0







    tempDf=pd.concat(notInMaster)
    mergeLog(tempDf, numberNotInMaster, m) if SHOWMERGE else 0


    for name in list(tempDf):
        if name not in masterTitles:
            tempDf.drop([name], axis=1, inplace=True)

    print(tempDf) if SHOWMERGE else 0
    newMaster = m.append(tempDf, ignore_index=True)

    return newMaster




emailUpdates.drop(['ELV Result'], axis=1, inplace=True)
emailUpdates.drop(['Unnamed: 8'], axis=1, inplace=True)
def Merge2(merged, e):

    master_size = merged.shape[0]
    data_not = []
    email_only = []
    ensure_all_added = []
    n_not = 0
    n_in = 0
    match = False

    ##ADD COLUMNS FOR EMAIL PERMISSION & EMAIL STATUS
    merged['Email Status'] = np.nan
    merged['Email permission status'] = np.nan

    for i in range(len(e['LastName'])):
        if e['LastName'][i] in list(merged['LastName']):

            m_index = list(merged['LastName']).index(e['LastName'][i])
            if e['FirstName'][i] == merged['FirstName'][m_index]:
                match = True
                n_in += 1

                for title in list(merged):
                    if title in list(e):
                        if not pd.isna(e.iloc[i][title]):
                            merged.loc[m_index,title] = e.iloc[i][title]

                ensure_all_added.append(i)
            else:
                match = False
        if not match:
            # if e['EmailAddress1'][i] ==
            if not pd.isna(e.iloc[i]['LastName']):
                data_not.append(e.iloc[[i]])
            else:
                email_only.append(e.iloc[[i]])
            ensure_all_added.append(i)
            n_not += 1


    df_not = pd.concat(data_not)

    # df_not.reset_index()
    print(df_not)
    print('titles:',list(df_not))
    print('l:',df_not.shape[0])

    # for name in list(tempDf):
    #     if name not in masterTitles:
    #         tempDf.drop([name], axis=1, inplace=True)
    # merged.reset_index()
    newMaster1 = merged.copy(deep=True)
    newMaster2 = merged.append(df_not, ignore_index=True)

    # print(ensure_all_added)
    # print('MATCHES:', n_in)
    # print('NUM_NEW:', n_not)
    # print('ALL:',e.shape[0],'should be',n_in+n_not)
    # print('New merge should have 2 extra columns, and',n_not,'extra rows, starting at',master_size,' =',n_not+master_size)
    #
    # print('There are ',newMaster2.shape[0]-(n_not+master_size),'more rows than expected.')
    return newMaster1, newMaster2, pd.concat(email_only)


def changeLog(ensure_all_added, b, numberMatches, numberNotInMaster, m):
    print('Each time I get a match, I take the row number and add it to a list')
    print('Each time I do not get a match, I do the same')
    print('The list SHOULD have all numbers from 0 to the length of the brochure - 1, which is', b.shape[0] - 1)
    print('Here is that list:\n', ensure_all_added)
    print('Length of brochure is:', b.shape[0])
    print('Length of the list is:', len(ensure_all_added))
    print('\nPROCESS\n')
    print(
        'Loop through everything in the brochure. IF LastName is found in Master\n\tTHEN GO there, check if FirstName matches')
    print('IF they match\n\tTHEN update the Master information with the Brochure information')
    print('\tELSE add the line to a new dataFrame, which we will add later')
    print('RESULT CHECK')
    print('N of MATCHES: ', numberMatches)
    print('N of NEW: ', numberNotInMaster)
    print('Size of brochure should match sum: n_B:', b.shape[0], 'vs', numberMatches + numberNotInMaster, '=n_SUM')
    print()
    print('Predicted size of new master:', m.shape[0] + numberNotInMaster, '\n********************\n')
def singleChangeLog1(m, m_index):
    print('I TAKE FIRST EXAMPLE:\nHere is the original in Master\n')
    print(m.loc[m_index])
def singleChangeLog2(m, m_index):
    print('\n****Change from Brochure Applied:*********\n')
    print(m.loc[m_index])
    print('\nTESTED TO ensure NaN will not replace')
def mergeLog(tempDf, numberNotInMaster, m):
    print()
    print('GOAL:', goal1, '\n')
    print('Here is a list of all the lines not in master(LastName and FirstName have no match)\n********\n')
    print(tempDf)
    print('\n*********\n')
    print('There are', numberNotInMaster, 'rows.')
    print('The length of the final spreadsheet should increase by', numberNotInMaster)
    print('Number of rows in Master:', m.shape[0])
    print('Number of rows to be added from Brochure:', tempDf.shape[0])
    print('Merge should have', (m.shape[0] + tempDf.shape[0]), 'rows.')

    print('I now remove the columns that are NOT in master')
def compare(og, new):
    print('\nORIGINAL:\n**********\n')
    print(og)
    print('\nMERGED:\n**********\n')
    print(new)

newMerge = Merge1(master, brochure)
compare(master, newMerge) if (SHOWCHANGE or SHOWMERGE) else 0



MasterFinal, MasterEmailAdded, NewEmails = Merge2(newMerge, emailUpdates)

print(MasterFinal)
print(MasterEmailAdded)
print(NewEmails)

def writeOut(f, title):
    f.to_excel('output_files/'+title+'.xlsx', index = False)

writeOut(MasterFinal, 'MasterFinal')
writeOut(MasterEmailAdded, 'Master_NoNameEmailsAdded')
writeOut(NewEmails, 'NewEmails')
#



    # output = merge2.to_excel('output_files/merged_titleIntersection.xlsx', index = False)


def readDimensionXLSX(spreadSheet):
    dataFrame = pd.read_excel(spreadSheet)
    print(dataFrame)

# readDimensionXLSX('output_files/merged.xlsx')
# readDimensionXLSX('output_files/merged_titleIntersection.xlsx')
#
# if RUN_MERGE == True:
#     0
    # output = merge(, b, c)
    # readDimensionXLSX(output)
readDimensionXLSX('MasterFinal')
