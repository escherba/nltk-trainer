#!/usr/bin/env roundup

describe "train_tagger.py"

it_displays_usage_when_no_arguments() {
	python -m nltk_trainer.scripts.train_tagger 2>&1 | grep -q "usage: train_tagger.py"
}

it_needs_corpus_reader() {
	last_line=$(python -m nltk_trainer.scripts.train_tagger foo 2>&1 | tail -n 1)
	test "$last_line" "=" "ValueError: you must specify a corpus reader"
}

it_cannot_import_reader() {
	last_line=$(python -m nltk_trainer.scripts.train_tagger corpora/treebank/tagged --reader nltk.corpus.reader.Foo 2>&1 | tail -n 1)
	test "$last_line" "=" "AttributeError: 'module' object has no attribute 'Foo'"
}

it_cannot_find_foo() {
	last_line=$(python -m nltk_trainer.scripts.train_tagger foo --reader nltk.corpus.reader.TaggedCorpusReader 2>&1 | tail -n 1)
	test "$last_line" "=" "ValueError: cannot find corpus path for foo"
}

it_trains_treebank() {
	test "$(PYTHONHASHSEED=0 python -m nltk_trainer.scripts.train_tagger treebank --no-pickle --no-eval --fraction 0.5)" "=" "loading treebank
3914 tagged sents, training on 1957
training AffixTagger with affix -3 and backoff <DefaultTagger: tag=-None->
training <class 'nltk.tag.sequential.UnigramTagger'> tagger with backoff <AffixTagger: size=2026>
training <class 'nltk.tag.sequential.BigramTagger'> tagger with backoff <UnigramTagger: size=3260>
training <class 'nltk.tag.sequential.TrigramTagger'> tagger with backoff <BigramTagger: size=1274>"
}

it_trains_corpora_treebank_tagged() {
	test "$(PYTHONHASHSEED=0 python -m nltk_trainer.scripts.train_tagger corpora/treebank/tagged --reader nltk.corpus.reader.ChunkedCorpusReader --no-pickle --no-eval --fraction 0.5)" "=" "loading corpora/treebank/tagged
51002 tagged sents, training on 25501
training AffixTagger with affix -3 and backoff <DefaultTagger: tag=-None->
training <class 'nltk.tag.sequential.UnigramTagger'> tagger with backoff <AffixTagger: size=1810>
training <class 'nltk.tag.sequential.BigramTagger'> tagger with backoff <UnigramTagger: size=3221>
training <class 'nltk.tag.sequential.TrigramTagger'> tagger with backoff <BigramTagger: size=1156>"
}

it_trains_ub() {
	test "$(PYTHONHASHSEED=0 python -m nltk_trainer.scripts.train_tagger treebank --sequential ub --no-pickle --no-eval --fraction 0.5)" "=" "loading treebank
3914 tagged sents, training on 1957
training <class 'nltk.tag.sequential.UnigramTagger'> tagger with backoff <DefaultTagger: tag=-None->
training <class 'nltk.tag.sequential.BigramTagger'> tagger with backoff <UnigramTagger: size=8435>"
}

it_trains_naive_bayes_classifier() {
	test "$(python -m nltk_trainer.scripts.train_tagger treebank --sequential '' --classifier NaiveBayes --no-pickle --no-eval --fraction 0.5)" "=" "loading treebank
3914 tagged sents, training on 1957
training ['NaiveBayes'] ClassifierBasedPOSTagger
Constructing training corpus for classifier.
Training classifier (50641 instances)
training NaiveBayes classifier"
}

it_trains_treebank_universal_tags() {
	test "$(PYTHONHASHSEED=0 python -m nltk_trainer.scripts.train_tagger treebank --tagset universal --no-pickle --no-eval --fraction 0.5)" "=" "loading treebank
using universal tagset
3914 tagged sents, training on 1957
training AffixTagger with affix -3 and backoff <DefaultTagger: tag=-None->
training <class 'nltk.tag.sequential.UnigramTagger'> tagger with backoff <AffixTagger: size=2026>
training <class 'nltk.tag.sequential.BigramTagger'> tagger with backoff <UnigramTagger: size=2244>
training <class 'nltk.tag.sequential.TrigramTagger'> tagger with backoff <BigramTagger: size=742>"
}
