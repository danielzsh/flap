import 'package:flutter/material.dart';
import 'block.dart';
import 'stfulbutton.dart';

void main() {
    runApp(const MyApp());
}

class MyApp extends StatelessWidget {
    const MyApp({Key? key}) : super(key: key);
    @override
    Widget build(BuildContext context) {
        return MaterialApp(
            title: 'My App',
            theme: ThemeData(
                primarySwatch: Colors.grey,
            ),
            home: const MyHomePage(title: 'My App'),
        );
    }
}

class MyHomePage extends StatefulWidget {
    const MyHomePage({Key? key, required this.title}) : super(key: key);

    final String title;
    @override
    State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
	int count = 0;
	String content = 'some text';
    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(
                title: Text(widget.title),
            ),
            body: Column(
			    children: [
					Block(text: '$count', bgcolor: Colors.blue),
					Block(text: '$content', bgcolor: Colors.green),
					TextButton(
					    onPressed:  () {
						setState(() {
							    count++;
							    content += 'a';
							});
						},
					    child: Text('Click me', style: TextStyle())
					),
					IconButton(
					    icon: Icon(Icons.delete, color: Colors.red),
					    onPressed: () {
						setState(() {
							    count = 0;
							    content = 'some text';
							});
						},
			    
					),
					StfulDemo(initial: 0)
			    ]
			),
        );
    }
}
