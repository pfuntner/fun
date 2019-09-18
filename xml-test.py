#! /usr/bin/env python2

import pdb
import xml.etree.ElementTree as ET
# import defusedxml.ElementTree as ET

def visitHtmlTree(node, indent=0):
  if node != None:
    if isinstance(node, basestring):
      s = node.replace('\n', '').strip()
      if s:
        print '{indent}{text}'.format(indent=' '*(2*indent), text=s)
    else:
      print '{indent}<{tag}>'.format(indent=' '*(2*indent), tag=node.tag)
      visitHtmlTree(node.text, indent+1)
      for child in node:
        visitHtmlTree(child, indent+1)
      print '{indent}</{tag}>'.format(indent=' '*(2*indent), tag=node.tag)

data = """
<html>
  <body>
    <p>
      Paragraph <span class='para-num'>one</span>
    </p>
    <p>
      Paragraph <span class='para-num'>two</span>
    </p>
  </body>
</html>
"""

root = ET.fromstring(data)
visitHtmlTree(root)

print '\nparagraphs:'
for pos, paragraph in enumerate(list(root.iter('p'))):
  if pos > 0:
    print ''
  print '  {pos}:'.format(**locals())
  visitHtmlTree(paragraph, 2)

# pdb.set_trace()
