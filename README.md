# Flap
A minimal compiler from readable XML to Flutter.
## Prerequisites
1. Flutter installed
2. Python installed (should come with most OSes)
## Components
### Main
Used to specify the entry point of the application:
```xml
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
            <Text size="20">{str: text} and more</Text>
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
Note that any parameter type other than `str` must be specified (e.g. `color: <color>`). 

A note about the `bg` argument: you only need to specify `color: <color>` if you're passing the color as a parameter. If the background color is fixed, you should write `bg: <color>`. (Specifying a type will make flap think you're referencing a variable)