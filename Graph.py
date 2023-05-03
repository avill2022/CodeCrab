import re
import os
def getTypeColor(type):
    if(type == "class"):
        return "yellow"
    if(type == "data class"):
        return "orange"
    if(type == "interface"):
        return "green"
    if(type == "sealed"):
        return "brown"
    if(type == "object"):
        return "red"

class FParameter:
    def __init__(self,declaration, name, type, value, comment):
        self.declaration_type = declaration
        self.parameter_name = name
        self.parameter_type = type
        self.parameter_value = value
        self.parameter_comment = comment
    def show(self):
        a = ""
        b=""
        c=""
        d=""
        if(self.parameter_type):
            b = f": {self.parameter_type}" 
        if(self.parameter_value):
            c = f"= {self.parameter_value}" 
        if(self.parameter_comment):
            d = f"// {self.parameter_comment}" 
        return f"{self.declaration_type} {self.parameter_name} {a}  {b}  {c}"
        


class FFunction:
    def __init__(self,typeF,name,parameters,returns,content):
        self.type=typeF
        self.name = name
        self.parameters = parameters
        self.returns = returns
        self.content = content

    def show(self):   
        if self.parameters and self.returns:
            return("• "+self.type + self.name+"(" + self.parameters+" ) : "+self.returns)
        else:
            if self.parameters:
                return("• "+self.type + self.name+"(" + self.parameters+" ) ")
            else:
                return("• "+self.type + self.name+"() : "+self.returns)

    def draw(self, canvas, x, y, width, height):
        self.rect = canvas.create_rectangle(x, y, x + width, y + height, fill='white', outline='black')
        canvas.create_text(x + width/2, y + height/2, text=self.name)

class FClass:
    def __init__(self,typeF,name,constructor_parameters,extends,content):
        self.type=typeF
        self.name = name
        self.content=content #analyzable content
        self.color = getTypeColor(typeF)
        self.constructor_parameters = constructor_parameters
        self.FFunctions=[]
        self.FParameters=[]
        self.FClasses=[] #
        self.extends = extends
        self.radius=50
        self.x=25
        self.y=25

    def scanningParameters(self):
        if self.constructor_parameters:
            for s in self.constructor_parameters.split(','):
                match = s.split()
                p1=""
                p2=""
                p3=""
                p4=""
                p5=""
                p1 = match[0] if match[0] else ""
                p2 = match[1] if match[1] else ""
                if len(match)>2:
                    p3 = match[2] if match[2] else ""
                if len(match)>3:
                    p4 = match[3] if match[3] else ""
                if len(match)>4:
                    p5 = match[4] if match[4] else ""
                self.FParameters.append(FParameter(p1,p2.replace(':',''),p3.replace(':',''),p4,p5))
                
    def show(self):
        if self.constructor_parameters and self.extends:
            return(self.type+" " + self.name+" (" + self.constructor_parameters+")"+" : " + self.extends)
        else:
            if self.constructor_parameters:
                return(self.type+" " + self.name+" (" + self.constructor_parameters+")")
            else:
                return(self.type+" " + self.name+" : " + self.extends)

    def draw(self, canvas, x, y, width, height):
        self.rect = canvas.create_rectangle(x, y, x + width, y + height, fill='white', outline='black')
        canvas.create_text(x + width/2, y + height/2, text=self.name)

class FileNode:
    def __init__(self, name):
        self.name = name
        self.content = None
        self.FClasses = []
        self.FObjects = []
        self.FFunctions = []
        self.color='gray'
        self.neighbors=[]
        self.rect = None  # Rectangle object on the canvas
    
    def compareClassesConstructor(self,name):
        for a in self.FClasses:
            print("classes parameters"+name + " = " + a.constructor_parameters)
            # Search for matches using the function pattern
            function_matches1 = re.findall(r'\s*:\s{}*'.format(name), a.constructor_parameters)
            function_matches2 = re.findall(r'\s*{}\s+'.format(name), a.constructor_parameters)
            if function_matches1 or function_matches2:
                return True
            
            #if(a.constructor_parameters.find(name)!=-1):
            #    return True
    def compareClassesExtends(self,name):
        for a in self.FClasses:
            print("classes extend "+name + " = " + a.extends)
            if(a.extends.find(name)!=-1):
                return True
            
    def compareObjects(self,name):
        for a in self.FileObjects:
            print(name + " = " + a.extends)
            if(a.find(name)!=-1):
                return True
    def compareFunctions(self,name):
        for a in self.FFunctions:
            if(a.find(name)!=-1):
                return True
            
    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def remove_neighbor(self, neighbor):
        if neighbor in self.neighbors:
            self.neighbors.remove(neighbor)

    def get_neighbors(self):
        return self.neighbors
    
    def show(self):
        for a in self.FClasses:
            a.show()
        for a in self.FileObjects:
            a.show()
        for a in self.FFunctions:
            a.show()

    def __str__(self):
        return self.name

class Relation:
    def __init__(self, file1, file2, weight):
        self.file1 = file1
        self.file2 = file2
        self.weight = weight

    def __str__(self):
        return f"{self.file1} -- {self.weight} --> {self.file2}"
    
class Project:
    def __init__(self):
        self.nodes = []
        self.relations = []
        self.type=0

    def clear(self):
        self.nodes.clear()
        self.relations.clear()

    def add_file(self, file,tag):
        if file not in self.nodes:
            for n in self.nodes:
                if(file.compareClassesConstructor(os.path.splitext(n.name)[0])):
                    self.add_relation(file, n, 1)
                    ##
                    ##
            self.nodes.append(file)

    def remove_file(self, file):
        if file in self.nodes:
            self.nodes.remove(file)
            # Remove any relations involving the removed file
            self.relations = [r for r in self.relations if r.file1 != file and r.file2 != file]

    def add_relation(self, file1, file2, weight):
        #file1.relations+=1
        relation = Relation(file1, file2, weight)
        self.relations.append(relation)
        file1.add_neighbor(file2)
        file2.add_neighbor(file1)

    def remove_relation(self, relation):
        if relation in self.relations:
            self.relations.remove(relation)
            relation.file1.remove_neighbor(relation.file2)
            relation.file2.remove_neighbor(relation.file1)

    def get_nodes(self):
        return self.nodes

    def get_relations(self):
        return self.relations
    

    def __str__(self):
        nodes_str = ', '.join(str(file) for file in self.nodes)
        relations_str = '\n'.join(str(relation) for relation in self.relations)
        return f"nodes: {nodes_str}\nRelations:\n{relations_str}"
        

def exampleproject():
    # Example usage:

    # Create nodes
    file1 = FileNode("A")
    file2 = FileNode("B")
    file3 = FileNode("C")
    file5 = FileNode("A")
    file4 = FileNode("C")

    # Create project
    project = project()

    # Add nodes to project
    project.add_file(file1)
    project.add_file(file2)
    project.add_file(file3)
    project.add_file(file4)
    project.add_file(file5)


    # Add relations to project
    project.add_relation(file1, file2, 5)
    project.add_relation(file2, file4, 5)
    project.add_relation(file1, file5, 5)
    project.add_relation(file5, file2, 5)
    project.add_relation(file2, file3, 3)

    # Print project
    #print(project)

    # Output:
    # nodes: A, B, C
    # Relations:
    # A -- 5 --> B
    # B -- 3 --> C

    # Remove a file and its relations from the project
    #project.remove_file(file2)

    # Print project after file removal
    #print(project)

    # Output:
    # nodes: A, C
    # Relations:
    return project

#exampleproject()
