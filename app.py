 """ generate function to load yml """ 
import yaml

def load_yml(file_path):
  with open(file_path, 'r') as f:
    return yaml.safe_load(f)
