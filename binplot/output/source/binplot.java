import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class binplot extends PApplet {

String[] lines;
int max;
int circ_diameter = 20;
float main_radius;
int maxPoints;

public void setup() {
  size(900,900);
  lines = loadStrings("out.txt");

  String[] lineData = lines[0].split(",");
  maxPoints = lineData.length;
  main_radius =  ((  maxPoints * (circ_diameter+4) ) / PI ) / 2;
  smooth(8);
  noStroke();

}

public void draw() {

  background(30);
  translate(width/2, height/2);
  for (int j=0; j < lines.length; j++) {
    String [] lineData = lines[j].split(",");
    for (int i=0; i < lineData.length; i++) {
      pushMatrix();
      rotate(radians(map(i, 0, lineData.length, 0, 360)));
      translate(main_radius - (j*circ_diameter*1.4f) ,0);
      if (lineData[i].equals("0") ) {fill(30); } else { fill(74,163,207 ); }
      ellipse(0,0, circ_diameter-j, circ_diameter-j);
      popMatrix();
    }

  }

  filter(BLUR, 1);
  saveFrame("out.jpg");
  exit();
}
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "--full-screen", "--bgcolor=#666666", "--hide-stop", "binplot" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
