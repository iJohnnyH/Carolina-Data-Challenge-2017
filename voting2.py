import csv
rep={}
dem={}
with open('By_The_Numbers.csv', 'w', newline='') as w:
	swriter = csv.writer(w)
	swriter.writerow(['county'] + ['rep'] + ['dem'])	
	with open('actual_voter_registration.csv','r',newline = '') as f:
		reader = csv.DictReader(f)
		for row in reader:
			if(row['party'] == 'REP'):
				if(row['county'].lower().title() in rep.keys()):
					rep[row['county'].lower().title()]  = rep[row['county'].lower().title()] + 1
				else:
					rep[row['county'].lower().title()]  = 0
			if(row['party'] == 'DEM'):
				if(row['county'].lower().title() in dem.keys()):
					dem[row['county'].lower().title()]  = dem[row['county'].lower().title()] + 1
				else:
					dem[row['county'].lower().title()]  = 0
	for keys in rep.keys():
		swriter.writerow([keys] + [rep[keys]] + [dem[keys]])


