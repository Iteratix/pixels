// http://glslsandbox.com/e#19474.0

PX.clips.BullShit = {

	params: {

	},

	fragmentFunctions: [ 

		[ 
		].join("\n")

	],

	fragmentMain: [
		"vec2 position = ( gl_FragCoord.xy / resolution.xy );",
		"float rcolor = 0.0;",
		"rcolor += position.x * sin(time);",
		"//color += sin( position.y * sin( time / 10.0 ) * 40.0 ) + cos( position.x * sin( time / 25.0 ) * 40.0 );",
		"//color += sin( position.x * sin( time / 5.0 ) * 10.0 ) + sin( position.y * sin( time / 35.0 ) * 80.0 );",
		"//color *= sin( time / 10.0 ) * 0.5;",
		"float gcolor = 0.0;",
		"gcolor += (1.0 - position.x) * sin(time * 0.1);",
		"float bcolor = 0.0;",
		"bcolor += (1.0 - position.y) * sin(time * 0.1);",
		"gl_FragColor = vec4( vec3( rcolor, gcolor, bcolor ), 1.0 );",
	].join("\n")

};
