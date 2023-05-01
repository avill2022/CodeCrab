import tkinter
from tkinter.font import Font
import re

class Layout(tkinter.Frame):
    def __init__(self, root):
        tkinter.Frame.__init__(self, root)
        self.root = root
        self.selected=None
        self.graph = None
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
        #self.canvas.bind("<ButtonPress-1>", self.move_start)
        #self.canvas.bind("<B1-Motion>", self.move_move)
        
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
        self.toolTrip(self.root,x,y,text,text_item,tag)
        return text_item

    def find_word_positions(self,text,textbox,pattern,color):
        lines = text.split("\n")
        for i, line in enumerate(lines):

            matches = re.finditer(pattern, line)
            for match in matches:
                start = match.start()
                end = match.end()
                textbox.tag_add(f"{start}.{end}", f"{i+1}.{start}", f"{i+1}.{end}")
                textbox.tag_config(f"{start}.{end}", foreground=color)

    def setTextLayout(self,display_box,content):
        if display_box and content:
            display_box.delete("0.0", tkinter.END)
            display_box.insert("0.0",content) 
            self.find_word_positions(content,display_box,r'\b\s*object\s*\b',"orange")
            self.find_word_positions(content,display_box,r'\b\s*fun\s*\b',"orange")
            self.find_word_positions(content,display_box,r'\b\s*class\s*\b',"red")
            self.find_word_positions(content,display_box,r'\b\s*override\s*\b',"blue")

    #move
    def move_start(self, event):
        self.canvas.itemconfig(event, fill='red')
        clicked_item = event.widget.find_closest(event.x, event.y)[0]
        tags = event.widget.gettags(clicked_item)
        if len(tags)>2:
            self.selected = tags[1]
        #print(f".....................................")
        #print(f"Tag of clicked text: {tags}")
        #print(f"Tag : {self.selected}")
        self.canvas.selected_item = clicked_item
        # Save the x and y coordinates of the mouse click
        self.canvas.drag_start_x = event.x
        self.canvas.drag_start_y = event.y
        # self.display_box.delete(1.0, tkinter.END)
        if self.graph:
                for file in self.graph.get_nodes():
                    if file.name == self.selected:
                        self.setTextLayout(self.display_box,file.content) 
                        break
                    for fc  in file.FileClasses:
                        if fc.name == self.selected:
                            self.setTextLayout(self.display_box,fc.show()+fc.content)   
                            break  
                        for ff  in fc.FFunctions:
                            if ff.name == self.selected:
                                self.setTextLayout(self.display_box,ff.show()+ff.content)   
                                break 
                        #print(file.name) 
    def move_move(self, event):
        dx = event.x - self.canvas.drag_start_x
        dy = event.y - self.canvas.drag_start_y
        #text = self.canvas.itemcget(self.canvas.selected_item, "text")
        if self.selected:
            for item in self.canvas.find_withtag(self.selected):
                self.canvas.move(item, dx, dy)
        self.canvas.drag_start_x = event.x
        self.canvas.drag_start_y = event.y
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

    def toolTrip(self,root,x,y,text,text_item,tag):
        x0, y0, x1, y1 = self.canvas.bbox(tag)
        text_width = x1 - x0
        # shorten text if width is more than 30 pixels
        if text_width > 30:
            text1 = text[:12] + "..." #+ text[-1:]
            # create a text item with the truncated text
            # change text of the text object
            self.canvas.itemconfig(text_item, text=text1)
            # create a tooltip that displays the full text when the mouse is hovered over the item
            tooltip = tkinter.Label(root, text=text, wraplength=300, justify="left")
            def show_tooltip(event):
                tooltip.place(x=event.x, y=event.y)
            def hide_tooltip(event):
                tooltip.place_forget()

            self.canvas.tag_bind(text_item, "<Button-1>", self.move_start)
            self.canvas.tag_bind(text_item, "<B1-Motion>", self.move_move)
            self.canvas.tag_bind(text_item, "<Enter>", show_tooltip)
            self.canvas.tag_bind(text_item, "<Leave>", hide_tooltip)

    def set_display_box(self,display_box):
        self.display_box=display_box
    def set_graph(self,graph):
        self.graph=graph   
    
    def draw_project(self):
        # Clear the canvas
        self.canvas.delete("all")
        if self.graph:
            # Define parameters for file layout
            canvas_width = 300
            canvas_height = 300
            file_radius = 20
            file_spacing = 100
            arrow_size = 40
            
            # Determine the number of nodes and their connections
            num_nodes = len(self.graph.get_nodes())
            file_connections = {file: len(file.get_neighbors()) for file in self.graph.get_nodes()}
            
            # Determine the total width and height required for the layout
            total_width = max(file_connections.values()) * file_spacing
            total_height = num_nodes * file_spacing
            
            # Calculate the starting position for the layout
            start_x = (canvas_width - total_width) / 2
            start_y = (canvas_height - total_height) / 2

            font_size=10
            x = 50
            y=50
            # Draw nodes as circles
            for file in self.graph.get_nodes():
                # Calculate the position of the file on the canvas
                x = start_x + file_connections[file] * file_spacing
                y = start_y + self.graph.get_nodes().index(file) * file_spacing
                # Update the file's position self.graph.get_nodes()
                file.x = x
                file.y = y
                background = None
                if(self.graph.type==0):#type of file
                    background = self.canvas.create_rectangle(x, 
                                            y, 
                                            x+100, 
                                            y+15*len(file.FClasses)
                                            +15*len(file.FObjects)
                                            +15*len(file.FFunctions),
                                    fill=file.color, outline='black')#,stipple= "gray50"
                #title file
                back_titleFile = self.canvas.create_rectangle(x+5, 
                                            y-10, 
                                            x+80, 
                                            y+10,
                                    fill="white", outline='black')#,stipple= "gray50"  

                titleFile=self.add_text(x+10,y-5, text=file.name,tag=file.name)
                
                self.canvas.addtag_withtag(file.name, background)
                self.canvas.addtag_withtag(file.name, titleFile)
                self.canvas.addtag_withtag(file.name, back_titleFile)
                
                #self.canvas.tag_bind(t, "<Button-1>", lambda event: show_message_box(file.name))
                #class files
                iterator=0
                for fc  in file.FileClasses:
                    self.canvas.addtag_withtag(file.name,
                                        self.canvas.create_rectangle(x+5, 
                                        y+13+15*iterator, 
                                        x+105, 
                                        y+13+15+15*iterator,
                                        fill=fc.color, 
                                        outline='black')
                                    )
                    self.canvas.addtag_withtag(
                                        file.name,self.add_text(x+7, 
                                        y+13+15*iterator, 
                                        text=fc.show(),
                                        tag=fc.name)
                                    )
                    iterator+=1
                    #print the functions
                    for ff in fc.FFunctions:
                        self.canvas.addtag_withtag(file.name,self.canvas.create_rectangle(x+5, 
                                        y+13+15*iterator, 
                                        x+105, 
                                        y+13+15+15*iterator,
                                fill="red", outline='black'))
                        self.canvas.addtag_withtag(file.name,self.add_text(x+7, 
                                        y+13+15*iterator, text=ff.show(),tag=ff.name))
                        iterator+=1
                    #print the objects
                
                '''
                
                for fc  in file.FileFunctions:
                    self.canvas.addtag_withtag(file.name,self.canvas.create_rectangle(x+5, 
                                        y+13+15*iterator, 
                                        x+105, 
                                        y+13+15+15*iterator,
                                fill="red", outline='black'))
                    self.canvas.addtag_withtag(file.name,self.add_text(x+7, 
                                        y+13+15*iterator, text=fc.show(),tag=fc.name))
                    iterator+=1'''
            # Draw relations as lines
            for relation in self.graph.get_relations():
                file1 = relation.file1
                file2 = relation.file2
                self.canvas.create_line(file1.x, file1.y, file2.x, file2.y, arrow=tkinter.LAST)
                # Draw the arrowhead
                #canvas.create_polygon(file2.x, file2.y, file2.x - arrow_size, file2.y - arrow_size, file2.x - arrow_size, file2.y + arrow_size, fill="black")
                #self.drawArrow(canvas,10,file1.x, file1.y, file2.x, file2.y)
                #canvas.create_line(file1.x, file1.y, file2.x, file2.y)
                # Draw nodes as circles