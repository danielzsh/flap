import xml.etree.ElementTree as ET
import textwrap
def process_xml(xml):
    print(xml.tag)
    res = ""
    if xml.tag == "Container":
        res += "return Container(\n"
        for prop in xml[:-1]:
            res += "\t" + process_xml(prop) + ",\n"
        res += "\tchild: " + process_xml(xml[-1]) + ",\n"
        res += ");"
    elif xml.tag == "margin":
        res += "margin: "
        if "all" in xml.attrib:
            res += f"EdgeInsets.all({xml.attrib['all']})"
    elif xml.tag == "Text":
        res = f"Text('{xml.text}')"
    return res
tree = ET.parse('test.xml')
root = tree.getroot()
for child in root:
    print(child.tag)
fo = open("test.dart", "w")
fo.write("import 'package:flutter/material.dart';\n")
if root.tag == 'Widget':
    fo.write(f"""class {root.attrib['name']} extends StatelessWidget {{
    {root.attrib['name']}({{Key? key}}) : super(key);
    @override
    Widget build(BuildContext context) {{
{textwrap.indent(process_xml(root[0]), '        ')}
    }}
}}""")