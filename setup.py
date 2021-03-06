import re
import itertools
from setuptools import setup, find_packages
from pkg_resources import resource_string
from glob import glob


# dependency links
SKIP_RE = re.compile(r'^\s*(?:-f|--find-links)\s+(.*)$')

# Regex groups: 0: URL part, 1: package name, 2: package version
EGG_RE = re.compile(r'^(.+)#egg=([a-z0-9_.]+)-([a-z0-9_.-]+)$')

# Regex groups: 0: URL part, 1: package name, 2: branch name
URL_RE = re.compile(r'^\s*(https?://[\w\.]+.*/([^\/]+)/archive/)([^\/]+).zip$')

# our custom way of specifying extra requirements in separate text files
EXTRAS_RE = re.compile(r'.*\bextras\.(\w+)\.txt$')


def parse_reqs(reqs):
    """Parse requirements.txt files into lists of requirements and dependencies
    """
    pkg_reqs = []
    dep_links = []
    for req in reqs:
        # find things like
        # --find-links http://packages.livefyre.com/buildout/packages/
        dep_link_info = re.search(SKIP_RE, req)
        if dep_link_info is not None:
            url = dep_link_info.group(1)
            dep_links.append(url)
            continue
        # add packages of form:
        # git+https://github.com/Livefyre/pymaptools#egg=pymaptools-0.0.3
        egg_info = re.search(EGG_RE, req)
        if egg_info is not None:
            url, egg, version = egg_info.group(0, 2, 3)
            pkg_reqs.append(egg + '==' + version)
            dep_links.append(url)
            continue
        # add packages of form:
        # https://github.com/escherba/matplotlib/archive/qs_fix_build.zip
        zip_info = re.search(URL_RE, req)
        if zip_info is not None:
            url, pkg = zip_info.group(0, 2)
            pkg_reqs.append(pkg)
            dep_links.append(url)
            continue
        pkg_reqs.append(req)
    return pkg_reqs, dep_links


def build_extras(glob_pattern):
    """Generate extras_require mapping
    """
    fnames = glob(glob_pattern)
    result = dict()
    dep_links = []
    for fname in fnames:
        extras_match = re.search(EXTRAS_RE, fname)
        if extras_match is not None:
            extras_file = extras_match.group(0)
            extras_name = extras_match.group(1)
            with open(extras_file, 'r') as fhandle:
                result[extras_name], deps = parse_reqs(fhandle.readlines())
                dep_links.extend(deps)
    return result, dep_links


INSTALL_REQUIRES, INSTALL_DEPS = parse_reqs(
    resource_string(__name__, 'requirements.txt').splitlines())
TESTS_REQUIRE, TESTS_DEPS = parse_reqs(
    resource_string(__name__, 'requirements-tests.txt').splitlines())
EXTRAS_REQUIRE, EXTRAS_DEPS = build_extras('requirements-extras.*.txt')
DEPENDENCY_LINKS = list(set(itertools.chain(
    INSTALL_DEPS,
    TESTS_DEPS,
    EXTRAS_DEPS
)))


setup(
    name='nltk-trainer',
    packages=find_packages(exclude=['tests', 'docs']),
    version='0.10lf',
    description='Train NLTK objects with 0 code',
    long_description=resource_string(__name__, 'README.rst'),
    license='Apache',
    author='Jacob Perkins',
    author_email='japerk@gmail.com',
    url='https://github.com/japerk/nltk-trainer',
    # TODO: download_url
    keywords=['nltk', 'nlp', 'nlproc'],
    scripts=(
        'nltk_trainer/scripts/analyze_chunked_corpus.py',
        'nltk_trainer/scripts/analyze_chunker_coverage.py',
        'nltk_trainer/scripts/analyze_classifier_coverage.py',
        'nltk_trainer/scripts/analyze_tagged_corpus.py',
        'nltk_trainer/scripts/analyze_tagger_coverage.py',
        'nltk_trainer/scripts/combine_classifiers.py',
        'nltk_trainer/scripts/train_chunker.py',
        'nltk_trainer/scripts/train_classifier.py',
        'nltk_trainer/scripts/train_tagger.py',
    ),
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    dependency_links=DEPENDENCY_LINKS,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
    ]
)
