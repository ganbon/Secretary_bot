import os.path
import yaml
with open('conda_env.yml', 'r') as yml:
    conda = yaml.safe_load(yml)
user_path = os.path.expanduser('~')
conda['prefix'] = user_path+r'\anaconda3\envs\bot-env'
with open("conda_env.yml", "w") as yf:
    yaml.dump(conda,yf)
