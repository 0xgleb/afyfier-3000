import Reveal from 'reveal.js';
import Markdown from 'reveal.js/plugin/markdown/markdown.esm.js';

// This is the animation - copy it till it says the end of animation
const fs = `#version 300 es
precision mediump float;

uniform mediump vec2 u_resolution;
uniform mediump float u_time;
uniform mediump float u_scroll;
in vec2 v_position;

out vec4 outColor;

float minus(float a, float b) {
  return a * abs(b -1.);
}

vec2 random2( vec2 p ) {
    return fract(sin(vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3))))*43758.5453);
}

#define PI 3.1415926535897932384626433832795

//this is a basic Pseudo Random Number Generator
float hash(in float n)
{
    return fract(sin(n)*43758.5453123);
}

void main() {

    //"squarified" coordinates
    vec2 xy = ( 2.* gl_FragCoord.xy - u_resolution.xy ) / u_resolution.y ;

    //rotating light
    vec3 center = vec3( sin( u_time ), 1., cos( u_time * .35 ) );

    //temporary vector
    vec3 pp = vec3(0.);

    //maximum distance of the surface to the center (try a value of 0.1 for example)
    float length = 10.;

    //this is the number of cells
    const float count = 50.;


    for( float i = 0.; i < count; i+=1. )
    {
        //random cell: create a point around the center

        //gets a 'random' angle around the center
        float an = sin( u_time * PI * .0000001 ) - hash( i ) * PI * 2.;

        //gets a 'random' radius ( the 'spacing' between cells )
        float ra = sqrt( hash( an ) ) * 1.;

        //creates a temporary 2d vector
        vec2 p = vec2( center.x + cos( an ) * ra, center.z + sin( an ) * ra );

        //finds the closest cell from the fragment's XY coords

        //compute the distance from this cell to the fragment's coordinates
        float di = distance( xy, p );

        //and check if this length is inferior to the minimum length
        length = min( length, di );

  //if this cell was the closest
        if( length == di )
        {
            //stores the XY values of the cell and compute a 'Z' according to them
            pp.xy = p;
        }
    }

    //shimmy shake:
    //uses the temp vector's coordinates and uses the angle and the temp vector
    //to create light & shadow (quick & dirty )
    vec3 shade = vec3( 1. ) * ( 1. - max( 0.0, dot( pp, center ) ) );
    vec3 col = pp;
    //vec3 col.r = pp.r + shade.r;
    col.b = pp.b + shade.b;
    // col.g = pp.g + shade.g;

    col.r = col.r*0.1+0.9;
    col.g = 0.;
    //final colo
    outColor = vec4( col, 1. );
}

`
const vs = `#version 300 es

uniform mediump vec2 u_resolution;
in vec2 a_position;

out vec2 v_position;

void main() {
  vec2 zeroToOne = a_position;
  vec2 zeroToTwo = zeroToOne * 2.0;
  vec2 clipSpace = zeroToTwo - 1.0;
  v_position = clipSpace;
  gl_Position = vec4(clipSpace, 0, 1);
}
`
const canvas = document.getElementById("bckg");
const webGl = canvas.getContext("webgl2");

if (!webGl) {
  console.log("No WebGl2!");
} else {
  runWebGl(webGl);
};

function fail() {
  throw "Background refuses to work."
}

function createShader(gl, t, s) {
  const shader = gl.createShader(t);
  if (shader) {
    gl.shaderSource(shader, s);
    gl.compileShader(shader);
    const success = gl.getShaderParameter(shader, gl.COMPILE_STATUS);
    if (!success) {
      console.log(gl.getShaderInfoLog(shader));
      fail();
    };
  } else {fail();};
  return shader;
}

function runWebGl(gl) {
  let time = 0;
  const vshader = createShader(gl, gl.VERTEX_SHADER, vs);
  const fshader = createShader(gl, gl.FRAGMENT_SHADER, fs);

  const program = gl.createProgram();

  if (program) {
    gl.attachShader(program, vshader);
    gl.attachShader(program, fshader);
    gl.linkProgram(program);
    const success = gl.getProgramParameter(program, gl.LINK_STATUS);
    if (!success) {
      console.log(gl.getProgramInfoLog(program));
      fail();
    };
  } else {fail();};

  const positionAttributeLocation = gl.getAttribLocation(program, "a_position");
  const positionBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  const positions = [
    -1.0,  1.0,
     1.0,  1.0,
    -1.0, -1.0,
     1.0, -1.0,
  ];


  gl.bufferData(gl.ARRAY_BUFFER,
     new Float32Array(positions),
     gl.DYNAMIC_DRAW);

  const numComponents = 2;
  const type = gl.FLOAT;
  const normalize = false;
  const stride = 0;
  const offset = 0;

  const vao = gl.createVertexArray();
  gl.bindVertexArray(vao);
  gl.enableVertexAttribArray(positionAttributeLocation);
  gl.vertexAttribPointer(positionAttributeLocation, numComponents, type, normalize, stride, offset);

  const resolutionUniformLocation = gl.getUniformLocation(program, "u_resolution");
  const timeUniformLocation = gl.getUniformLocation(program, "u_time");
  const scrollUniformLocation = gl.getUniformLocation(program, "u_scroll");

  gl.useProgram(program);

  updateResolution();

  const ro = new ResizeObserver(updateResolution);
  ro.observe(document.querySelector("body"));

  step();


  function step() {
    time += 0.0015;
    const y = window.scrollY;

    gl.uniform1f(scrollUniformLocation, window.scrollY);
    gl.uniform1f(timeUniformLocation, time);
    redraw();
    window.requestAnimationFrame(step);
  }

  function updateResolution() {
    gl.canvas.width  = window.innerWidth;
    gl.canvas.height = window.innerHeight;
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.uniform2f(resolutionUniformLocation, gl.canvas.width, gl.canvas.height);
    gl.uniform1f(scrollUniformLocation, window.scrollY);
    redraw();
  }

  function redraw () {
    gl.clearColor(1,1,1,0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.drawArrays(gl.TRIANGLE_STRIP, offset, 4);
  };
};


// This is the end of animation - here comes the presentation script

let deck = new Reveal({
   plugins: [ Markdown ]
})

deck.initialize();
