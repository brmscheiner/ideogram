import converter, writer, reader
import os

asts = reader.fetch(os.path.join('test','self'))
fdefs, calls = converter.convert(asts,os.path.join('test','self'))
len(writer.jsonTree(fdefs,calls))

