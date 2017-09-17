
import csv

with open('actual_voter_registration.csv', 'w', newline='') as w:
	swriter = csv.writer(w)
	swriter.writerow(['county'] + ['party'])
	with open('voter_registration.tsv','r',newline = '') as f:
		reader = csv.DictReader(f,dialect = 'excel-tab')
		for row in reader:
			if(row['voter_status_desc'] == 'ACTIVE'):
				swriter.writerow([row['county_desc']] + [row['party_cd']])
		pass