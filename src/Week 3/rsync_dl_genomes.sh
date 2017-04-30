# script parses refseq summary file and for first five genomes from
# Drosophila or Arabidopsis, downloads genome using rsync 

# set internal field separator to newline
old_IFS=$IFS
IFS=$'\n'
# parse summary file for lines that match Drosophila and Arabidopsis
# take first five matches, extract field corresponding to URL, replace
# ftp with rsync 
for line in $(cat assembly_summary_refseq.txt | grep -e "Drosophila" -e "Arabidopsis" | head -5 | cut -f20 | perl -pe 's/ftp/rsync/g'); 
do
    # make destination directory for download corresponding to name of file
    f=$(echo $line | cut -d'/' -f10-)
    # using rsync, download the genome
    rsync -avzL $line $f 
done
IFS=$old_IFS 