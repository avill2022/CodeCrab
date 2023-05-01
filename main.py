import customtkinter
import tkinter

from tkinter import filedialog
from tkinter import messagebox

import os
#the layout where the graph will be painting
import layout as la
import Graph as g
#functions for regular detection
import kotlin_regular_expressions as kre
import java_regular_expressions as jre

#messagebox.showinfo(""+str(count_files))

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  

build_gradle_project = ""
build_gradle_app = ""
folder_path="C:/Users/alber/Desktop/programation/Python/Projects/testing/folderExample"
to_folder="\\project"
count_files = 0

graph = g.Project()

def changeFile(campo):
    print(campo)
    file=open(campo,'r+')
    l=file.readlines()
    result=[]
    for i in l:
        result.append(i.replace(textFrom.get(),textTo.get()))
    file.close()

    file=open(campo,'w')
    file.truncate(0)
    for a in result:
        file.write(a)
    file.close()

def change_reference():
    global folder_path
    global to_folder
    if(folder_path and textFrom.get() and textTo.get()):
        messagebox.showinfo("Warning","This is a destructive functionality, we recommend you copy or clean the project first!")
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                dire = os.path.join(root, file)
                if file.endswith(".kt") or file.endswith(".java"):
                    #change reference
                    changeFile(os.path.join(root, file))
                    os.rename(os.path.join(root, file), os.path.join(root, file).replace(textFrom.get(),textTo.get()))
        start_loading()
        monitor.draw_project()
    else:
        messagebox.showinfo("There isn't a folder selected!", "Select a android project")
    textFrom.delete(0, tkinter.END)
    textTo.delete(0, tkinter.END)

#0:
def select_folder():
    global folder_path 
    folder_path = filedialog.askdirectory()
    if os.path.exists(folder_path+"/gradle.properties") and os.path.exists(folder_path+"/build.gradle"):
        progressbar_1.size= howManyFiles()
        progressbar_1.set(0.0)
        entry_1.delete(0, tkinter.END)
        entry_1.insert(0, folder_path)
        start_loading()
    else:
        progressbar_1.size= howManyFiles()
        progressbar_1.set(0.0)
        entry_1.delete(0, tkinter.END)
        entry_1.insert(0, folder_path)
        start_loading()
#1:
def howManyFiles():
    global count_files
    count_files = 0
    global folder_path 
    if(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                dire = os.path.join(root, file)
                if file.endswith(".kt") or file.endswith(".java"):
                        count_files +=1
    return count_files
#1: search into the files and save like a graph each file
def start_loading():
    global graph
    graph.clear()
    global count_files
    count = 0.0
    global folder_path
    global to_folder

    if(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                dire = os.path.join(root, file)
                if file.endswith(".kt"):
                    with open(os.path.join(root, file), 'r') as fileContent:
                        base_name = os.path.basename(os.path.join(root, file))
                        graph.add_file(kre.kotlinRegularExpressions(fileContent.read(),base_name),base_name)
                    count+=1
                    progressbar_1.set((count*1)/count_files)
                    app.update()
                    #time.sleep(0.1)
                if file.endswith(".java"):
                    with open(os.path.join(root, file), 'r') as fileContent:
                        base_name = os.path.basename(os.path.join(root, file))
                        graph.add_file(jre.javaRegularExpressions(fileContent.read(),base_name),base_name)
                    count+=1
                    progressbar_1.set((count*1)/count_files)
                    app.update()
    else:
        messagebox.showinfo("There isn't a folder selected!", "Select a android project")

#UI
app = customtkinter.CTk()
app.title("CodeCrab")

slideBar = customtkinter.CTkFrame(app)
slideBar.pack(side="right", padx=10, pady=10)
#open Project
openProject = customtkinter.CTkFrame(slideBar)
openProject.grid(row=0,column=0,pady=5, padx=5, sticky='NSWE')
entry_1 = customtkinter.CTkEntry(master=openProject, placeholder_text="C:/Users/james/Desktop/",width=290)
entry_1.grid(row=1,column=0,pady=5, padx=5, sticky='NSWE')
entry_1.insert(0, "")
entry_1.insert(0, folder_path)
button_1 = customtkinter.CTkButton(master=openProject, text="Select folder", command=select_folder)
button_1.grid(row=2,column=0,pady=5, padx=5, sticky='NSWE')
progressbar_1 = customtkinter.CTkProgressBar(master=openProject)
progressbar_1.grid(row=3,pady=5, padx=5, sticky='NSWE')
progressbar_1.size= howManyFiles()
progressbar_1.set(0.0)
#Change Reference
changeReference = customtkinter.CTkFrame(slideBar)
changeReference.grid(row=1,column=0,pady=5, padx=5)
#elements textFrom ...
lbl = customtkinter.CTkLabel(changeReference, text="change: ")
lbl.grid(column=0, row=0,pady=5, padx=5, sticky='NSWE')
textFrom = customtkinter.CTkEntry(changeReference, placeholder_text="com.something.something",width=230)
textFrom.grid(column=1, row=0,pady=5, padx=5, sticky='NSWE')
#elements textFrom ...
lto = customtkinter.CTkLabel(changeReference, text="to: ")
lto.grid(column=0, row=1,pady=5, padx=5, sticky='NSWE')
textTo = customtkinter.CTkEntry(changeReference, placeholder_text="com.something.something")
textTo.grid(column=1, row=1,pady=5, padx=5, sticky='NSWE')
progressbar_2 = customtkinter.CTkProgressBar(master=changeReference)
progressbar_2.grid(row=2,columnspan=2,pady=5, padx=5, sticky='NSWE')
progressbar_2.size= howManyFiles()
progressbar_2.set(0.0)
btn = customtkinter.CTkButton(changeReference, text="Change reference",command=change_reference)
btn.grid(column=0,columnspan=2,pady=5, padx=5, row=3, sticky='NSWE')
# Text Box
displayBox = customtkinter.CTkTextbox(slideBar, width=300,height=330)
displayBox.grid(row=3,pady=5, padx=5, sticky='NSWE')
# Create a canvas widget
monitor = la.Layout(app)
monitor.pack(expand=tkinter.YES,side="left" ,fill=tkinter.BOTH)

start_loading()

monitor.set_display_box(displayBox)
monitor.set_graph(graph)
monitor.draw_project()

app.mainloop()
