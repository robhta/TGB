from typing import Optional, cast, Union, List, overload, Literal
from tqdm import tqdm
import numpy as np
import pandas as pd
import os.path as osp
import time
import csv
from datetime import datetime
"""
functions for redditcomments
-------------------------------------------
"""
def csv_to_pd_data_rc(
        fname: str,
        ) -> pd.DataFrame:
    r'''
    currently used by redditcomments dataset
    convert the raw .csv data to pandas dataframe and numpy array
    input .csv file format should be: timestamp, node u, node v, attributes
    Args:
        fname: the path to the raw data
    '''
    feat_size = 2 #1 for subreddit, 1 for num words
    num_lines = sum(1 for line in open(fname)) - 1
    print ("number of lines counted", num_lines)
    print ("there are ", num_lines, " lines in the raw data")
    u_list = np.zeros(num_lines)
    i_list = np.zeros(num_lines)
    ts_list = np.zeros(num_lines)
    label_list = np.zeros(num_lines)
    feat_l = np.zeros((num_lines, feat_size))
    idx_list = np.zeros(num_lines)
    w_list = np.zeros(num_lines)
    node_ids = {}

    unique_id = 0
    max_words = 5000 #counted form statistics 


    with open(fname, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        idx = 0
        # ['ts', 'src', 'dst', 'subreddit', 'num_words', 'score']
        for row in tqdm(csv_reader):
            if (idx == 0):
                idx += 1
                continue
            else:
                ts = int(row[0])
                src = row[1]
                dst = row[2]
                num_words = (int(row[3]) / max_words) #int number, normalize to [0,1]
                score = int(row[4]) #int number


                #reindexing node and subreddits
                if (src not in node_ids):
                    node_ids[src] = unique_id
                    unique_id += 1
                if (dst not in node_ids):
                    node_ids[dst] = unique_id
                    unique_id += 1
                w = float(score)
                u = node_ids[src]
                i = node_ids[dst]
                u_list[idx-1] = u
                i_list[idx-1] = i
                ts_list[idx-1] = ts
                idx_list[idx-1] = idx
                w_list[idx-1] = w
                feat_l[idx-1] = np.array([num_words])
                idx += 1
    print ("there are ", len(node_ids), " unique nodes")

    return pd.DataFrame({'u': u_list,
                        'i': i_list,
                        'ts': ts_list,
                        'label': label_list,
                        'idx': idx_list,
                        'w':w_list}), feat_l, node_ids



    






"""
functions for stablecoin
-------------------------------------------
"""
def csv_to_pd_data_sc(
        fname: str,
        ) -> pd.DataFrame:
    r'''
    currently used by stablecoin dataset
    convert the raw .csv data to pandas dataframe and numpy array
    input .csv file format should be: timestamp, node u, node v, attributes
    Parameters:
        fname: the path to the raw data
    Returns:
        df: a pandas dataframe containing the edgelist data
        feat_l: a numpy array containing the node features
        node_ids: a dictionary mapping node id to integer
    '''
    feat_size = 1
    num_lines = sum(1 for line in open(fname)) - 1
    print ("number of lines counted", num_lines)
    u_list = np.zeros(num_lines)
    i_list = np.zeros(num_lines)
    ts_list = np.zeros(num_lines)
    label_list = np.zeros(num_lines)
    feat_l = np.zeros((num_lines, feat_size))
    idx_list = np.zeros(num_lines)
    w_list = np.zeros(num_lines)
    print ("numpy allocated")
    node_ids = {}
    unique_id = 0

    with open(fname, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        idx = 0
        # time,src,dst,weight
        # 1648811421,0x27cbb0e6885ccb1db2dab7c2314131c94795fbef,0x8426a27add8dca73548f012d92c7f8f4bbd42a3e,800.0
        for row in tqdm(csv_reader):
            if (idx == 0):
                idx += 1
                continue
            else:
                ts = int(row[0])
                src = row[1]
                dst = row[2]

                if (src not in node_ids):
                    node_ids[src] = unique_id
                    unique_id += 1
                if (dst not in node_ids):
                    node_ids[dst] = unique_id
                    unique_id += 1

                w = float(row[3])
                if (w == 0):
                    w = 1 

                u = node_ids[src]
                i = node_ids[dst]
                u_list[idx-1] = u
                i_list[idx-1] = i
                ts_list[idx-1] = ts
                idx_list[idx-1] = idx
                w_list[idx-1] = w
                feat_l[idx-1] = np.zeros(feat_size)
                idx += 1

    #! normalize by log 2 for stablecoin
    w_list = np.log2(w_list)

    return pd.DataFrame({'u': u_list,
                        'i': i_list,
                        'ts': ts_list,
                        'label': label_list,
                        'idx': idx_list,
                        'w':w_list}), feat_l, node_ids







"""
functions for opensky
-------------------------------------------
"""

def convert_str2int(in_str):
    """
    convert strings to vectors of integers based on individual character
    each letter is converted as follows, a=10, b=11
    numbers are still int
    Parameters:
        in_str: an input string to parse
    Returns:
        out: a numpy integer array
    """
    out = []
    for element in in_str:
        if (element.isnumeric()):
            out.append(element)
        elif(element == "!"):
            out.append(-1)
        else:
            out.append(ord(element.upper()) -44 + 9)
    out = np.array(out, dtype=np.float32)
    return out


#! panda dataframe can't take numpy 2d arrays
def csv_to_pd_data(
        fname: str,
        ) -> pd.DataFrame:
    r'''
    currently used by open sky dataset
    convert the raw .csv data to pandas dataframe and numpy array
    input .csv file format should be: timestamp, node u, node v, attributes
    Args:
        fname: the path to the raw data
    '''
    feat_size = 16
    num_lines = sum(1 for line in open(fname)) - 1
    print ("number of lines counted", num_lines)
    u_list = np.zeros(num_lines)
    i_list = np.zeros(num_lines)
    ts_list = np.zeros(num_lines)
    label_list = np.zeros(num_lines)
    feat_l = np.zeros((num_lines, feat_size))
    idx_list = np.zeros(num_lines)
    w_list = np.zeros(num_lines)
    print ("numpy allocated")
    TIME_FORMAT = "%Y-%m-%d" #2019-01-01
    node_ids = {}
    unique_id = 0

    with open(fname, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            idx = 0
            #'day','src','dst','callsign','typecode'
            for row in tqdm(csv_reader):
                if (idx == 0):
                    idx += 1
                    continue
                else:
                    ts = row[0]
                    date_cur = datetime.strptime(ts, TIME_FORMAT)
                    ts = float(date_cur.timestamp())
                    src = row[1]
                    dst = row[2]

                    # 'callsign' has max size 8, can be 4, 5, 6, or 7
                    # 'typecode' has max size 8
                    # use ! as padding

                    # pad row[3] to size 7
                    if (len(row[3]) == 0):
                        row[3] = "!!!!!!!!"
                    while (len(row[3]) < 8):
                        row[3] += "!"

                    # pad row[4] to size 4
                    if (len(row[4]) == 0):
                        row[4] = "!!!!!!!!"
                    while (len(row[4]) < 8):
                        row[4] += "!"
                    if (len(row[4]) > 8):
                        row[4] = "!!!!!!!!"

                    feat_str = row[3] + row[4]

                    if (src not in node_ids):
                        node_ids[src] = unique_id
                        unique_id += 1
                    if (dst not in node_ids):
                        node_ids[dst] = unique_id
                        unique_id += 1
                    u = node_ids[src]
                    i = node_ids[dst]
                    u_list[idx-1] = u
                    i_list[idx-1] = i
                    ts_list[idx-1] = ts
                    idx_list[idx-1] = idx
                    w_list[idx-1] = float(1)
                    feat_l[idx-1] = convert_str2int(feat_str)
                    idx += 1
    return pd.DataFrame({'u': u_list,
                        'i': i_list,
                        'ts': ts_list,
                        'label': label_list,
                        'idx': idx_list,
                        'w':w_list}), feat_l, node_ids




def process_node_feat(
        fname: str,
        node_ids, 
        ):
    """
    1. need to have the same node id as csv_to_pd_data
    2. process the various node features into a vector
    3. return a numpy array of node features with index corresponding to node id

    airport_code,type,continent,iso_region,longitude,latitude
    type: onehot encoding
    continent: onehot encoding
    iso_region: alphabet encoding same as edge feat
    longitude: float divide by 180
    latitude: float divide by 90
    """
    feat_size = 20
    node_feat = np.zeros((len(node_ids), feat_size))
    type_dict = {}
    type_idx = 0
    continent_dict = {}
    cont_idx = 0

    with open(fname, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        idx = 0
        #airport_code,type,continent,iso_region,longitude,latitude
        for row in tqdm(csv_reader):
            if (idx == 0):
                idx += 1
                continue
            else:
                code = row[0]
                if (code not in node_ids):
                    continue
                else:
                    node_id = node_ids[code]
                    airport_type = row[1]
                    if (airport_type not in type_dict):
                        type_dict[airport_type] = type_idx
                        type_idx += 1
                    continent = row[2]
                    if (continent not in continent_dict):
                        continent_dict[continent] = cont_idx
                        cont_idx += 1

    with open(fname, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        idx = 0
        #airport_code,type,continent,iso_region,longitude,latitude
        for row in tqdm(csv_reader):
            if (idx == 0):
                idx += 1
                continue
            else:
                code = row[0]
                if (code not in node_ids):
                    continue
                else:
                    node_id = node_ids[code]
                    airport_type = type_dict[row[1]]
                    type_vec = np.zeros(type_idx)
                    type_vec[airport_type] = 1
                    continent = continent_dict[row[2]]
                    cont_vec = np.zeros(cont_idx)
                    cont_vec[continent] = 1
                    while (len(row[3]) < 7):
                        row[3] += "!"
                    iso_region = convert_str2int(row[3]) #numpy float array
                    lng = float(row[4])
                    lat = float(row[5])
                    coor_vec = np.array([lng, lat])
                    final = np.concatenate((type_vec,cont_vec,iso_region,coor_vec), axis=0)
                    node_feat[node_id] = final
    return node_feat









"""
functions for lastfmgenre
-------------------------------------------
"""

#! these are helper functions
# TODO cleaning the un trade csv with countries with comma in the name, to remove this function
def clean_rows(
        fname: str,
        outname: str,
    ):
    r'''
    clean the rows with comma in the name
    args:
        fname: the path to the raw data
        outname: the path to the cleaned data
    '''

    outf = open(outname, "w")

    with open(fname) as f:
        s = next(f)
        outf.write(s)
        for idx, line in enumerate(f):
            strs = ['China, Taiwan Province of', 'China, mainland'] 
            for str in strs:
                    line = line.replace('China, Taiwan Province of', "Taiwan Province of China")
                    line = line.replace('China, mainland', "China mainland")
                    line = line.replace('China, Hong Kong SAR', "China Hong Kong SAR")
                    line = line.replace('China, Macao SAR', "China Macao SAR")
                    line = line.replace('Saint Helena, Ascension and Tristan da Cunha', 'Saint Helena Ascension and Tristan da Cunha')
                    
            
            e = line.strip().split(',')
            if (len(e) > 4):
                print (e)
                raise ValueError("line has more than 4 elements")
            outf.write(line)

    outf.close()



def sort_edgelist(fname, 
                  outname = 'sorted_lastfm_edgelist.csv'):
    r"""
    sort the edgelist by time
    """
    edgelist = open(fname, "r")
    lines = list(edgelist.readlines())
    edgelist.close()
    
    with open(outname, 'w') as outf:
        write = csv.writer(outf)
        fields = ["time", "user_id", "genre", "weight"]              
        write.writerow(fields)
        
        rows_dict = {}
        for idx in range(1,len(lines)):
            vals = lines[idx].split(',')
            user_id = vals[0]
            time_ts = vals[1][:-7]
            genre = vals[2]
            w = float(vals[3].strip())
            if (time_ts not in rows_dict):
                rows_dict[time_ts] = [(user_id, genre, w)]
            else:
                rows_dict[time_ts].append((user_id, genre, w))
        
        time_keys = list(rows_dict.keys())
        time_keys.sort()
        
        for ts in time_keys:
            rows = rows_dict[ts]
            for user_id, genre, w in rows:
                write.writerow([ts, user_id, genre, w])
                



def sort_node_labels(fname,
                     outname):
    r"""
    sort the node labels by time
    """
    edgelist = open(fname, "r")
    lines = list(edgelist.readlines())
    edgelist.close()
    
    with open(outname, 'w') as outf:
        write = csv.writer(outf)
        fields = ["time", 'user_id', 'genre', 'weight']         
        write.writerow(fields)
        rows_dict = {}
        
        for i in range(1,len(lines)):
            vals = lines[i].split(',')
            user_id = vals[0]
            year = int(vals[1])
            month = int(vals[2])
            day = int(vals[3])
            genre = vals[4]
            w = float(vals[5])
            date_cur = datetime(year,month,day)
            time_ts = date_cur.strftime("%Y-%m-%d")
            if (time_ts not in rows_dict):
                rows_dict[time_ts] = [(user_id, genre, w)]
            else:
                rows_dict[time_ts].append((user_id, genre, w))
                
        time_keys = list(rows_dict.keys())
        time_keys.sort()
        
        for ts in time_keys:
            rows = rows_dict[ts]
            for user_id, genre, w in rows:
                write.writerow([ts, user_id, genre, w])
            
    
    
#! data loading functions
def load_node_labels(fname,
                     genre_index,
                     user_index):
    r"""
    load node labels as weight distribution
    time, user_id, genre, weight
    assume node labels are already sorted by time
    convert all time unit to unix time
    genre_index: a dictionary mapping genre to index
    """
    if not osp.exists(fname):
        raise FileNotFoundError(f"File not found at {fname}")
    #lastfmgenre dataset
    edgelist = open(fname, "r")
    lines = list(edgelist.readlines())
    edgelist.close()
    
    TIME_FORMAT = "%Y-%m-%d"

    # day, user_idx, label_vec
    label_size = len(genre_index)
    label_vec = np.zeros(label_size)
    date_prev = 0
    prev_user = 0
    
    ts_list = []
    node_id_list = []
    y_list = []
    

    #user_id,year,month,day,genre,weight
    for i in tqdm(range(1,len(lines))):
        vals = lines[i].split(',')
        user_id = user_index[vals[1]]
        ts = vals[0]
        genre = vals[2]
        weight = float(vals[3])
        date_cur = datetime.strptime(ts, TIME_FORMAT)
        if (i == 1):
            date_prev = date_cur
            prev_user = user_id
        #the next day
        if (date_cur != date_prev):
            ts_list.append(date_prev.timestamp())
            node_id_list.append(prev_user)
            y_list.append(label_vec)
            label_vec = np.zeros(label_size)
            date_prev = date_cur
            prev_user = user_id
        else:
            label_vec[genre_index[genre]] = weight
            
        if (user_id != prev_user):
            ts_list.append(date_prev.timestamp())
            node_id_list.append(prev_user)
            y_list.append(label_vec)
            prev_user = user_id
            label_vec = np.zeros(label_size)
    return pd.DataFrame({'ts': ts_list,
                        'node_id': node_id_list,
                        'y': y_list})


def load_edgelist(fname, genre_index):
    """
    load the edgelist into a pandas dataframe
    assume all edges are already sorted by time
    convert all time unit to unix time
    
    time, user_id, genre, weight
    """
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"  #2005-02-14 00:00:3
    #lastfmgenre dataset
    edgelist = open(fname, "r")
    lines = list(edgelist.readlines())
    edgelist.close()

    user_index = {} #map user id to index
    unique_id = max(genre_index.values()) + 1
    u_list = []
    i_list = []
    ts_list = []
    label_list = []
    idx_list = []
    feat_l = []
    w_list = []
    for idx in tqdm(range(1,len(lines))):
        vals = lines[idx].split(',')
        time_ts = vals[0]
        user_id = vals[1]
        genre = vals[2]
        w = float(vals[3].strip())
        date_object = datetime.strptime(time_ts, TIME_FORMAT)
        if (user_id not in user_index):
            user_index[user_id] = unique_id
            unique_id += 1

        u = user_index[user_id]
        i = genre_index[genre]
        label = 0
        feat = np.zeros((1))
        u_list.append(u)
        i_list.append(i)
        ts_list.append(date_object.timestamp())
        label_list.append(label)
        idx_list.append(idx)
        feat_l.append(feat)
        w_list.append(w)

    return pd.DataFrame({'u': u_list,
                        'i': i_list,
                        'ts': ts_list,
                        'label': label_list,
                        'idx': idx_list,
                        'w':w_list}), user_index


def load_genre_list(fname):
    """
    load the list of genres 
    """
    if not osp.exists(fname):
        raise FileNotFoundError(f"File not found at {fname}")

    edgelist = open(fname, "r")
    lines = list(edgelist.readlines())
    edgelist.close()

    genre_index = {}
    ctr = 0
    for i in range(1,len(lines)):
        vals = lines[i].split(',')
        genre = vals[0]
        if (genre not in genre_index):
            genre_index[genre] = ctr
            ctr += 1
        else:
            raise ValueError("duplicate in genre_index")
    return genre_index



"""
functions for wikipedia and un_trade
-------------------------------------------
"""
def _to_pd_data(
        fname: str,
        ):
    r'''
    convert the raw .csv data to pandas dataframe and numpy array
    input .csv file format should be: timestamp, node u, node v, weight w, 
    Args:
        fname: the path to the raw data
    '''
    u_list, i_list, ts_list, label_list = [], [], [], []
    feat_l = []
    idx_list = []
    w_list = []

    with open(fname) as f:
        s = next(f)
        node_ids = {}
        unique_id = 0
        for idx, line in enumerate(f):
            e = line.strip().split(',')
            if (len(e) > 4):
                print (e)
            #convert to integer node id
            ts = float(e[0])

            if (e[1] not in node_ids):
                node_ids[e[1]] = unique_id
                unique_id += 1
            if (e[2] not in node_ids):
                node_ids[e[2]] = unique_id
                unique_id += 1
            
            u = node_ids[e[1]]
            i = node_ids[e[2]]
            w = float(e[3])

            label = 0
            feat = np.zeros((1))

            u_list.append(u)
            i_list.append(i)
            ts_list.append(ts)
            label_list.append(label)
            idx_list.append(idx)
            feat_l.append(feat)
            w_list.append(w)
    
    return pd.DataFrame({'u': u_list,
                        'i': i_list,
                        'ts': ts_list,
                        'label': label_list,
                        'idx': idx_list,
                        'w':w_list}), np.array(feat_l)




def reindex(
        df: pd.DataFrame, 
        bipartite: Optional[bool] = False,
        ):
    r'''
    reindex the nodes especially if the node ids are not integers
    Args:
        df: the pandas dataframe containing the graph
        bipartite: whether the graph is bipartite
    '''
    new_df = df.copy()
    if bipartite:
        assert (df.u.max() - df.u.min() + 1 == len(df.u.unique()))
        assert (df.i.max() - df.i.min() + 1 == len(df.i.unique()))

        upper_u = df.u.max() + 1
        new_i = df.i + upper_u

        new_df.i = new_i
        new_df.u += 1
        new_df.i += 1
        new_df.idx += 1
    else:
        new_df.u += 1
        new_df.i += 1
        new_df.idx += 1

    return new_df

if __name__ == "__main__":
    # """
    # clean rows for un trade dataset
    # """
    # fname = "/mnt/c/Users/sheny/Desktop/TGB/tgb/datasets/un_trade/un_trade.csv"
    # outname = "/mnt/c/Users/sheny/Desktop/TGB/tgb/datasets/un_trade/un_trade_cleaned.csv"
    # clean_rows(fname, outname)
    
    # """
    # sort edgelist by time for lastfm dataset
    # """
    # fname = "../datasets/lastfmGenre/lastfm_edgelist_clean.csv"
    # outname = '../datasets/lastfmGenre/sorted_lastfm_edgelist.csv'
    # sort_edgelist(fname, 
    #               outname = outname)
    
    """
    sort node labels by time for lastfm dataset
    """
    fname = "../datasets/lastfmGenre/7days_labels.csv"
    outname = '../datasets/lastfmGenre/sorted_7days_node_labels.csv'
    sort_node_labels(fname,
                     outname)
    
    
    