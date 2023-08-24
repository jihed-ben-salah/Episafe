import pandas as pd 
import os 
import multiprocessing


def folder_gen(data):
    folder_feature = []
    for i in range(data.shape[0]):
        parts = data['path'][i].split('/')
        folder_feature.append(parts[7])
    data['folder'] = folder_feature
    return data

def clientid_gen(data):
    client_id_feature = []
    for i in range(data.shape[0]):
        parts = data['path'][i].split('/')
        client_id_feature.append(parts[6])
    data['client_id'] = client_id_feature
    return data

def date_gen(data):
    date_feature = []
    for i in range(data.shape[0]):
        parts = data['path'][i].split('/')
        date_feature.append(parts[8].split('-')[1])
    data['date'] = date_feature
    return data

def time_gen(data):
    time_feature = []
    for i in range(data.shape[0]):
        parts = data['path'][i].split('/')
        time_feature.append(parts[8].split('-')[2].split('.')[0])
    data['time_slot'] = time_feature
    return data

def filename_gen(data):
    file_name_feature = []
    for i in range(data.shape[0]):
        parts = data['path'][i].split('/')
        file_name_feature.append(parts[8])
    data['file_name'] = file_name_feature
    return data


def label_gen(data,labels):
    labels_feature = []
    for i in range(data.shape[0]):
        if data['file_name'][i] in labels['filepath']:
            labels_feature.append(1)
        else: 
            labels_feature.append(0)
    data['label'] = labels_feature

    return data

def drop_path(data):
    data.drop('path',axis = 1, inplace=True)
    data.drop('file_name',axis=1,inplace=True)
    return data


def worker_function(process_num):
    print(f"Process {process_num} starting")
    data_path = 'D:/Orange/Episafe/generated-data'
    labels = pd.read_csv('epileptic_records2.csv')
    for i in os.listdir(data_path):
        path = os.path.join(data_path,i).replace(os.path.sep,'/')
        data = pd.read_csv(path)
        op1 = folder_gen(data)
        op2 = clientid_gen(op1)
        op3 = date_gen(op2)
        op4 = time_gen(op3)
        op5 = filename_gen(op4)
        op6 = label_gen(op5,labels)
        op7 = drop_path(op6)
        op7.to_csv(i)
    print(f"Process {process_num} finished")

def main():
    num_processes = 10  # Number of processes you want to run
    processes = []

    for i in range(num_processes):
        process = multiprocessing.Process(target=worker_function, args=(i,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()  # Wait for all processes to finish

    print("All processes have finished.")

if __name__ == "__main__":
    main()