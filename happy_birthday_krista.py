import math
import random
import Tkinter
# import pyaudio
import wave
import sys

class Happy_Birthday:
  def __init__(self, master, age): #master is a window
    self.master=master
    frame=Tkinter.Frame(master)
    frame.pack()

    #Constants
    self.WIDTH = 900
    self.HEIGHT = 600

    #Sound initialization stuff
#    self.p = pyaudio.PyAudio()
#    self.stream = []

    #Text and variables
    self.age_limit = age
    self.button_text="Click me!"
    self.clickcount = 0
    self.year_count = 0
    self.colors=["firebrick", "dodger blue", "indian red", "dark orange", "medium purple", "medium sea green", "gold"]
    self.dot_list=[]
    self.wrongly_clicked_dots = []
    self.lets_not_recurse_too_far=0
    self.clicked_the_dot = False
    self.clicked_wrong_dot = False
    self.finished = False
    self.color_replacement = None

    #Widgets
    self.c=Tkinter.Canvas(frame,width=self.WIDTH,height=self.HEIGHT)
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
#  def sound(self, filename):
#    wf = wave.open(filename, 'rb')
#    def callback(in_data, frame_count, time_info, status):
#      data = wf.readframes(frame_count)
#      return (data, pyaudio.paContinue)
#    stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
#                channels=wf.getnchannels(),
#                rate=wf.getframerate(),
#                output=True,
#                stream_callback=callback)
##    stream.start_stream()
#    return (stream, wf)

#Clicking related functions
  def button(self):
    if self.clickcount == 0:
#      self.sound('file_1.wav')
      self.c.itemconfig(self.canvas_text, text=
"Always click the newest dot! \n    Don't click the others! \n (Please wait until the music\n  finishes to start clicking.)", tag='message')
      self.year_count += 1
      self.clickcount += 1
      self.make_a_dot()
      self.b.config(text="Click that dot.")
    elif self.clickcount == 1 and not self.finished:
      self.b.config(text="Don't click me! Click the dot!")
      self.clickcount += 1
    elif self.clickcount > 1 and self.clickcount < 5 and not self.finished:
      self.b.config(text="I know it's your birthday, but do as you're told!!!")
#      self.sound('file_2.wav')
      self.clickcount += 1
    elif self.clickcount >= 5 and not self.finished:
      self.b.config(text="For the love of God...")
    if self.finished and self.clickcount < 100:
#      self.sound('file_6.wav')
      end_message = self.canvas_text = self.c.create_text((self.WIDTH/2), self.HEIGHT/2)
      self.c.itemconfig(end_message, text="      Happy Birthday!\n    You won the game!\n   That means that you\n  still have good vision!", tag='message')
      easter_egg= self.canvas_text = self.c.create_text((self.WIDTH/2), (self.HEIGHT-10))
      self.c.itemconfig(easter_egg, text="Play again and try clicking the button a bunch for funsies! (Or click it now for credits.)", tag='message')
      self.clickcount = 100
    elif self.finished and self.clickcount == 100:
      self.roll_credits()

  def mouse_click(self, event):
    coord = (event.x, event.y)
    if self.clickcount > 0:
      self.clickcheck(coord)
      right_dot = self.clicked_the_dot
      wrong_dot = self.clicked_wrong_dot
      if self.year_count < self.age_limit and right_dot and not self.finished:
#        self.sound('file_3.wav')
        self.year_count += 1
        self.c.itemconfig(self.canvas_text, text="Woo!", tag='message')
        if self.color_replacement:
          self.make_a_dot(color = self.color_replacement)
          self.color_replacement = None
        else:
          self.make_a_dot()
      elif not (right_dot or wrong_dot or self.finished):
#        self.sound('file_4.wav')
        self.c.itemconfig(self.canvas_text, text="That's not a dot!", tag='message')
      elif wrong_dot and not self.finished:
        self.color_replacement = list(self.wrongly_clicked_dots)[-1].color
#        self.sound('file_5.wav')
        self.c.itemconfig(self.canvas_text, text="Wrong dot!", tag='message')
        for dot in list(self.wrongly_clicked_dots):
            self.delete_dot(dot)
            self.dot_list.remove(dot)
            self.wrongly_clicked_dots.remove(dot)
        self.clicked_wrong_dot = False
        self.year_count -= 1
      else:
        self.finish()

#Helper functions
  def distance_check(self, coord, dot):
    result =  math.sqrt((coord[0]-dot.x)**2+(coord[1]-dot.y)**2)
    if result  <= dot.radius:
      return True
    if dot.x < coord[0] and result <= (dot.radius + 2):
      return True
    else:
      return False

  def clickcheck(self, coordinates):
    good_distance = self.distance_check(coordinates, self.dot_list[-1])
    if good_distance:
      self.clicked_the_dot = True
    else:
      self.clicked_the_dot = False
      for x in list(self.dot_list[:-1]):
       if self.distance_check(coordinates, x):
         self.clicked_wrong_dot = True
         self.wrongly_clicked_dots.append(x)

  def finish(self):
    self.c.itemconfig(self.canvas_text, text="  Congratulations!\nLook at the button!", tag='message')
    self.b.config(text="Okay, you can click me again.")
    self.finished = True

  def roll_credits(self):
#    self.sound('file_7.wav')
    self.c.delete('message')
    end_text = self.c.create_text(self.WIDTH/2, self.HEIGHT/2)
    self.c.itemconfig(end_text, text = "Game Design ... Linnea Damer\nChief Programmer ... Linnea Damer\nAssistant Programmer ... Linnea Damer\nChief Debugger ... Linnea Damer\nEmpyrean Debugging Assistance ... Steven Damer\n\nSound Effects ... Linnea Damer\nSound Engineering ... Linnea Damer\nSnacks ... Linnea Damer\nKnowledge Provider ... Steven Damer\nAbsurdity ... Linnea Damer\n\nSpecial Thanks to Steven Damer\n\n\nHappy Birthday, Krista!")


#Dealing with dots
  def make_a_dot(self, color = None):
    dot_not_made = True
    while dot_not_made:
      x = random.randint(10, self.WIDTH-10)
      y = random.randint(10, self.HEIGHT-10)
      xcheck = [abs(x-z.x) for z in self.dot_list]
      ycheck = [abs(y-z.y) for z in self.dot_list]
      coordcheck = zip(xcheck, ycheck)
      booleancheck = [u > 10 and t > 10 for u,t in coordcheck]
      if False not in booleancheck:
        coordinates = (x,y)
        if color:
          color = color
        else:
          color = self.colors[(self.year_count%7)]
        number = self.year_count
        new_dot = Dot(coordinates, color, number)
        self.dot_list.append(new_dot)
        new_dot.draw(self.c)
        dot_not_made = False
      else:
        continue

  def delete_dot(self, dot):
    dot.undraw(self.c)
    for other_dot in list(self.dot_list):
      if other_dot.number > dot.number:
        other_dot.number_shift()
        self.c.addtag_withtag("dot"+str(other_dot.number), "dot"+str(other_dot.number+1))
        self.c.dtag("dot"+str(other_dot.number), "dot"+str(other_dot.number+1))

class Dot:
  def __init__(self, coordinates, color, number):
    self.coordinates = coordinates
    self.x = coordinates[0]
    self.y = coordinates[1]
    self.color = color
    self.number = number
    self.radius = 5

  def draw(self, canvas):
    coordinates = (self.x+self.radius, self.y+self.radius, self.x-self.radius, self.y-self.radius)
    canvas.create_oval(coordinates, fill=self.color, tag="dot"+str(self.number), outline = self.color)

  def undraw(self, canvas):
    canvas.delete("dot"+str(self.number))

  def number_shift(self):
    self.number -= 1


if __name__ == "__main__":
  master=Tkinter.Tk()
  master.wm_title("It's your birthday!")
  window=Happy_Birthday(master, 38)
  master.mainloop()
