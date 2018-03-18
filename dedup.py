# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 19:37:57 2018

@author: somi prakash
"""
import math
import numpy as np
import pandas as pd     
import Levenshtein

# Global parameters
weights = [1,1,2,2]
weights = [y/(np.sum(weights)) for y in weights]   # Normalizing the weights in range (0,1)
net_threshold  = 0.7
linkage_list = ['single','average','complete']
linkage = linkage_list[2]


def similarity(s,t):
    l_max = max(len(s),len(t))
    return round(1- float(Levenshtein.distance(s, t)/float(l_max)),2)

def record_pair_similarity(list1,list2):
    record_pair_list = []
    sim_vector = []
    pair_dict = {'pair':'','sim_vec':'','net_sim':''}
    for rowA in list1:
        for rowB in list2:   
                pair_dict['pair'] = [rowA['rec_no'] , rowB['rec_no']]  # making pair as [1,2]
                sim_vector.append(similarity(rowA['first_name'],rowB['first_name']))
                sim_vector.append(similarity(rowA['last_name'],rowB['last_name']))
                sim_vector.append(similarity(rowA['dob'],rowB['dob']))
                sim_vector.append(similarity(rowA['gender'],rowB['gender']))          
                pair_dict['sim_vec'] = sim_vector
                sim_vector = []
                record_pair_list.append(pair_dict)
                pair_dict = {'pair' : '','sim_vec' : ''}
    return record_pair_list    # returns pair list

def get_weighed_similarity(pair_list):
    net_sim = 0
    for i in range(len(pair_list)):
         net_sim = weights[0]*pair_list[i]['sim_vec'][0] + weights[1]*pair_list[i]['sim_vec'][1] + weights[2]*pair_list[i]['sim_vec'][2] + weights[3]*pair_list[i]['sim_vec'][3]
         pair_list[i]['net_sim'] = round(net_sim,2)
    return  pair_list      # returns pair list with net similarity

                            


def create_sim_matrix(pair_list):
    arr_len = int(math.sqrt(len(pair_list)))
    matrix  = np.zeros(shape=(arr_len,arr_len))
    for count in range(len(pair_list)):
          matrix[pair_list[count]['pair'][0]][pair_list[count]['pair'][1]] = pair_list[count]['net_sim']
    return matrix                    # Returns a 2D array
           
            
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    HIERARCHIAL CLUSTERING FUNCTIONS  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
def cluster_formation(dataset,sim_matrix):    #takes the dataset as input
    clusters = {}
    cluster_list = []
    new_clus = {}
    intermediate_clusters = []
    for i in range(0,len(dataset)):
        clusters['cluster'] = [i]
        cluster_list.append(clusters)
        clusters = {}
    merge = closest_similarity(cluster_list,sim_matrix)     # Cluster list is a list of dict like  >>> {'cluster' : [1]}
    while(merge['sim_val'] > net_threshold):
        new_clus = merge_clusters(cluster_list[merge['pair'][0]],cluster_list[merge['pair'][1]])
        cluster_list.append(new_clus)
        cluster_list.remove(cluster_list[merge['pair'][0]])
        cluster_list.remove(cluster_list[merge['pair'][1]])
        intermediate_clusters.append(new_clus)
        new_clus = {}
        merge = closest_similarity(cluster_list,sim_matrix)
    return cluster_list

       
    
def closest_similarity(cluster_list,sim_matrix):
    most_closest = {}
    c_len = len(cluster_list)
    sim_matrix_new = np.zeros(shape=(c_len,c_len))
    for row in range(c_len):
        for col in range(c_len):
            sim_matrix_new[row][col] = find_cluster_sim(cluster_list[row],cluster_list[row],sim_matrix,linkage)  # Passed of form >>>   {'cluster' : [1]} , {'cluster' : [1,2,6]}
    mx = 0
    el =[]
    for j in range(1,c_len):
        for q in range(j):
            if (sim_matrix_new[j][q] > mx):
                mx=sim_matrix_new[j][q]
                el = [j,q]
    most_closest['pair'] = el
    most_closest['sim_val'] = mx
    return most_closest       # Returns {'pair': [x,y],'sim_val': z}
    
        
def find_cluster_sim(cluster1,cluster2,sim_matrix,linkage):    # Passed of form >>>   {'cluster' : [1]} , {'cluster' : [1,2,6]
    l1 = cluster1['cluster']
    l2 = cluster2['cluster']
    if (linkage == 'average'):
        t_terms = len(l1) + len(l2)
        total =0
        for p in l1:
            for q in l2:
                total += sim_matrix[p][q]
        avg_sim = round(total/float(t_terms),2)
        return avg_sim
    elif (linkage =='complete'):
         min_sim = 2
         for p in l1:
            for q in l2:
                if(sim_matrix[p][q] < min_sim):
                    min_sim = sim_matrix[p][q]
         return min_sim
    elif (linkage == 'single'):
         max_sim = 0
         for p in l1:
            for q in l2:
                if(sim_matrix[p][q] > max_sim ):
                    max_sim = sim_matrix[p][q]
         return max_sim
    
def merge_clusters(clus1,clus2):      # Gets {'cluster' : [x,y,z]} , {'cluster' : [a,b]}
    new_cluster = {}
    new_cluster['cluster'] = clus1['cluster'] + clus2['cluster']
    return new_cluster

def clustered_dataset(dataset,clusters):
    for x,each in enumerate(clusters):
        print('\n Cluster : ' + str(x) + ' members : ')
        for index in each['cluster']:
            print(dataset[index])


if __name__ == "__main__":   
    df = pd.read_csv('dataset.csv')               # Enter he path of the dataset csv file
    dset_a = []
    record_data = {'rec_no' : '','first_name' : '','last_name' : '','dob' : '','gender' : '' }
    for count in range(0,len(df['ln'])):
        record_data['rec_no'] = count
        record_data['first_name'] = df.iloc[count]['fn']
        record_data['last_name'] = df.iloc[count]['ln']
        record_data['dob'] = df.iloc[count]['dob']
        record_data['gender'] = df.iloc[count]['gn']
        dset_a.append(record_data)
        record_data = {'rec_no' : '','first_name' : '','last_name' : '','dob' : '','gender' : '' } 
        
    dset_b = dset_a.copy()             
    paired = record_pair_similarity(dset_a,dset_b)
    w = get_weighed_similarity(paired)  
    sim_mat = create_sim_matrix(w)
    
    # Print formed clusters
    clusters = cluster_formation(dset_a,sim_mat)
    for el in clusters:
        print(el)
        
    clustered_dataset(dset_a,clusters)



        




    
    
    
    
    
