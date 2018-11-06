import sys
import os
import glob
import argparse


from .aggregator import Aggregator


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='''
Take a list of files, output most frequent words
plus the sentences and docs where they are.

The core funcionality is defined on class Aggregator from `aggregator`
module which can be used on any program capable of feeding lines of
text to an Aggregator instance

examples:
python -m task.main -f "./docs/*.txt" -o markdown  > ./results/full.md
python -m task.main -f "./docs/*.txt" -o html  > ./results/full.html
python -m task.main -f "./docs/*.txt" -l -d -e 10 -o markdown  > ./results/uncommon.md
		''',  formatter_class=argparse.RawTextHelpFormatter)

	parser.add_argument('-f', dest='gpatt', default=None, help='''
A glob pattern of input files to analyze (exp: ./docs/*.txt)''')

	parser.add_argument('-l', dest='out_long_sent', action='store_true',
		default=False, help='''
Print the whole paragraph. Otherwise, only the first and last 50 chars.''')

	parser.add_argument('-d', dest='lowest_first', action='store_true',
		help='Output less frequent words first'
		)
	parser.add_argument('-o', dest='fmt', default='markdown', help='''
Output format: html or markdown''')
	parser.add_argument('-e', dest='head', type=int, help='''
Output first N words''')

	args = vars(parser.parse_args())
	gpatt = args.get('gpatt')
	fmt = args.get('fmt')
	lowest_first = args.get('lowest_first')
	out_long_sent = args.get('out_long_sent')
	head = args.get('head')

	aggregator = Aggregator()
	file_paths = glob.glob(gpatt)
	for fpath in file_paths:
		with open(fpath) as _file:
			source_label = fpath.split("/")[-1]
			for line in _file:
				aggregator.process_line(source_label, line)

	# sorted(words, key=lambda x:x.get('count'))
	result = aggregator.output(
		reverse=not lowest_first,
		fmt=fmt,
		head=head,
		longs=out_long_sent
		)
	print(result)
	sys.exit(0)