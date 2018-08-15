
default_target: all

TinyHaskellAST.py: TinyHaskell.ebnf
	python -m tatsu --object-model --outfile TinyHaskellAST.py TinyHaskell.ebnf

TinyHaskellParser.py: TinyHaskell.ebnf
	python -m tatsu --generate-parser --outfile TinyHaskellParser.py TinyHaskell.ebnf

parser: TinyHaskellAST.py TinyHaskellParser.py

runtest: parser Test.py
	python Test.py

all: runtest
