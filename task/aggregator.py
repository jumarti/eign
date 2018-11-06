import hashlib
import re
from collections import OrderedDict

class Aggregator():
	'''
	Processes lines of input text in order to count words' frequencies and
	store each sentence a word is mentioned.
	the method process_line processes an input line
	the method output returns a formatted (html or markdown) table

	The table shows, per word: count, sentences the word is mentioned, and
	documents_labels* where found

	* The class processes lines w/o knowing the source. When process_line
	is called, a source_id is labeled by the caller.
	'''

	def __init__(self):
		self.words = {}
		self.sentences = {}

	def _hash_sentence(self, inp):
		m = hashlib.md5()
		m.update(inp.encode())
		return m.hexdigest()

	def process_line(self, source_label, line):
		'''
		Process a line of text.
		Aggregates self.words and self.sentences
		'''

		for sentence in line.split("."):
			#Sentences: a line splitted by dots.
			if len(sentence) < 1:
				continue
			#hash the sentence so that each word can
			# contain a list of hashes the word is
			# mentioned
			shash = self._hash_sentence(sentence)
			self.sentences[shash] = sentence
			#improve: not handling hash collision

			for word in re.split("\W+", sentence):
				if len(word) == 0:
					continue
				#taking valid words, w/o punctuaction
				word = word.lower()
				if word not in self.words:
					#create the word dict
					self.words[word] = {
						'count' : 0,
						'in_hashes' : {},
						'in_sources' : {}
						}
					#in_hashes is a dict where
					#key is the sentence hash, the
					# value is set to any dummy value (True)

					#in_sources is a dict where
					#key is the source_label, the
					# value is set to any dummy value (True)

				#increment the word count
				self.words[word]['count'] += 1

				#set (or reset) the sentence hash
				_hashes = self.words[word]['in_hashes']
				_hashes[shash] = True

				#set (or reset) the source_label
				_sources = self.words[word]['in_sources']
				_sources[source_label] = True

	def output(self, longs=False, head=None, reverse=True, fmt="html"):
		'''
		returns a string representing the desired output
		PARAMS:
			- longs (boolean) : Print the whole sentence, otherwise only first
			and last chars.

			- head (int): print the first N words

			- reverse (boolean): Output most frequent word first

			- fmt (string): Output as 'html' or 'markdown'
		'''

		sorted_words = OrderedDict(
			sorted(
				self.words.items(),
				key=lambda x:x[1].get('count'),
				reverse=reverse
			))

		if fmt == 'html':
			pre = ["<table border>"]
			pre.append('''
				<tr><th >word</th>
				<th width=40>count</th>
				<th width=100>found in</th>
				<th width=800>paragraphs</th>
				</tr>
				''')
			def _fmt_word(word, count, sources):
				return "<tr><td>{word}</td><td>{count}</td><td>{sources}</td><td></td></tr>"\
					.format(**dict(word=word, count=count, sources=sources))
			def _fmt_sentence(sentence):
				return "<tr><td></td><td></td><td></td><td><div>{}</div></td></tr>"\
					.format(sentence)
			post = ["</table>"]

		elif fmt == 'markdown':
			pre = []
			post = []
			pre.append('''| word | count| found in| paragraphs|''')
			pre.append('''| --- | ---| --- | --- |''')
			def _fmt_word(word, count, sources):
				return "| {word} | {count} |{sources} | |"\
					.format(**dict(word=word, count=count, sources=sources))
			def _fmt_sentence(sentence):
				return "| .| .| .| {} |"\
					.format(sentence)
		else:
			raise Exception("unsupported format {}".format(fmt))

		lines = []
		index = 0
		for word, value in sorted_words.items():
			lines.append(
				_fmt_word(
					word,
					value.get('count'),
					list(value.get('in_sources').keys())
					))
			for _hash in value['in_hashes']:
				if longs == False:
					sent = self.sentences[_hash][0:40] + " ... "
					sent = self.sentences[_hash][-40:]
				else:
					sent = self.sentences[_hash]
				lines.append(_fmt_sentence(sent))
			index += 1
			if head is not None:
				if index >= head:
					break

		return "\n".join(pre + lines + post)

