import math
import random
import Tkinter
import pyaudio
import wave
import sys

class Happy_Birthday:
  def __init__(self, master): #master is a window
    self.master=master
    frame=Tkinter.Frame(master)
    frame.pack()  

    #Constants
    self.WIDTH = 900
    self.HEIGHT = 600

    #Sound initialization stuff
    self.p = pyaudio.PyAudio()
    self.stream = []

    #Text and variables
    self.button_text="Click me!"
    self.clickcount = 0
    self.year_count = 0
    self.bad_dot_number = 0
    self.colors=["pale violet red", "dark orange", "medium sea green", "dodger blue", "medium purple"]
    self.good_dot_list=[]
    self.bad_dot_list=[]
    self.dots_to_remove = []
    self.lets_not_recurse_too_far=0
    self.clicked_a_bad_dot = False
    self.clicked_the_dot = False
    self.clicked_wrong_dot = False
    self.finished = False

    #Widgets
    self.c=Tkinter.Canvas(frame,width=self.WIDTH,height=self.HEIGHT, background = "light goldenrod yellow")
    self.c.pack(side=Tkinter.TOP)
    self.c.bind('<Button-1>', self.mouse_click)
    self.c.create_rectangle(3, 3, 899, 599, activeoutline="Black")
      #Canvas text
    self.canvas_text = self.c.create_text((self.WIDTH/2), 35)
    self.c.itemconfig(self.canvas_text, text="Let's play a birthday game!", tag='message')
      #The button
    self.b=Tkinter.Button(frame, text=self.button_text, command=self.button)
    self.b.pack(side=Tkinter.TOP)

#Sound function
  def sound(self, filename):
    wf = wave.open(filename, 'rb')
    def callback(in_data, frame_count, time_info, status):
      data = wf.readframes(frame_count)
      return (data, pyaudio.paContinue)
    stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)
#    stream.start_stream()                                                                 
    return (stream, wf)

#Clicking related functions
  def button(self):
    if self.clickcount == 0:
      self.sound('file_1.wav')
      self.c.itemconfig(self.canvas_text, text=
                        "   First click all the empty dots \n  Then click the numbered dot! \n   (Please wait until the music\nfinishes and click the dots slowly.)", tag='message')
      self.year_count += 1
      self.clickcount += 1
      self.make_a_good_dot()
      self.make_a_bad_dot()
      self.make_a_bad_dot()
      self.make_a_bad_dot()
      self.make_a_bad_dot()
      self.b.config(text="Click the dots.")
    elif self.clickcount == 1 and not self.finished:
      self.b.config(text="Don't click me! Click the dots!")
      self.clickcount += 1
    elif self.clickcount > 1 and self.clickcount < 5 and not self.finished:
      self.b.config(text="I know it's your birthday, but do as you're told!!!") 
      self.sound('file_2.wav')
      self.clickcount += 1
    elif self.clickcount >= 5 and not self.finished:
      self.b.config(text="For the love of God...")
    if self.finished and self.clickcount < 100:
      self.sound('file_6.wav')
      end_message = self.canvas_text = self.c.create_text((self.WIDTH/2), self.HEIGHT/2)
      self.c.itemconfig(end_message, text="Happy Birthday, Helena!", tag='message')
      easter_egg= self.canvas_text = self.c.create_text((self.WIDTH/2), (self.HEIGHT-10))
      self.c.itemconfig(easter_egg, text="Play again and try clicking the button a bunch for funsies! (Or click it now for credits.)", tag='message')
      self.clickcount = 100
    elif self.finished and self.clickcount == 100:
      self.roll_credits()

  def mouse_click(self, event):
    coord = (event.x, event.y)
    self.clickcheck(coord)
    right_dot = self.clicked_the_dot
    wrong_dot = self.clicked_wrong_dot
    bad_dot = self.clicked_a_bad_dot
    if self.year_count < 5 and right_dot and not (self.finished or self.bad_dot_list):
      self.sound('file_3.wav')
      self.year_count += 1
      self.c.itemconfig(self.canvas_text, text="Whee!", tag='message')
      self.make_a_good_dot()
      self.make_a_bad_dot()
      self.make_a_bad_dot()
      self.make_a_bad_dot()
      self.make_a_bad_dot()
      self.clicked_the_dot = False
      self.clicked_wrong_dot = False
      self.clicked_a_bad_dot = False
    elif not (right_dot or wrong_dot or bad_dot or self.finished):
      self.sound('file_4.wav')
      self.c.itemconfig(self.canvas_text, text="That's not a dot!", tag='message')
    elif (self.bad_dot_list and right_dot and not (self.finished or bad_dot)) or wrong_dot:
      self.sound('file_8.wav')
      self.c.itemconfig(self.canvas_text, text="Wrong dot!", tag='message')
      self.clicked_wrong_dot = False
    elif bad_dot and not self.finished:
      self.sound("file_5.wav")
      self.c.itemconfig(self.canvas_text, text="Woo!", tag='message')
      for dot in list(self.dots_to_remove):
          self.delete_dot(dot)
          self.bad_dot_list.remove(dot)
          self.dots_to_remove.remove(dot)
      self.clicked_a_bad_dot = False
    else:
      self.finish()
    
#Helper functions
  def distance_check(self, coord, dot):
    result =  math.sqrt((coord[0]-dot.x)**2+(coord[1]-dot.y)**2)
    if result  <= 90:
      return True
    else:
      return False

  def clickcheck(self, coordinates):
    if self.bad_dot_list:
      good_distance_list = []
      for dot in self.bad_dot_list:
        good_distance_list.append(self.distance_check(coordinates, dot))
      if True in good_distance_list:
        x = good_distance_list.index(True)
        self.dots_to_remove.append(self.bad_dot_list[x])
        self.clicked_a_bad_dot = True
      good_distance_list = []
    good_distance_list = self.distance_check(coordinates, self.good_dot_list[-1])       
    if good_distance_list:
      self.clicked_the_dot = True
    else:
      self.clicked_the_dot = False
      for x in list(self.good_dot_list[:-1]):
        if self.distance_check(coordinates, x):
          self.clicked_wrong_dot = True 
  
  def finish(self):
    self.c.itemconfig(self.canvas_text, text="  Congratulations!\nLook at the button!", tag='message')
    self.b.config(text="Okay, you can click me again.")
    self.finished = True

  def roll_credits(self):
    self.sound('file_7.wav')
    self.c.delete('message')
    end_text = self.c.create_text(self.WIDTH/2, self.HEIGHT/2)
    self.c.itemconfig(end_text, text = "Game Design ... Linnea Damer\nChief Programmer ... Linnea Damer\nAssistant Programmer ... Linnea Damer\nChief Debugger ... Linnea Damer\nEmpyrean Debugging Assistance ... Steven Damer\n\nSound Effects ... Linnea Damer\nSound Engineering ... Linnea Damer\nSnacks ... Linnea Damer\nKnowledge Provider ... Steven Damer\nAbsurdity ... Linnea Damer\n\nSpecial Thanks to Steven Damer")
    

#Dealing with dots
  def make_a_good_dot(self):
    dotnotmade = True
    while dotnotmade:
      x = random.randint(60, self.WIDTH-60)
      y = random.randint(60, self.HEIGHT-60)
      xcheck = [abs(x-z.x) for z in self.bad_dot_list+self.good_dot_list]
      ycheck = [abs(y-z.y) for z in self.bad_dot_list+self.good_dot_list]
      coordcheck = zip(xcheck, ycheck)
      booleancheck = [u > 120 or t > 120 for u,t in coordcheck]
      if False not in booleancheck:
        coordinates = (x,y)
        color = self.colors[(self.year_count%5)]
        number = self.year_count
        new_dot = Dot(coordinates, color, number, True)
        self.good_dot_list.append(new_dot)
        new_dot.draw(self.c)
        dotnotmade = False
      else:
        continue
    if not dotnotmade:
      print "big dot at:" + str(coordinates)

  def make_a_bad_dot(self):
    dotnotmade = True
    while dotnotmade:
      x = random.randint(60, self.WIDTH-60)
      y = random.randint(60, self.HEIGHT-60)
      xcheck = [abs(x-z.x) for z in self.bad_dot_list+self.good_dot_list]
      ycheck = [abs(y-z.y) for z in self.bad_dot_list+self.good_dot_list]
      coordcheck = zip(xcheck, ycheck)
      booleancheck = [u > 90 or t > 90 for u,t in coordcheck]
      if False not in booleancheck:
        coordinates = (x,y)
        color = self.colors[(self.year_count%5)]
        number = self.bad_dot_number
        new_dot = Dot(coordinates, color, number, False)
        self.bad_dot_list.append(new_dot)
        new_dot.draw(self.c)
        dotnotmade = False
      else:
        continue
      self.bad_dot_number += 1
      if not dotnotmade:
        print "little dot at:" + str(coordinates)

  def delete_dot(self, dot):
    dot.undraw(self.c)
"""
    for other_dot in list(self.dot_list):      
      if other_dot.number > dot.number:
        other_dot.number_shift()
        self.c.addtag_withtag("dot"+str(other_dot.number), "dot"+str(other_dot.number+1))
        self.c.dtag("dot"+str(other_dot.number), "dot"+str(other_dot.number+1))
"""

class Dot:
  def __init__(self, coordinates, color, number, good):
    self.coordinates = coordinates
    self.x = coordinates[0]
    self.y = coordinates[1]
    self.color = color
    self.good = good
    self.number = number
    if self.good:
      self.radius = 60
    else: 
      self.radius = 30

  def draw(self, canvas):
    coordinates = (self.x+self.radius, self.y+self.radius, self.x-self.radius, self.y-self.radius)
    if self.good:
      canvas.create_oval(coordinates, fill=self.color, tag="good_dot"+str(self.number), outline = self.color)
      canvas.create_text((self.x, self.y), text = str(self.number), tag ="good_dot"+str(self.number))
    else:
      canvas.create_oval(coordinates, fill=self.color, tag="bad_dot"+str(self.number), outline = self.color)

  def undraw(self, canvas):
    if self.good:
      canvas.delete("good_dot"+str(self.number))
    else:
      canvas.delete("bad_dot"+str(self.number))

  def number_shift(self):
    self.number -= 1


if __name__ == "__main__":
  master=Tkinter.Tk()
  master.wm_title("It's your birthday!")
  window=Happy_Birthday(master)
  master.mainloop()
