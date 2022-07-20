import xml.etree.ElementTree as ET
import sys
import re
import textwrap
kwds = ['src']
styleComponents = ['Padding', 'Margin']
def getparams(xml):
    pattern = re.compile('\{([^\{\}]+)\}')
    params = []
    if xml.text is not None:
        params += pattern.findall(xml.text)
    for _, v in xml.attrib.items():
        params += pattern.findall(v)
    for child in xml:
        params += getparams(child)
    return params

def removeparams(text):
    pattern = '\{([^\{\}]+)\}'
    def getname(str):
        return f"${str.group(1).split(':')[1].strip()}"
    return re.sub(pattern, getname, text)

def getname(str):
    if str[0] != '{' or str[-1] != '}': return None
    else: return str[1:-1].split(':')[1].strip()

def processMargin(xml):
    res = ""
    res += "margin: "
    if "left" in xml.attrib or "right" in xml.attrib or "top" in xml.attrib or "bottom" in xml.attrib:
        res += f"EdgeInsets.only(left: {xml.attrib.get('left') or 0}, right: {xml.attrib.get('right') or 0}, top: {xml.attrib.get('top') or 0}, bottom: {xml.attrib.get('bottom') or 0}"
    elif "vertical" in xml.attrib or "horizontal" in xml.attrib:
        res += f"EdgeInsets.symmetric(horizontal: {xml.attrib.get('horizontal') or 0}, vertical: {xml.attrib.get('vertical') or 0})"
    elif "all" in xml.attrib:
        res += f"EdgeInsets.all({xml.attrib['all']})"
    else:
        raise Exception("margin tag must contain one of the following: 'left', 'right', 'top', 'bottom', 'horizontal', 'vertical', 'all'")
    return res

def processPadding(xml):
    res = ""
    res += "padding: "
    if "left" in xml.attrib or "right" in xml.attrib or "top" in xml.attrib or "bottom" in xml.attrib:
        res += f"EdgeInsets.only(left: {xml.attrib.get('left') or 0}, right: {xml.attrib.get('right') or 0}, top: {xml.attrib.get('top') or 0}, bottom: {xml.attrib.get('bottom') or 0}"
    elif "vertical" in xml.attrib or "horizontal" in xml.attrib:
        res += f"EdgeInsets.symmetric(horizontal: {xml.attrib.get('horizontal') or 0}, vertical: {xml.attrib.get('vertical') or 0})"
    elif "all" in xml.attrib:
        res += f"EdgeInsets.all({xml.attrib['all']})"
    else:
        raise Exception("padding tag must contain one of the following: 'left', 'right', 'top', 'bottom', 'horizontal', 'vertical', 'all'")
    return res

def processIcon(xml):
    styles = [""]
    for style in xml.attrib:
        if style == "color":
            styles.append(f"color: Colors.{xml.attrib['color']}")
        elif style == "size":
            styles.append(f"size: {xml.attrib['size']}")
    return f"Icon(Icons.{xml.text}{', '.join(styles)})"

def processText(xml):
    styles = []
    for style in xml.attrib:
        if style == 'size':
            styles.append(f"fontSize: {xml.attrib['size']}")
        elif style == 'color':
            color = getname(xml.attrib['color']) or f"Colors.{xml.attrib['color']}"
            styles.append(f"color: {color}")
    return f"Text('{removeparams(xml.text)}', style: TextStyle({','.join(styles)}))"

def processContainer(xml):
    res = ""
    res += "Container(\n"
    decoration = []
    for style in xml.attrib:
        if style == 'bg':
            bg = getname(xml.attrib['bg']) or f"Colors.{xml.attrib['bg']}"
            decoration.append(f"\tcolor: {bg},")
        elif style == 'bradius':
            decoration.append(f"\tborderRadius: BorderRadius.all(Radius.circular({xml.attrib['bradius']})),")
        elif style == 'width':
            res += f"\twidth: {xml.attrib['width']},\n"
        elif style == 'height':
            res += f"\theight: {xml.attrib['height']},\n"
    for prop in xml[:-1]:
        res += "\t" + process_xml(prop) + ",\n"
    if len(decoration) > 0: res += "\t decoration: BoxDecoration(\n" + textwrap.indent("\n".join(decoration), "\t") + "\n\t),\n"
    res += "\tchild: " + process_xml(xml[-1]).replace("\n", "\n\t") + ",\n"
    res += ")"
    return res

def processCenter(xml):
    indentedchild = process_xml(xml[0]).replace('\n', '\n\t\t')
    return \
f"""Center(
    child: {indentedchild},
)"""


def processExpanded(xml):
    indentedchild = process_xml(xml[0]).replace('\n', '\n\t\t')
    return \
f"""Expanded(
    child: {indentedchild},
)"""

def processColumn(xml):
    children = []
    for child in xml:
        if child.tag in styleComponents: continue # add support for styles later
        children.append(process_xml(child))
    fchildren = textwrap.indent(",\n".join(children), "\t\t")
    return \
f"""Column(
    children: [
{fchildren}
    ]
)"""

def processRow(xml):
    children = []
    for child in xml:
        if child.tag in styleComponents: continue # add support for styles later
        children.append(process_xml(child))
    fchildren = textwrap.indent(",\n".join(children), "\t\t")
    return \
f"""Row(
    children: [
{fchildren}
    ]
)"""

def processButton(xml):
    onpressed = None
    for child in xml:
        if child.tag == 'Press':
            if onpressed is not None:
                raise Exception('cannot have two press attributes in a button')
            onpressed = textwrap.dedent(child.text).strip()
    fonpressed = 'null'
    if onpressed is not None:
        indented = onpressed.replace('\n', '\n\t')
        fonpressed = \
f"""() {{
{indented}
}}""".replace('\n', '\n\t')
    if xml[-1].tag == 'Text':
        return \
f"""TextButton(
    onPressed: {fonpressed},
    child: {process_xml(xml[-1])}
)"""
    if xml[-1].tag == 'Icon':
        styles = ""
        if 'size' in xml[-1].attrib:
            styles += f"iconSize: {xml[-1].attrib['size']},"
        return \
f"""IconButton(
    icon: {process_xml(xml[-1])},
    onPressed: {fonpressed},
    {styles}
)"""

def processStateless(xml):
    params = getparams(xml)
    formattedparams = [""]
    paramdecls = []
    for param in params:
        spl = param.split(':')
        name = spl[1].strip()
        formattedparams.append(f"required this.{name}")
        if spl[0].strip() == 'str':
            paramdecls.append(f"final String {name};")
        elif spl[0].strip() == 'color':
            paramdecls.append(f"final Color {name};")
    declconcat = "\n\t".join(paramdecls)
    indentedchild = process_xml(xml[0]).replace('\n', '\n\t\t')
    return f"""class {xml.attrib['name']} extends StatelessWidget {{
    {xml.attrib['name']}({{Key? key{", ".join(formattedparams)}}}) : super(key: key);
    {declconcat}
    @override
    Widget build(BuildContext context) {{
        return {indentedchild};
    }}
}}"""

def processStateful(xml):
    state = None
    for child in xml:
        if child.tag == 'State':
            state = child
            break
    vars = []
    params = []
    types = []
    initContent = [] # things that go in initState()
    for k, v in state.attrib.items():
        type, val = v.split(':')
        val = val.strip()
        type = type.strip()
        isvar = val[0] == '{' and val[-1] == '}'
        if type == 'num':
            if isvar:
                vars.append(f"int {k.strip()} = 0;")
                initContent.append(f"{k.strip()} = widget.{val[1:-1]};")
                params.append(val[1:-1])
                types.append('int')
            else: vars.append(f"int {k.strip()} = {val};")
        if type.strip() == 'str':
            if isvar:
                vars.append(f"String {k.strip()} = '';")
                initContent.append(f"{k.strip()} = widget.{val[1:-1]};")
                params.append(val[1:-1])
                types.append('String')
            vars.append(f"String {k.strip()} = '{val}';")
    body = process_xml(xml[-1]).replace('\n', '\n\t\t')
    indentedVars = textwrap.indent("\n".join(vars), "\t")
    paramPass = map(lambda s: f"required this.{s}", params)
    paramDecl = map(lambda x, y: f"final {x} {y};", types, params)
    indentedDecl = textwrap.indent("\n".join(paramDecl), "\t")
    initcontent = textwrap.indent("\n".join(initContent), "\t\t")
    return \
f"""class {xml.attrib['name']} extends StatefulWidget {{
    const {xml.attrib['name']}({{Key? key, {", ".join(paramPass)}}}) : super(key: key);
{indentedDecl}
    @override
    State<{xml.attrib['name']}> createState() => _{xml.attrib['name']}State();
}}

class _{xml.attrib['name']}State extends State<{xml.attrib['name']}> {{
{indentedVars}
    @override
    void initState() {{
{initcontent}
        super.initState();
    }}
    @override
    Widget build(BuildContext context) {{
        return {body};
    }}
}}"""

def processWidget(xml):
    for child in xml:
        if child.tag == 'State':
            return processStateful(xml)
    return processStateless(xml)

def processMain(xml):
    imports = ""
    vars = []
    navactions = ""
    for child in xml:
        if child.tag == 'State':
            for k,v in child.attrib.items():
                type, val = v.split(':')
                if type.strip() == 'num':
                    vars.append(f"int {k.strip()} = {val.strip()};")
                if type.strip() == 'str':
                    vars.append(f"String {k.strip()} = '{val.strip()}';")
        elif child.tag == 'Navbar':
            for desc in child:
                navactions += f"{process_xml(desc)},\n"
    body = process_xml(xml[-1]).replace('\n', '\n\t\t\t')
    indentedVars = textwrap.indent("\n".join(vars), "\t")
    indentedactions = textwrap.indent(navactions, '\t')
    appbaractions = textwrap.indent(f"actions: [\n{indentedactions}\n]", "\t\t\t")
    return imports + \
f"""
void main() {{
    runApp(const MyApp());
}}

class MyApp extends StatelessWidget {{
    const MyApp({{Key? key}}) : super(key: key);
    @override
    Widget build(BuildContext context) {{
        return MaterialApp(
            title: '{xml.attrib.get('title') or 'Flap app'}',
            theme: ThemeData(
                primarySwatch: Colors.{xml.attrib.get('swatch') or 'blue'},
            ),
            home: const MyHomePage(title: '{xml.attrib.get('title') or 'Flap app'}'),
            debugShowCheckedModeBanner: false,
        );
    }}
}}

class MyHomePage extends StatefulWidget {{
    const MyHomePage({{Key? key, required this.title}}) : super(key: key);

    final String title;
    @override
    State<MyHomePage> createState() => _MyHomePageState();
}}

class _MyHomePageState extends State<MyHomePage> {{
{indentedVars}
    @override
    Widget build(BuildContext context) {{
        return Scaffold(
            appBar: AppBar(
                title: Text(widget.title),
{appbaractions}
            ),
            body: {body},
        );
    }}
}}
"""

def process_xml(xml):
    if f"process{xml.tag}" not in globals():
        params = []
        for param in xml.attrib:
            if param in kwds:
                continue
            if xml.attrib[param].split(':')[0].strip() == 'color':
                params.append(f"{param}: Colors.{xml.attrib[param].split(':')[1].strip()}")
            elif xml.attrib[param].split(':')[0].strip() == 'num':
                params.append(f"{param}: {xml.attrib[param].split(':')[1].strip()}")
            else: params.append(f"{param}: '{xml.attrib[param]}'")
        return f"{xml.tag}({', '.join(params)})"
    return globals()[f"process{xml.tag}"](xml)

def parse_file(filename):
    tree = ET.parse(f"{filename}.xml")
    root = tree.getroot()
    imports = ["import 'package:flutter/material.dart';"]
    for child in root:
        if child.tag == 'link':
            if 'src' not in child.attrib:
                raise Exception("a 'link' element must contain the 'src' tag")
            parse_file(child.attrib['src'])
            imports.append(f"import '{child.attrib['src']}.dart';")
    fo = open(f"src/lib/{filename}.dart", "w")
    fo.write("\n".join(imports) + "\n")
    fo.write(process_xml(root))
if len(sys.argv) == 1:
    parse_file("main")
else: 
    parse_file(sys.argv[1])