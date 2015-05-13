import urllib2
import os

"""
This script obtains the synsets associated with a given list of words, in order to download those words from ImageNet.
A synset is a set of synonyms, from WordNet, that ImageNet associates to a class of images.
You can use the MATLAB toolbox to get the images from a list of synsets: http://image-net.org/download-toolbox
Word-synset relations are extracted from http://www.image-net.org/archive/words.txt

Currently, each word is assigned all synsets to which it is one of the labels. 
ie. if a synset is labeled 'cinnamon, cinnamon tree, Ceylon cinnamon', then the associated synset is appended to 
each of these labels.
If you only want the one synset per word, ie. only the synset labeled 'cinnamon' for word 'cinnamon', then comment
out/in the appropriate lines of code, indicated below. (Note: sometimes this still gives more than one synset per
word, due to an ImageNet labeling error)

UPDATE: now, each word is assigned its unique synset. If it doesn't exist, then it is assigned all associated
synsets.

Final output is a list of tuples, (word, [list of synsets for word])
"""



WORD_SYNSET = 'http://www.image-net.org/archive/words.txt'
WORDLIST = ['cat','dog','attack','cinnamon','Ceylon cinnamon']


def createSynsetDict(data):
	syns_dict_unique = {}
	syns_dict_all = {}
	for row in data:
		row = row.split('\t')
		labels = row[1]
		labels_all = labels.split(', ') #""" Comment out this line if you only want 1 synset per word """ 
		label_unique = labels #""" Un-comment this line if you only want 1 synset per word """
		if label_unique not in syns_dict_unique:
			syns_dict_unique[label_unique] = [row[0]]
		else:
			syns_dict_unique[label_unique].append(row[0])
		for label in labels_all:
			if label not in syns_dict_all:
				syns_dict_all[label] = [row[0]]
			else:
				syns_dict_all[label].append(row[0])		
	return syns_dict_unique, syns_dict_all

def getWordSynsets(syns_dict_unique, syns_dict_all):
	desired_synsets = []
	for word in WORDLIST:
		if word in syns_dict_unique:
			desired_synsets.append((word,syns_dict_unique[word]))
		elif word in syns_dict_all:
			desired_synsets.append((word,syns_dict_all[word]))
	return desired_synsets



print 'Getting list of synsets'
word_synset_data = urllib2.urlopen(WORD_SYNSET).read()
word_synset_data = word_synset_data.split('\n')

print 'Constructing synset dictionary'
syns_dict_unique, syns_dict_all = createSynsetDict(word_synset_data)

print 'Assigning correct synsets to input words'
desired_synsets = getWordSynsets(syns_dict_unique, syns_dict_all)

print desired_synsets

