
# JSON-DECODE
Decode Json file with python

Example

data.json:

{"id":10003, "user": "John", "text": "Example Text", "birthday": {"day": 1, "month": 1}}
{"id":10005, "user": "Jack", "text": "Some other text\nExtra line", "birthday": {"day": 2, "month": 2}}

Usage:

$ cat data.json | json_decode.py "{user} said: {text}"
John said: Example Text
Jack said: Some other text
Extra line

$ cat data.json | json_decode.py "{user} has birthday on {birthday[day]}/{birthday[month]}"
John has birthday on 1/1
Jack has birthday on 2/2

$ cat data.json | json_decode.py -o data_{id}.json
$ cat data_10003.json
{"id":10003, "user": "John", "text": "Example Text", "birthday": {"day": 1", "month": 1}}

$ cat data.json | json_decode.py {text} -o user_{user}.txt
$ cat user_Jack.txt
Some other text
Extra line

$ json_decode.py -h
cat JSON | json_decode.py [FORMAT] [-o OUTPUTFILE]

  JSON    json_decode takes input from STDIN. Every line should be a single JSON-object.
          Newlines are not supported.

          {"id": 12345, "text": "Example Text"}
          {"id": 12346, "text": "Some other text:\nLines within data are no problem."}

  FORMAT  String that determines format. You can use the keys from the input as variables.
          echo '{"id":1234}' | json_decode.py "This object's id is: {id}"

          You can use nested arrays like this:
          {profile[name]} to access "John" in {"profile":{"name":"John"}}

          Lists are also accessible:
          {items[0]}

          If empty, the entire JSON file will be output without modification.
          This is useful if you want to split your input (using -o OUTPUTFILE).

  OUTPUTFILE
          Appends output to a file. The outputfile can be dynamic, depending on your JSON.

          Example: Saves 'text' field of every JSON object into its own file:
          cat objects/*.json | json_decode "{text}" -o "objectdump_{id}.txt"
