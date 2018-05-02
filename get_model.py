#!/usr/bin/python
#usage: get_model [filename.ply]
#example: get_model cup.ply 

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str)
args = parser.parse_args()
with open(args.filename,"r") as file:
	lines=file.readlines()
	
	vertex_len=-1
	face_len=-1
	line_index=-1
	vertex_norm_start_index=0
	
	model_vertex=list()
	model_norm=list()
	model_index=list()
	
	flag_vertex_norm=0
	flag_model_index=0
	for line in lines:
		line_index=line_index+1
		row=line.split()
		#print row
		if line_index==3:
			vertex_len=int(row[2])
		if line_index==10:
			face_len=int(row[2])
		if row[0]=="end_header":
			flag_vertex_norm=1
			vertex_norm_start_index=line_index+1
			continue
		if line_index==vertex_norm_start_index+vertex_len:
			flag_vertex_norm=0
			flag_model_index=1
		if flag_vertex_norm:
			model_vertex.append(float(row[0]))
			model_vertex.append(float(row[1]))
			model_vertex.append(float(row[2]))
			model_norm.append(float(row[3]))
			model_norm.append(float(row[4]))
			model_norm.append(float(row[5]))
		if flag_model_index:
			model_index.append(int(row[1]))
			model_index.append(int(row[2]))
			model_index.append(int(row[3]))
	
	#write to .h file
	modelname=args.filename.split(".")[0]
	chead=open(modelname+".h","w")
	chead.write("//\n")
	chead.write("// Each group of three values specifies a torus vertex\n")
	chead.write("//\n")
	
	#vertices
	chead.write("float "+modelname+"Vertices[] = {\n")
	for i in range(0,vertex_len):
		index=i*3
		chead.write(",".join([str(model_vertex[index]),
			str(model_vertex[index+1]),
			str(model_vertex[index+2])]))
		if i==vertex_len-1:
			chead.write("\n")
		else:
			chead.write(",\n")
	chead.write("};\n")
	chead.write("int "+modelname+"VerticesLength = sizeof("+modelname+"Vertices)/sizeof(float);\n")
		
	#norm
	chead.write("float "+modelname+"Normals[] = {\n")
	for i in range(0,vertex_len):
		index=i*3
		chead.write(",".join([str(model_norm[index]),
			str(model_norm[index+1]),
			str(model_norm[index+2])]))
		if i==vertex_len-1:
			chead.write("\n")
		else:
			chead.write(",\n")
	chead.write("};\n")
	chead.write("int "+modelname+"NormalsLength = sizeof("+modelname+"Normals)/sizeof(float);\n")
	
	#elements
	chead.write("int "+modelname+"Elements[] = {\n")
	for i in range(0,face_len):
		index=i*3
		chead.write(",".join([str(model_index[index]),
			str(model_index[index+1]),
			str(model_index[index+2])]))
		if i==vertex_len-1:
			chead.write("\n")
		else:
			chead.write(",\n")
	chead.write("};\n")
	chead.write("int "+modelname+"ElementsLength = sizeof("+modelname+"Elements)/sizeof(int);\n")
	
	#normalIndices
	chead.write("int "+modelname+"NormalIndices[] = {\n")
	for i in range(0,face_len):
		index=i*3
		chead.write(",".join([str(model_index[index]),
			str(model_index[index+1]),
			str(model_index[index+2])]))
		if i==vertex_len-1:
			chead.write("\n")
		else:
			chead.write(",\n")
	chead.write("};\n")
	chead.write("int "+modelname+"NormalIndicesLength = sizeof("+modelname+"NormalIndices)/sizeof(int);\n")
