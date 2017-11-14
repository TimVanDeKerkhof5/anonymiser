import pandas as pd
import datetime as dt
import numpy as np

#name of file to write:
newfile = 'anonymised.csv'

#path to dataset:
filepath = 'homedupe.csv'

#list of headers needed in the dataset, change this to meet your needs
selected = ['volgnr','Geboortedatum','DiagnoseCode', 'OpnameUitvoerder','OpnameBewegingVolgnr','OpnameBehandelaar','vrgeschiedenis_myochardinfarct','vrgeschiedenis_PCI','vrgeschiedenis_CABG','vrgeschiedenis_CVA_TIA','vrgeschiedenis_vaatlijden','vrgeschiedenis_hartfalen','vrgeschiedenis_maligniteit','vrgeschiedenis_COPD','vrgeschiedenis_atriumfibrilleren','TIA','CVA_Niet_Bloedig','CVA_Bloedig','LV_Functie','dialyse','riscf_roken','riscf_familieanamnese','riscf_hypertensie','riscf_hypercholesterolemie','riscf_diabetes','roken','Radialis','Femoralis','Brachialis','vd_1','vd_2','vd_3','graftdysfunctie','lengte','gewicht','bloeddruk','HB','HT','INR','Glucose','Kreat','Trombocyten','Leukocyten','Cholesterol_totaal','Cholesterol_ldl']

#name of header that should be anonymised:
anoheader = 'PATNR'

encrdata = pd.read_csv(filepath,header=0,low_memory=False,encoding='utf-8')

#initializing of some variables that are used for logic

#counter is used for the id that will replace the original
counter = 0
scrambledict = {}
patarr = []

#shuffle the dataframe
encrdata = encrdata.sample(frac=1).reset_index(drop=True)

#if an identifier is not in the dictionary of identifiers, add it
for id in encrdata[anoheader]:
	if id not in scrambledict.keys():
		counter += 1
		scrambledict[id] = counter

#add the corresponding replacement of the identifier to a new array
for id in encrdata[anoheader]:
	patarr.append(scrambledict[id])

#replace the identifiers with the new, anonymised ones
encrdata['volgnr'] = patarr


#snippet for converting a date of birth to an age. to activate, set DOB to True, to disable, set to False
DOB = True

if DOB:
	#if the date you are converting is different from the label name below, change it accordingly
	l = 'Geboortedatum'
	now = pd.Timestamp(dt.datetime.now())

	#if your date is of a different format, consult the documentation on pandas datetimes
	encrdata[l] = pd.to_datetime(encrdata[l], format='%Y-%m-%d')
	encrdata[l] = encrdata[l].where(encrdata[l] < now, encrdata[l] - np.timedelta64(100, 'Y'))
	encrdata[l] = (now - encrdata[l]).astype('<m8[Y]')


#finally, convert the dataframe back into a .csv file, separated by comma's
encrdata.to_csv(path_or_buf=newfile,sep=',',columns=selected,index=False)


