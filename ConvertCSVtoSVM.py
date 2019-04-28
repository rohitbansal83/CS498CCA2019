#!/usr/bin/env python

"""
Convert CSV file to libsvm format. Works only with numeric variables.
Put -1 as label index (argv[3]) if there are no labels in your file.
Expecting no headers. If present, headers can be skipped with argv[4] == 1.
"""

import sys
import csv
from collections import defaultdict

def construct_Bin_line( label, line ):
	new_line = []
	if float( label ) == 0.0:
		label = "0"
	if float(label) >= 1.0:
		label = "1"
	new_line.append( label )


	for i, item in enumerate( line ):
		if item == '' or float( item ) == 0.0:
			continue
		new_item = "%s:%s" % ( i + 1, item )
		new_line.append( new_item )
	new_line = " ".join( new_line )
	new_line += "\n"
	return new_line

def construct_Multi_line( label, line ):
	new_line = []
	if float(label) >= 2.0:
		label = "0"
	if float(label) == 1.0:
		label = "1"
	
	new_line.append( label )


	for i, item in enumerate( line ):

		if item == '' or float( item ) == 0.0:
			continue
		new_item = "%s:%s" % ( i + 1, item )
		new_line.append( new_item )
	new_line = " ".join( new_line )
	new_line += "\n"
	return new_line

def construct_Test_line( label, line ):
	new_line = []
	
	new_line.append( str(label) )


	for i, item in enumerate( line ):

		if item == '' or float( item ) == 0.0:
			continue
		new_item = "%s:%s" % ( i + 1, item )
		new_line.append( new_item )
	new_line = " ".join( new_line )
	new_line += "\n"
	return new_line


# ---

input_file = sys.argv[1]
output_file = 'combined_hd_absence'
output_file1 = 'combined_hd_level'
output_file2 = 'user_data'

try:
	label_index = int( sys.argv[2] )
except IndexError:
	label_index = 0

try:
	skip_headers = sys.argv[3]
except IndexError:
	skip_headers = 0

i = open( input_file, 'r' )
o = open( output_file, 'w' )
o1 = open( output_file1, 'w' )
o2 = open( output_file2, 'w' )

reader = csv.reader( i )

if skip_headers:
	headers = reader.next()
counter = 0
#Build Binary File:
for line in reader:
	
	if label_index == -1:
		label = '1'
	else:
		label = line.pop( label_index )

	new_line = construct_Bin_line( label, line )
	o.write( new_line )
	counter += 1
	if counter%100 == 0:
		new_line = construct_Test_line( counter, line )
		o2.write( new_line )

	if float(label) == 0.0:
		continue

	new_line = construct_Multi_line( label, line )
	o1.write( new_line )

	
