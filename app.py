""" generate funtion to load yml """ 
def load_yml(file_path):
  """Load YAML file from given path"""
  import yaml
  with open(file_path, 'r') as f:
    return yaml.safe_load(f)
