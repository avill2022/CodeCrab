import re
import Graph as gr

# Sample Java code
""" java_code =

"""

def getFunctionsJava(java_code):
    onFileFunctions = []
    ######## functions with out parameters and whit out return type
    function_pattern = r'(?:public|private)?\s+(?:static\s+)?\w+\s+(\w+)\s*\((.*?)\)\s*\{'
    # Search for matches using the function pattern
    function_matches = re.findall(function_pattern, java_code)
    # Extract and print function names and parameter lists
    for match in function_matches:
        function_name = match[0]
        parameter_list = match[1]
        if parameter_list:
            onFileFunctions.append(gr.FileFunction("public void ",function_name,parameter_list,""))
        else:
            onFileFunctions.append(gr.FileFunction("public void ",function_name,"",""))
    return onFileFunctions
    #FUNCTIONS PARAMETERS AND RETURN TYPE
    '''function_pattern = r'fun\s+(\w+)\s*\((.*?)\)\s*:\s*(\w+)?\s*\{'
    function_matches = re.findall(function_pattern, java_code)
    for match in function_matches:
        onFileFunctions.append(gr.FileFunction("fun",match[0],match[1],match[2]))
    return onFileFunctions'''

def getVariables(java_code):
    
    parameter_pattern = r'(?:final\s+)?(\w+)\s+(\w+)\s*=\s*(.*?);'
    # Search for matches using the parameter pattern
    parameter_matches = re.findall(parameter_pattern, java_code)
    onFileParameters = []
    # Extract and print value type, value name, and value initialization
    for match in parameter_matches:
        value_type = match[0]
        value_name = match[1]
        value_initialization = match[2]
        #print("-    Parameter: "+ value_type + " " + value_name + " - initialization:" + value_initialization)
'''
def getObjects(java_code):
    onFileObjects = []
    class_pattern = r'\bobject\b\s+(\w+)\s*\{'
    class_matches = re.findall(class_pattern, java_code)
    for match in class_matches:
        onFileObjects.append(gr.FileClass("object",match,"",""))
        #print("Object name: " + class_name)

    class_pattern = r'\binterface\b\s+(\w+)\s*\{'
    class_matches = re.findall(class_pattern, java_code)
    for match in class_matches:
        onFileObjects.append(gr.FileClass("interface",match,"",""))

    pattern = r'data\s+class\s+(\w+)\s*\(([^)]*)\)\s*(?:\:(.*?)\s*{)?'
    # Find Java data class declarations
    matches = re.findall(pattern, java_code)
    # Extract class name, parameters, and extension from matches
    for match in matches:
        onFileObjects.append(gr.FileClass("data class",match[0],match[1],match[2]))
    return onFileObjects'''

def getClassName(java_code):
    onFileClasses = []
    class_pattern = r'class\s+(\w+)\s*(?:extends\s+(\w+))?\s*\{'
    class_matches = re.findall(class_pattern, java_code)
    #class without parameters
    for match in class_matches:
        class_name = match[0]
        extended_class_name = match[1]
        if extended_class_name:
            onFileClasses.append(gr.FileClass("class",class_name + "()","",extended_class_name))
            #print("Class: " + class_name+ " - Extended class: " + extended_class_name)
        else:
            onFileClasses.append(gr.FileClass("class",class_name + "()","",""))
            #print("Class: " + class_name + "()")

    #class AAAAAAAAAAAAAAAAA {
    '''class_pattern = r'\bclass\b\s+(\w+)\s*\{'
    class_matches = re.findall(class_pattern, java_code)
    for match in class_matches:
        class_name = match
        onFileClasses.append(gr.FileClass("class",class_name,"",""))'''
    #class without parameters but ()
    #class BBBBBBBBBBBBBBBB(){
    '''class_pattern = r'\bclass\b\s+(\w+)\s*\(\)\s*\{'
    class_matches = re.findall(class_pattern, java_code)
    for match in class_matches:
        class_name = match
        onFileClasses.append(gr.FileClass("class",class_name +"()","",""))'''

    #class without parameters extend
    #class Person1 : Person2(name, age) { 
    '''class_pattern = r'\bclass\b\s+(\w+)\s*:(.*?)\s*\{'
    class_matches = re.findall(class_pattern, java_code)
    for match in class_matches:
        class_name = match[0]
        extends = match[1]
        onFileClasses.append(gr.FileClass("class",class_name,"",extends))'''
    #class with parameters and extend (?:\:(.*?))?
    '''class_pattern = r'class\s+(\w+)\s*\((.*?)\)\s*(?:\:(.*?))?\s*\{'
    class_matches = re.findall(class_pattern, java_code)
    for match in class_matches:
        class_name = match[0]
        constructor_parameters = match[1]
        extends = match[2]
        onFileClasses.append(gr.FileClass("class",class_name,constructor_parameters,extends))'''
    return onFileClasses

def javaRegularExpressions(file_contents,file_name):
    file_node = gr.FileNode(file_name)
    #file_node.onFileObjects = getObjects(java_code=file_contents)
    file_node.FileFunctions = getFunctionsJava(java_code=file_contents)
    file_node.FileClasses = getClassName(java_code=file_contents)
    file_node.show()
    return file_node
