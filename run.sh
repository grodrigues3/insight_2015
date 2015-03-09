
# first I'll load all my dependencies
#apt-get install python-pandas
#apt-get install python-numpy

# next I'll make sure that all my programs (written in Python in this example) have the proper permissions
chmod a+x count_words.py
chmod a+x get_median.py

# finally I'll execute my programs, with the input directory wc_input and output the files in the directory wc_output
./count_words.py ./wc_input/ ./wc_output/wc_result.txt
./get_median.py ./wc_input/ ./wc_output/med_result.txt
