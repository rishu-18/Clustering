from util import kmeans,create_cluster_image,init,create_cluster_image,clear_mem
import random
import math
from PIL import Image,ImageDraw,ImageFont
from extract_original import gene
from Gene_vs_DataPoints import Corresponding_Gene






def main():
	
	#INITIALIZATION

	k=int(raw_input("Enter the no of Clusters:"))
	num_dimension_diseased=int(raw_input("Enter the no of dimensions in DISEASED DATASET:"))
	diseased = init("./diseased.txt",k)	
	cluster_centre=random.sample(range(0,len(diseased)),k)
	cluster_diseased=kmeans(cluster_centre,k,num_dimension_diseased,diseased)
	del diseased[:]
	clear_mem()
	num_dimension_normal=int(raw_input("Enter the no of dimensions in NORMAL DATASET:"))
	normal = init("./normal.txt",k)	
	cluster_centre=random.sample(range(0,len(normal)),k)
	cluster_normal=kmeans(cluster_centre,k,num_dimension_normal,normal)
	cluster_diseased_vs_normal={}
	for i in cluster_diseased.iterkeys():
		highest_match=0
		data_points_diseased=cluster_diseased[i]
		for j in cluster_normal.iterkeys():
			x=len(set(data_points_diseased) & set(cluster_normal[j]))
			if x>highest_match:
				highest_match=x
				Corresponding_cluster=j
		cluster_diseased_vs_normal[i]=cluster_normal[Corresponding_cluster]
		del cluster_normal[Corresponding_cluster]
	# show image
	im_diseased=create_cluster_image(cluster_diseased)
	im_normal=create_cluster_image(cluster_diseased_vs_normal)
	draw = ImageDraw.Draw(im_diseased)
	font = ImageFont.truetype("fonts/OpenSans-Bold.ttf",35)
	draw.text((580,660),"For DISEASED",(0,0,255),font=font)
	draw = ImageDraw.Draw(im_normal)
	font = ImageFont.truetype("fonts/OpenSans-Bold.ttf",35)
	draw.text((580,660),"For NORMAL",(0,0,255),font=font)
	im_diseased.show()
	im_normal.show() 
	im_diseased.save("KMEANS_DISEASED.png")
	im_normal.save("KMEANS_NORMAL.png") 
	#check true positive
	responsible=[]
	for i in range(0,k):
		x=set(cluster_diseased_vs_normal[i])-set(cluster_diseased[i])
		responsible.extend(x)
	print "No of Genes responsible for diseased:",len(responsible)
	responsible_gene_name=[]
	for i in responsible:
		responsible_gene_name.append(Corresponding_Gene[i])
	true_positive=list(set(responsible_gene_name) & set(gene))
	print len(true_positive)
	x=(float(len(true_positive))/float(len(responsible_gene_name)))*100.0
	print x




	

if __name__ == '__main__':
	main()