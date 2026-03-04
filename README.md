All python and R scripts and the full data sheet used in Pascal Tschabrun's Masters thesis.

token_converter.py takes inputs from a .txt file that was the result of an Annis export and creates an output file to be used for the data sheet (only compatible with specific export form)

evangelienbuch_ih_iz_instances.ods is the sheet file with all instances of the ih & iz pronouns and their context informations used for the analysis. In the columns concerning the distances to prosodic boundaries the ordering is not as it was for the data extraction and some tokens are labelled (some only partially) despite not being part of the analysis as they were part of a data collection preceding the randomisation of the data. They are typically found in book I. 

csv_converter.py takes data from selected columns of the data sheet and outputs a csv file with them, it includes a filter function and a function to select from the first n rows of the sheet

csv_files.zip are the csv files for input in the R script

data_stats.R uses the generated csv files and performs the statistical tests and creates bar charts
