# run script while in dirtree directory

# for each directory in dirtree
for dir in *; do
    # for file in each subdirectory with extension tbl
	for file in $dir/*/*.tbl; do
        # retrieve top gsat score from file by isolating
        # header and first line, keeping first line, and
        # keeping gsat score field in the line
		gsat=$(head -3 $file | tail -1 | cut -f 4)
        # format output: name of directory '\t' top gsat score
		echo $dir'\t'$gsat 
	done 
# sort by gsat score in reverse order, then break ties by
# sorting directories in alpha order
done | sort -k2rn -k1