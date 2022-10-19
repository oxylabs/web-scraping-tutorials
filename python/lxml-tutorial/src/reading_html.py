from lxml import html
with open('input.html') as f:
    html_string = f.read()
tree = html.fromstring(html_string)
para = tree.xpath('//p/text()')
for e in para:
    print(e)
 
# Output
# This HTML is XML Compliant!
# This is the second paragraph