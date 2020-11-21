
import re
import sys

# filter_name = r'(\"name\": (?P<name>[a-z]*)|\"description\": (?P<description>[a-z]*))'

filter_name = r'(.*\"name\": (?P<name>[a-z]*))'
filter_description = r'.*(\"description\": (?P<description>[a-z]*))'

for line in sys.stdin:
    line = line.strip()
    name = re.match(filter_name, line)
    description = re.match(filter_description, line)
    if (name.group('name') == 'null' and description.group('description') == 'null'):
        continue
    print(line)