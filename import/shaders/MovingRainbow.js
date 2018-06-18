

// http://glslsandbox.com/e#18039.0

PX.clips.MovingRainbow = {

  // params: {

  //   "p1": { value: 0.35, desc: "scale" }

  // },

  // fragmentFunctions: [

  //   [ "precision lowp float;",
  //     "uniform float time;",
  //     "uniform vec2 resolution;"
      
  //   ].join("\n")

  // ],

  constants: [

  ],

  fragmentMain: [
  "vec2 cPos = -1.0 + 2.0 * gl_FragCoord.xy / resolution.xy;",
  "float ratio = resolution.x / resolution.y;",
  "cPos.x *= ratio;",
  "float cLength = length(cPos);",
  "float speed = 3.0;",
  "vec2 uv = gl_FragCoord.xy / resolution.xy + (cPos / cLength) * (cos(cLength * 10.7 - time * speed) )* 0.9;",
  "   uv +=  (cPos / cLength) * (cos((uv) * 3.2 - time*0.4788 * speed) )* 0.7;",
  "uv*=.6;",
  "gl_FragColor = vec4(vec3(uv.x, uv.y, uv.y), 1.0);"

  ].join("\n")

};

