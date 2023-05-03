import re
import Graph as gr


def capture_parentheses(text):
    #if a parenthesis is found, capture it
    level=0
    capture = ""
    for i in range(0, len(text)):
        if text[i] == '{':
            level += 1
        elif text[i] == '}':
            level -= 1

        if(level and level>0):
            capture += text[i]
            
        if level == 0 and capture!="":
            # Found the closing parenthesis, return the captured text
            return capture+"\n}"
    return "}"

def createFunctionKotlin(fun_name,fun_parameters,returns,kotlin_code):
    function_pattern = r'\bfun\s+{}([\s\S]*)'.format(fun_name)
    match = re.search(function_pattern, kotlin_code)
    if match:
        content = match.group(1)
        content = capture_parentheses(content)                                                     
        if content:
            return gr.FFunction("fun ",fun_name,fun_parameters,returns,content)

def getFunctionsKotlin(kotlin_code):
    FFunctions = []
    #function parameters return
    function_pattern = r'\bfun\s+(\w+)\s*\((.*?)\)\s*:\s*(\w+)?\s*\{'
    function_matches = re.findall(function_pattern, kotlin_code)
    for match in function_matches:
        a =createFunctionKotlin(match[0],match[1],match[2],kotlin_code)
        if a:
            FFunctions.append(a)

    #function parameters 
    function_pattern = r'\bfun\s+(\w+)\s*\((.*?)\)\s*\{'
    function_matches = re.findall(function_pattern, kotlin_code)
    for match in function_matches:
        a =createFunctionKotlin(match[0],match[1],"",kotlin_code)
        if a:
            FFunctions.append(a)

    #function return
    function_pattern = r'\bfun\s+(\w+)\s*\(\)\s*:\s*(\w+)?\s*\{'
    function_matches = re.findall(function_pattern, kotlin_code)
    for match in function_matches:
        a =createFunctionKotlin(match[0],"()",match[1],kotlin_code)
        if a:
            FFunctions.append(a)
    #function
    function_pattern = r'\bfun\s+(\w+)\s*\(\)\s*\{'
    function_matches = re.findall(function_pattern, kotlin_code)
    for match in function_matches:
        a =createFunctionKotlin(match[0],"()","",kotlin_code)
        if a:
            FFunctions.append(a)
    return FFunctions


    class_pattern = r'\binterface\b\s+(\w+)\s*\{'
    class_matches = re.findall(class_pattern, kotlin_code)
    for match in class_matches:
        FileObjects.append(gr.FileClass("interface",match,"",""))

    '''pattern = r'data\s+class\s+(\w+)\s*\(([^)]*)\)\s*(?:\:(.*?)\s*{)?'
    # Find Kotlin data class declarations
    matches = re.findall(pattern, kotlin_code)
    # Extract class name, parameters, and extension from matches
    for match in matches:
        FileObjects.append(gr.FileClass("data class",match[0],match[1],match[2]))'''
    return FileObjects

def createClassKotlin(name,class_name,constructor_parameters,extends,kotlin_code):
    function_pattern = r'\b'+name+' '+class_name+'([\s\S]*)'

    match = re.search(function_pattern, kotlin_code)
    if match:
        content = match.group(1)
        content = capture_parentheses(content)
        if content:
            return gr.FClass(name,class_name,constructor_parameters,extends,content)

def getClassesKotlin(name,kotlin_code):
    FileClasses = []
    #class parameters extend
    class_pattern = r'\b'+name+'\s+(\w+)\s*\((.*?)\)\s*(?:\:(.*?))?\s*\{'
    class_matches = re.findall(class_pattern, kotlin_code)
    for match in class_matches:
        class_name = match[0]
        constructor_parameters = match[1]
        extends = match[2]
        fileClass = createClassKotlin(name,class_name,constructor_parameters,extends,kotlin_code)
        if fileClass:
            fileClass.FFunctions = getFunctionsKotlin(kotlin_code=fileClass.content)
            fileClass.FParameters = getParametersKotlin(kotlin_code=fileClass.content)
            ##fileClass.FClasses=getClassesKotlin("class",kotlin_code=fileClass.content)
            fileClass.scanningParameters()
            FileClasses.append(fileClass)

    #class parameters
    class_pattern = r'\b'+name+'\s+(\w+)\s*\((.*?)\)\s*\{'
    class_matches = re.findall(class_pattern, kotlin_code)
    for match in class_matches:
        class_name = match[0]
        constructor_parameters = match[1]
        fileClass = createClassKotlin(class_name,constructor_parameters,"",kotlin_code)
        if fileClass:
            fileClass.FFunctions = getFunctionsKotlin(kotlin_code=fileClass.content)
            fileClass.FParameters = getParametersKotlin(kotlin_code=fileClass.content)
           ## fileClass.FClasses=getClassesKotlin("class",kotlin_code=fileClass.content)
            fileClass.scanningParameters()
            FileClasses.append(fileClass)
    #class extend
    class_pattern = r'\b'+name+'\s+(\w+)\s*:\s*(.*?)\s*\{'
    class_matches = re.findall(class_pattern, kotlin_code)
    for match in class_matches:
        class_name = match[0]
        extends = match[1]
        fileClass = createClassKotlin(name,class_name,"",extends,kotlin_code)
        if fileClass:
            fileClass.FFunctions = getFunctionsKotlin(kotlin_code=fileClass.content)
            fileClass.FParameters = getParametersKotlin(kotlin_code=fileClass.content)
           ## fileClass.FClasses=getClassesKotlin("class",kotlin_code=fileClass.content)
            fileClass.scanningParameters()
            FileClasses.append(fileClass)

    #class ()
    class_pattern = r'\b'+name+'\s+(\w+)\s*\(\)\s*\{'
    class_matches = re.findall(class_pattern, kotlin_code)
    for match in class_matches:
        class_name = match
        fileClass = createClassKotlin(name,class_name,"()","",kotlin_code)
        if fileClass:
            fileClass.FFunctions = getFunctionsKotlin(kotlin_code=fileClass.content)
            fileClass.FParameters = getParametersKotlin(kotlin_code=fileClass.content)
           ## fileClass.FClasses=getClassesKotlin("class",kotlin_code=fileClass.content)
            fileClass.scanningParameters()
            FileClasses.append(fileClass)

    #class
    class_pattern = r'\b'+name+'\s+(\w+)\s*\{'
    class_matches = re.findall(class_pattern, kotlin_code)
    for match in class_matches:
        class_name = match
        fileClass = createClassKotlin(name,class_name,"","",kotlin_code)
        if fileClass:
            fileClass.FFunctions = getFunctionsKotlin(kotlin_code=fileClass.content)
            fileClass.FParameters = getParametersKotlin(kotlin_code=fileClass.content)
           ## fileClass.FClasses=getClassesKotlin("class",kotlin_code=fileClass.content)
            fileClass.scanningParameters()
            FileClasses.append(fileClass)
            #for f in fileClass.FFunctions:
                #print(f.show())

    return FileClasses

def getParametersKotlin(kotlin_code):
    FileParameters = []
    #pattern = r'var\s+.*$'
    pattern = r'(val|var)\s+(\w+)\s*:\s*(\w+)\s*=\s*([^/\n]+)\s*(//\s*(.*))?'
    matches = re.findall(pattern, kotlin_code)
    #match = re.search(pattern, kotlin_code)
    for match in matches:
        declaration_type = match[0]
        parameter_name = match[1]
        parameter_type = match[2]
        parameter_value = match[3]
        parameter_comment = match[5] if match[5] else ""
        fileParameter =  gr.FParameter(declaration_type,parameter_name,parameter_type,parameter_value,parameter_comment)
        FileParameters.append(fileParameter)
        '''function_pattern = r'\b(val)\s+{}([\s\S]*)'.format(parameter_name)
        match = re.search(function_pattern, kotlin_code)
        if match:
            content = match.group(1)
            print(content)'''
    return FileParameters
    #var count
    #val name: String = "John Doe"
    #val name: Int = 8 //asdfasfsadfd
    #var count: String
    #var count = 0
#main function#
def kotlinRegularExpressions(file_contents,file_name):
    file_node = gr.FileNode(file_name)
    file_node.content = file_contents
    file_node.FClasses=getClassesKotlin("class",kotlin_code=file_contents)
    file_node.FObjects=getClassesKotlin("object",kotlin_code=file_contents)
    file_node.FInterfaces=getClassesKotlin("interface",kotlin_code=file_contents)
    #file_node.FileObjects=getObjects(kotlin_code=file_contents)
    return file_node









def getObjects(kotlin_code):
    FileObjects = []
    class_pattern = r'\bobject\b\s+(\w+)\s*\{'
    class_matches = re.findall(class_pattern, kotlin_code)
    for match in class_matches:
        FileObjects.append(gr.FClass("object",match,"",""))
        #print("Object name: " + class_name)
