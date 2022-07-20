import 'package:flutter/material.dart';
class Block extends StatelessWidget {
    Block({Key? key, required this.bgcolor, required this.text}) : super(key: key);
    final Color bgcolor;
	final String text;
    @override
    Widget build(BuildContext context) {
        return Container(
			margin: EdgeInsets.symmetric(horizontal: 4, vertical: 8),
			padding: EdgeInsets.all(8),
			 decoration: BoxDecoration(
				color: bgcolor,
				borderRadius: BorderRadius.all(Radius.circular(10)),
			),
			child: Text('$text', style: TextStyle(color: Colors.white)),
		);
    }
}