def find_word_positions(text,key,textbox,color):
    # Split the text into lines
    lines = text.split("\n")
    tag=0
    # Loop through each line
    for line_num, line in enumerate(lines):
        # Split the line into words
        words = line.split()
        # Loop through each word in the line
        for word_num, word in enumerate(words):
            # If the word is "fun", print its position
            if word == key:
                start_pos = sum(len(words[i])+1 for i in range(word_num))
                end_pos = start_pos + len(word)
                print(f"{line_num+1}.{start_pos}-{line_num+1}.{end_pos}")
                # tag the second word in the text
                textbox.tag_add(f"{key}.{tag}.{start_pos}", f"{line_num+1}.{start_pos}", f"{line_num+1}.{end_pos}")
                # configure the color of the tagged text
                textbox.tag_config(f"{key}.{tag}.{start_pos}", foreground=color)
                tag+=1



import tkinter as tk
from customtkinter import CTkTextbox

root = tk.Tk()

text = 'This is a test fun text.'


textbox = CTkTextbox(root, height=100, width=500)
textbox.insert(tk.END, text)

find_word_positions(text,textbox)

textbox.pack()
root.mainloop()


import tkinter as tk

# Create the Tkinter window
root = tk.Tk()

# Create the canvas
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Create a rectangle and a text item, and add them to a tag
rect = canvas.create_rectangle(50, 50, 150, 150, fill="blue")
text = canvas.create_text(100, 100, text="Hello, world!")
canvas.addtag_withtag("group", rect)
canvas.addtag_withtag("group", text)

# Define a function to move the group
def move_group(event):
    # Get the current coordinates of the group
    x0, y0, x1, y1 = canvas.bbox("group")

    # Calculate the distance to move the group based on the mouse event
    dx = event.x - x0
    dy = event.y - y0

    # Move each item in the group
    for item in canvas.find_withtag("group"):
        x, y = canvas.coords(item)
        canvas.coords(item, x+dx, y+dy)

# Bind the move_group function to the left mouse button press event
canvas.tag_bind("group", "<Button-1>", move_group)

# Start the Tkinter event loop
root.mainloop()




import tkinter as tk

def on_press(event):
    # Get the x and y coordinates of the mouse click event
    x, y = event.x, event.y
    # Find the item on the canvas that was clicked
    item = event.widget.find_closest(x, y)[0]
    # Set the selected item
    canvas.itemconfig(item, fill='red')
    canvas.selected_item = item
    # Save the x and y coordinates of the mouse click
    canvas.drag_start_x = x
    canvas.drag_start_y = y

def on_drag(event):
    # Calculate the distance the mouse has moved since the last drag event
    dx = event.x - canvas.drag_start_x
    dy = event.y - canvas.drag_start_y
    # Move the selected item by the same amount
    canvas.move(canvas.selected_item, dx, dy)
    # Save the new x and y coordinates of the mouse
    canvas.drag_start_x = event.x
    canvas.drag_start_y = event.y

def on_release(event):
    # Reset the selected item
    canvas.itemconfig(canvas.selected_item, fill='blue')
    canvas.selected_item = None

# Create a new Tkinter window and canvas
root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Draw some rectangles on the canvas
rect1 = canvas.create_rectangle(50, 50, 100, 100, fill='blue')
rect2 = canvas.create_rectangle(150, 150, 200, 200, fill='blue')
rect3 = canvas.create_rectangle(250, 250, 300, 300, fill='blue')

# Bind mouse events to the canvas
canvas.bind('<ButtonPress-1>', on_press)
canvas.bind('<B1-Motion>', on_drag)
canvas.bind('<ButtonRelease-1>', on_release)

# Start the Tkinter event loop
root.mainloop()
import tkinter
from tkinter.font import Font

class Layout(tkinter.Frame):

    def __init__(self, root):
        tkinter.Frame.__init__(self, root)
        self.root = root
        self.font = Font(self, "Arial 10")  # create font object
        self.fontsize = 10  # keep track of exact fontsize which is rounded in the zoom
        self.canvas = tkinter.Canvas(self, width=512, height=512, background="white")
        self.canvas.pack(expand=tkinter.YES,side="left" ,fill=tkinter.BOTH)
        #self.xsb = tkinter.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        #self.ysb = tkinter.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        #self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        #self.canvas.configure(scrollregion=(0,0,1000,1000))

        #self.xsb.grid(row=1, column=0, sticky="ew")
        #self.ysb.grid(row=0, column=1, sticky="ns")
        #self.canvas.grid(row=0, column=0, sticky="nsew")
        #self.grid_rowconfigure(0, weight=1)
        #self.grid_columnconfigure(0, weight=1)

        # This is what enables using the mouse:
        self.canvas.bind('<ButtonPress-1>', self.move_start)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        
        #linux scroll
        self.canvas.bind("<Button-4>", self.zoomerP)
        self.canvas.bind("<Button-5>", self.zoomerM)
        #windows scroll
        self.canvas.bind("<MouseWheel>",self.zoomer)


    #create text
    def create_text(self, *args, **kwargs):
        text_item = self.canvas.create_text(*args, **kwargs, font=self.font,anchor="nw", activefill="blue", tags=("text", ""))
        #toolTrip(self.root,self.canvas,"",text_item,)
    def add_text(self,x,y,text,tag):
        text_item = self.canvas.create_text(x,y,text=text, font=self.font,anchor="nw", activefill="blue", tags=("text",tag))
        self.toolTrip(self.root,x,y,self.canvas,text,text_item,tag)
        return text_item
    #move
    def move_start(self, event):
        widget = event.widget

        #self.canvas.itemcget(widget, 'text')
        '''
        widget = event.widget
        a = event.widget.find_closest(event.x, event.y) 

        item_id = event.widget.find_closest(event.x, event.y)[0]
    
        # Get the tags associated with the item
        tags = event.widget.itemcget(item_id, 'tags')
    
        print(f"Clicked item with ID {item_id} and tags {tags}")
        print (a)
        print("Widget Type:", widget.type)
        print("Widget ID:", widget.find_withtag("current"))
        print("Widget Coordinates:", widget.coords("current"))
        print("-----------------------------------------------")
        #widget_tags = event.widget.tags()
        #if 'text' in widget_tags or 'label' in widget_tags:
        #    print(widget_tags)
        if isinstance(widget, tkinter.Text):
            print("Widget Type:", widget.type)
            print("Widget ID:", widget.find_withtag("current"))
            print("Widget Coordinates:", widget.coords("current"))
            item = event.widget.find_closest(event.x, event.y)
        if isinstance(event.widget, tkinter.Text):
        # Get the content of the text object
            text = event.widget.get("1.0", "end-1c")
            print(text)
        self.canvas.scan_mark(event.x, event.y)'''
        
    def on_press(self,event):
        # Get the x and y coordinates of the mouse click event
        x, y = event.x, event.y
        # Find the item on the canvas that was clicked
        item = event.widget.find_closest(x, y)[0]
        # Set the selected item
        self.canvas.itemconfig(item, fill='red')
        self.canvas.selected_item = item
        # Save the x and y coordinates of the mouse click
        self.canvas.drag_start_x = x
        self.canvas.drag_start_y = y

    def on_drag(self,event):
        # Calculate the distance the mouse has moved since the last drag event
        dx = event.x - self.canvas.drag_start_x
        dy = event.y - self.canvas.drag_start_y
        # Move the selected item by the same amount
        self.canvas.move(self.canvas.selected_item, dx, dy)
        # Save the new x and y coordinates of the mouse
        self.canvas.drag_start_x = event.x
        self.canvas.drag_start_y = event.y

    def on_release(self,event):
        # Reset the selected item
        self.canvas.itemconfig(self.canvas.selected_item, fill='blue')
        self.canvas.selected_item = None
    #windows zoom
    def zoomer(self,event):
        if (event.delta > 0):
            self.fontsize *= 1.1
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.fontsize *= 0.9
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.font.configure(size=int(self.fontsize))  # update fontsize
        #self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    #linux zoom
    def zoomerP(self,event):
        self.fontsize *= 1.1
        self.font.configure(size=int(self.fontsize))
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        #self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def zoomerM(self,event):
        self.fontsize *= 0.9
        self.font.configure(size=int(self.fontsize))
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        #self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def toolTrip(self,root,x,y,canvas,text,text_item,tag):
        x0, y0, x1, y1 = canvas.bbox(tag)
        text_width = x1 - x0
        # shorten text if width is more than 30 pixels
        if text_width > 30:
            text1 = text[:12] + "..." #+ text[-1:]
            # create a text item with the truncated text
            # change text of the text object
            canvas.itemconfig(text_item, text=text1)
            # create a tooltip that displays the full text when the mouse is hovered over the item
            tooltip = tkinter.Label(root, text=text, wraplength=300, justify="left")
            def show_tooltip(event):
                tooltip.place(x=event.x, y=event.y)
            def hide_tooltip(event):
                tooltip.place_forget()
                
            canvas.tag_bind(text_item, "<Enter>", show_tooltip)
            canvas.tag_bind(text_item, "<Leave>", hide_tooltip)
            
    def set_display_box(self,display_box):
        self.display_box=display_box




#canvas
def on_canvas_click(event,canvas):
    # Get the rectangle item that was clicked on
    item = canvas.find_closest(event.x, event.y)[0]

    #search

    # Store the item ID and the starting coordinates for moving
    canvas.itemconfig(item, tags=("selected",))
    canvas.tag_bind("selected", "<B1-Motion>", on_canvas_drag)
    canvas.tag_bind("selected", "<ButtonRelease-1>", on_canvas_release)
    canvas.tag_bind("selected", "<Leave>", on_canvas_leave)
    canvas.start_x = event.x
    canvas.start_y = event.y

def on_canvas_drag(event,canvas):
    # Calculate the distance moved
    dx = event.x - canvas.start_x
    dy = event.y - canvas.start_y
    # Move the selected rectangle
    canvas.move("selected", dx, dy)
    # Update the starting coordinates for the next drag event
    canvas.start_x = event.x
    canvas.start_y = event.y

def on_canvas_release(event,canvas):
    # Reset the selected tag and clear the starting coordinates
    canvas.dtag("selected", "selected")
    canvas.start_x = None
    canvas.start_y = None

def on_canvas_leave(event,canvas):
    # Reset the selected tag and clear the starting coordinates
    canvas.dtag("selected", "selected")
    canvas.start_x = None
    canvas.start_y = None
# Function to handle mouse wheel event for zooming
def on_mousewheel(event,canvas):
    scale = 1.0
    scale2=1
    if event.delta > 0:
        scale = 1.1
        #print(scale)
    else:
        scale2=-1
        scale = 0.9
        #print(scale)
    
    text_items = canvas.find_withtag("text")
    canvas.scale('all', event.x, event.y, scale, scale)
    
    for item in text_items:
        text = canvas.itemcget(item, "text")
        font_config = canvas.itemconfig(text, "text")

        print(font_config)
        #font_size = int(font_config[-1].split()[1])
        #font_size+=scale2
        #font = ("Helvetica", font_size)
        #canvas.itemconfig(text, font=font)
# Define a variable to keep track of the last mouse position
last_x = None
last_y = None
# Define a function to handle the mouse click and drag events
def onMoveHolding(event,canvas):
    global last_x, last_y
    # Check if this is the first mouse movement
    #search position in the graph
    #graph.isT()

    #else
    if last_x is None:
        last_x = event.x
        last_y = event.y
    # Compute the movement since the last event
    dx = event.x - last_x
    dy = event.y - last_y
    # Move all the canvas items by the same amount
    canvas.move("all", dx, dy)
    # Update the last mouse position
    last_x = event.x
    last_y = event.y
def onDrag(event,canvas):
    global last_x, last_y
    last_x = None
    last_y = None
    canvas.scan_dragto(event.x, event.y, gain=0)
def onClick(event,canvas):
    canvas.scan_mark(event.x, event.y)
