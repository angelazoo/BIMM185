import sys

full_matrix = sys.argv[1]
pub_status = sys.argv[2]
aux_status = sys.argv[3]

hpv_status = {}
with open(pub_status, 'r') as f:
    f.readline()
    f.readline()
    for line in f:
        line = line.rstrip().split('\t')
        pt = line[0]
        hpv = line[5]
        if hpv == "HPV+":
            hpv_status[pt] = 'Positive'
        else: 
            hpv_status[pt] = 'Negative'
    f.close()

with open(aux_status, 'r') as f:
    f.readline()
    f.readline()
    for line in f:
        line = line.rstrip().split('\t')
        pt = line[0]
        hpv = line[4]
        if pt not in hpv_status:
            if hpv == "Positive":
                hpv_status[pt] = hpv 
            elif hpv == "Negative":
                hpv_status[pt] = hpv 
            # do not record other statuses (indeterminate, etc.) 
    f.close()

fields_list = [1, 38, 40, 43, 44, 46]
with open(sys.argv[1], 'r') as f:
    hdr = f.readline().rstrip().split('\t')
    print '\t'.join([hdr[i] for i in fields_list])
    f.readline()
    f.readline()
    for line in f:
        line = line.rstrip().split('\t')
        pt = line[1]
        if pt in hpv_status:
            print '\t'.join([line[1], hpv_status[pt]]+[line[i] for i in fields_list[2:]])
        else: 
            print '\t'.join([line[i] for i in fields_list])