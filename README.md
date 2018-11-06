# Word hash Task

## Instalation
`requires python3`
```
git clone git@github.com:jumarti/eign.git

```
## Usage from shell
```
cd eign
python -m task.main --help
usage: main.py [-h] [-f GPATT] [-l] [-d] [-o FMT] [-e HEAD]

Take a list of files, output most frequent words
plus the sentences and docs where they are.

The core funcionality is defined on class Aggregator from `aggregator`
module which can be used on any program capable of feeding lines of
text to an Aggregator instance

examples:
python -m task.main -f "./docs/*.txt" -o markdown  > ./results/full.md
python -m task.main -f "./docs/*.txt" -o html  > ./results/full.html
python -m task.main -f "./docs/*.txt" -l -d -e 10 -o markdown  > ./results/uncommon.md
		

optional arguments:
  -h, --help  show this help message and exit
  -f GPATT    
              A glob pattern of input files to analyze (exp: ./docs/*.txt)
  -l          
              Print the whole paragraph. Otherwise, only the first and last 50 chars.
  -d          Output less frequent words first
  -o FMT      
              Output format: html or markdown
  -e HEAD     
              Output first N words
```


## Using the aggregator class
`aggregator.py` defines the class `Aggregator` which processes lines of text to produce the result

### Usage
```ptyhon
aggregator = Aggregator()
#for each line of input
## set source_label to the doc-id containing the line

aggregator.process_line(source_label, line)

#finaly, request the output
result = aggregator.output()
```

#### output function
```
returns a string representing the desired output
		PARAMS:
			- longs (boolean) : Print the whole sentence, otherwise only first
			and last chars.

			- head (int): print the first N words

			- reverse (boolean): Output most frequent word first
			
			- fmt (string): Output as 'html' or 'markdown' 
```