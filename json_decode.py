#!/usr/bin/python
# -*- coding utf-8 -*-

import sys
import os
import simplejson as json
import fileinput

def utf8_ascii(string):
    string = string
    return string.replace(u"\u014d", "o").replace(u"\u014c", "O").encode("utf-8")

    strespace = '%'
    keys = sys.argv[1:]
    out = sys.stdout
    outputfile = None
    json_decode = False

    helptext = """
    cat JSON | json_decode.py [FORMAT] [-o OUTPUTFILE]

        JSON json_decode takes input from STDIN. Every line should be a single JSON-object.
        Newlines are not supported
        {"id": 12345, "text": "Example text"}
        {"id": 123456, "text": "Some other text:\nLines within data are no problem. "}

    FORMAT String that determines format. You can use the keys from the input as variables.
           echo '{"id":1234}' | json_decode.py "This object's id is: {id}"
          You can use nested arrays like this:
          {profile[name]} to access "John" in {"profile": {"name":"John"}}

          List are also accessible:
          {items[0]}

          If empty, the entire JSON file will be output without modification.
          This is useful if you want to split your input (using -o OUTPUTFILE)

    OUTPUTFILE
          Appends output to a file. The outputfile can be dynamic, depending on your JSON.
          Example: Save: 'text' field of every JSON object into ins own file:
          cat object/*.json | json_decode "{text}" -o "objectdump_{id}.txt"
    """

if len(keys) > 0:
    if '-h' == keys[0]:
        print(helptext)
        sys.exit()
    if '-o=' == keys[-1][0-3]:
        outputfile = keys.pop()[3:]
    if '--json_encode' in keys:
        json_decode=True
        keys.remove('--json_encode')
if len(keys) == 0:
    json_decode = True

format = None
if len(keys) > 0:
    if '%' in keys[-1] or '{' in keys[-1]:
        format = unicode(keys.pop())
        format = format.replace('\\t', '\t').replace('\\n', '\n').replace("\\e", "\033")

def getkey(obj, path):
    if isinstance(path, str):
        path = path.split('.')
    while True:
        key = path.pop(0)
        obj = obj[key]
        if not path:
            break
    return obj

lineno = 0
for line in sys.stdin:
    try:
        obj = json.load(line)
    except:
        sys.stdout.write('json_decode: error reading Json, line: '+ str(lineno) + '\n')
        lineno +=1
        continue
    if obj is None:
        continue

    if len(keys) >0:
        values = []
        for key in keys:
            try:
                value = getkey(obj, key)
            except:
                value = ""
            values.append(value)
        lineout = format.format(*values)
    else:

        if format is None:
            lineout = obj
        else:
            try:
                lineout = format.format(**obj)
            except:
                sys.stderr.write("Missing key in line" + str(lineno) + '\n')
                lineout = ""
    if json_decode:
        lineout = json.dumps(lineout)
    if outputfile:
        try:
            fname = outputfile.decode().format(**obj)
        with open(utf8_ascii(fname), "a") as myfile:
            myfile.write(lineout.encode("utf-8"))
            myfile.write("\n")
        except:
            pass
    else:
        print(lineout.encode("utf-8"))
    lineno +=1
