import converter, writer, reader
import os

asts = reader.fetch(os.path.join('test','django'))
fdefs, calls = converter.convert(asts,os.path.join('test','django'))
len(writer.jsonTree(fdefs,calls,'django_tout.json'))

