import sys
import tatsu
from TinyHaskellAST import *
import TinyHaskellParser

inputfile = '../src/Decode.hs'

# with open(inputfile, 'r') as f:
#    source = f.read()
# model = parser.parse(source, rule_name='start', semantics=TinyHaskellModelBuilderSemantics())

model = None

try:
    model = TinyHaskellParser.main(filename=inputfile,
                                   semantics=TinyHaskellModelBuilderSemantics())
except tatsu.exceptions.FailedParse as e:
    sys.stderr.write("Error: " + e.__str__())
    sys.exit(1)

print("-------- The model -----")
print(model)
print("----- Tests")
print(model.decls[0].name)
print(model.imports)
