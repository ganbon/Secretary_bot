import pickle


path_dict = {} #keyにアプリ名、valuseにアプリのpath
with open('app_path_data.pkl','wb') as tf:
    pickle.dump(path_dict,tf)