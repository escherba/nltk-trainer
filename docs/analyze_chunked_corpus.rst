Analyzing a Chunked Corpus
--------------------------

The ``analyze_chunked_corpus.py`` script will show the following statistics about a chunked corpus:

 * total number of words
 * number of unique words
 * number of tags
 * number of IOB tags
 * the number of times each tag and IOB tag occurs

To analyze the treebank corpus::
	``python -m nltk_trainer.scripts.analyze_chunked_corpus treebank_chunk``

To sort the output by tag count from highest to lowest::
	``python -m nltk_trainer.scripts.analyze_chunked_corpus treebank_chunk --sort count --reverse``

To analyze a custom corpus using a ``ChunkedCorpusReader``::
	``python -m nltk_trainer.scripts.analyze_chunked_corpus /path/to/corpus --reader nltk.corpus.reader.ChunkedCorpusReader``

The corpus path can be absolute, or relative to a nltk_data directory.

For a complete list of usage options::
	``python -m nltk_trainer.scripts.analyze_chunked_corpus --help``
