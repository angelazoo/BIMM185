import sys

# filename for TCGA archives HNSCC composite flat file (contains smoking history)
full_matrix = sys.argv[1]
# file name for published HPV status for 279 HNSCC patients
pub_status = sys.argv[2]
# file name for TCGA auxiliary HNSCC HPV status file
aux_status = sys.argv[3]

hpv_status = {}
with open(pub_status, 'r') as f:
    # skip header lines
    f.readline()
    f.readline()
    for line in f:
        line = line.rstrip().split('\t')
        pt = line[0]
        hpv = line[5]
        # parse and record HPV status for each pt
        if hpv == "HPV+":
            hpv_status[pt] = 'Positive'
        else: 
            hpv_status[pt] = 'Negative'
    f.close()

with open(aux_status, 'r') as f:
    # skip header lines
    f.readline()
    f.readline()
    for line in f:
        line = line.rstrip().split('\t')
        pt = line[0]
        hpv = line[4]
        # parse and record HPV status if not already determined in prev file
        if pt not in hpv_status:
            if hpv == "Positive":
                hpv_status[pt] = hpv 
            elif hpv == "Negative":
                hpv_status[pt] = hpv 
            # do not record other statuses (indeterminate, etc.) 
    f.close()

# list of fields corresponding to pt id, smoking, and drinking history
fields_list = [1, 38, 40, 43, 44, 46]
with open(sys.argv[1], 'r') as f:
    # capture headers corresponding to field list
    hdr = f.readline().rstrip().split('\t')
    print '\t'.join([hdr[i] for i in fields_list])
    # skip header lines
    f.readline()
    f.readline()
    for line in f:
        line = line.rstrip().split('\t')
        pt = line[1]
        # collate hpv status from above files with fields in current file
        if pt in hpv_status:
            print '\t'.join([line[1], hpv_status[pt]]+[line[i] for i in fields_list[2:]])
        # if hpv status not present in other files, use prelim status recorded in current file
        else: 
            print '\t'.join([line[i] for i in fields_list])
