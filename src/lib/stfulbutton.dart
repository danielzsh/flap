import 'package:flutter/material.dart';
class StfulDemo extends StatefulWidget {
    const StfulDemo({Key? key, required this.initial}) : super(key: key);
	final int initial;
    @override
    State<StfulDemo> createState() => _StfulDemoState();
}

class _StfulDemoState extends State<StfulDemo> {
	int content = 0;
    @override
    void initState() {
		content = widget.initial;
        super.initState();
    }
    @override
    Widget build(BuildContext context) {
        return TextButton(
		    onPressed:  () {
			setState(() {
				    content++;
				});
			},
		    child: Text('$content', style: TextStyle())
		);
    }
}