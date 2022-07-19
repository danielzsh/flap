# Flap
A minimal compiler from readable XML to Flutter. Designed as an easy way to get into Flutter, not as a replacement.
## Prerequisites
1. Flutter installed
2. Python installed (should come with most OSes)
## Usage Guide
1. Navigate to the directory you want your project in
2. run `flutter create src`
3. copy `processor.py` into the directory
4. create your `.xml` files
5. run `python processor.py` to generate your source files
6. If you don't already have `flutter` running:
```sh
cd src/
flutter run lib/main.dart
```
If you do, just go to the console window where you have it running and hit `r` to reload or `R` to restart.

(Note: many features aren't implemented yet and the order in which features are added is very arbitrary, so if any of you guys want to see a feature implemented feel free to open an issue and i'll try to prioritize it)
## Components
### Main
Used to specify the entry point of the application:
```xml
<!--main.xml-->
<Main title="my app">
    <Text>I love Flap!</Text>
</Main>
```
### Widget
Used to create a reusable widget:
```xml
<!--TestWidget.xml-->
<Widget name="Test">
    <Center>
        <Container bg="{color: bgcolor}">
            <Padding all="8"/>
            <Text size="20">
                {str: text} and more
            </Text>
        </Container>
    </Center>
</Widget>
```
Text in brackets specifies parameters in the form `{type: name}`, and the widget can be used like so:
```xml
<Link src="TestWidget" />
...
<Test text="some text" bgcolor="color: blue"/>
```
Parameter names cannot be style names (e.g. `bg`). Note that any parameter type other than `str` must be specified (note `"some text"` vs `"color: blue"`). 

A note about the `bg` argument: you only need to specify `color: <color>` if you're passing the color as a parameter. If the background color is fixed, you should write `bg: <color>`. (Specifying a type will make flap think you're referencing a variable)
### Container
```xml
<Container bg="green">
    <Margin all="8" />
    <Padding all="8" />
    <Text>The last element is always the child.</Text>
<Container>
```
A simple wrapper that allows you to style its child (the last element). Accepts `Margin` and `Padding` elements to add spacing, and the `bg` attribute to set the background color.
### Button
```xml
<Button>
    <Press>
        print('Pressed');
        print('Check formatting');
    </Press>
    <Text>{str: buttontext}</Text>
</Button>
```
The `Press` element sets on `onPressed` for the `Button`: its contents must be written in `dart`. If `Press` is not specified the `Button` will be disabled. The `child` tag can be either `Text` or `Icon`.
### Text
```xml
<Text size="20" color="white">White text: font size 20</Text>
```
Plain text: accepts `size` and `color` attributes.
### Icon
```xml
<Icon color="red" size="100">delete</Icon>
```
Pulls an icon from the Flutter `Icons` class.
### Row/Column
```xml
<Row>
    <Text>one</Text>
    <Text>two</Text>
    <Text>three</Text>
</Row>
```
Horizontal/vertical container.
### More examples: check out the `.xml` files in this repo
## Contribution
If you want to contribute to this project, here's a few tips to get you started:

1. `processor.py` is the only source file that should be modified (i.e. everything is crammed into one file)
2. The `processor` takes advantage of the `python` reflection system to make code refactoring easier, but this also means that all functions must be named as `process<Widget>` (e.g. `processContainer`, `processMargin`, `processMain`, etc.)
3. Each of said functions should return the generated source code without extra indents (i.e. base indentation should always be 0, but nested elements can and should be indented), newlines, commas or semicolons.

Example function and breakdown:
```py
def processRow(xml): # all functions accept am xml argument
    children = []
    for child in xml: # loops through all children
        if child.tag in styleComponents: continue # ignore style for now
        children.append(process_xml(child)) # add the string representation to the list of children
    fchildren = textwrap.indent(",\n".join(children), "\t\t") # indent children properly
    return \
f"""Row(
    children: [
{fchildren}
    ]
)""" # return the string representation
```

If you have any more questions about contribution, let me know by opening an issue.