import sys, bz2

'''
Given tab-separated bzfile input with fields: protein ID, partner ID, 
method, interaction score outputs proteins ordered by number of total 
interactions, followed by ID & score of partner with max interaction 
score
'''

# open bz2 file
bz_file = bz2.BZ2File(sys.argv[1], 'r') 

# initializations
curr_prot = ''
prot_dict = {}

# nested dict - 2000 proteins as keys, values = dict of partners + score 
# as (k, v) pair   
while len(prot_dict) < 2000:
	line = bz_file.readline().rstrip().split("\t")
	curr_prot = line[0]
	# only one dict entry for unique protein
	if curr_prot not in prot_dict:
		prot_dict[curr_prot] = {}
	prot_dict[curr_prot][line[1]] = float(line[3])

prot_dict_params = {}

for elm in prot_dict:
	# enumerate # of partners assoc with each protein
	partners = len(prot_dict[elm])
	# nested dict with # of partners of protein = keys
	if partners not in prot_dict_params:
		prot_dict_params[partners] = {}
	# determine protein partner with max score	
	max_partner = max(prot_dict[elm], key=prot_dict[elm].get)
	max_score = prot_dict[elm][max_partner]
	# create nested dict saving max score, IDs of max partner and assoc.
	# protein
	prot_dict_params[partners][max_score] = [] 
	prot_dict_params[partners][max_score] = [max_partner, elm]

# numeric sort of dict in reverse order to prioritize proteins with most
# partners
for p in sorted(prot_dict_params, key=int, reverse=True):
	# if # partners identical, sort by max score of binding partners
	for e in sorted(prot_dict_params[p], key=float, reverse=True):
		partner = prot_dict_params[p][e][0]
		prot = prot_dict_params[p][e][1]
		# format output
		print '\t'.join([prot, str(p), partner, str(e)]) 
