
from lxml import etree

root = etree.Element("html")
head = etree.SubElement(root, "head")
title = etree.SubElement(head, "title")
title.text = "This is Page Title"
body = etree.SubElement(root, "body")
heading = etree.SubElement(body, "h1", style="font-size:20pt", id="head")
heading.text = "Hello World!"
para = etree.SubElement(body, "p",  id="firstPara")
para.text = "This HTML is XML Compliant!"
para = etree.SubElement(body, "p",  id="secondPara")
para.text = "This is the second paragraph."

etree.dump(root)  # prints everything to console. Use for debug only


with open('input.html', 'wb') as f:
    f.write(etree.tostring(root, pretty_print=True))
