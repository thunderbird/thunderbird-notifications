import yaml
import json
import glob
import os

YAML_DIR = 'yaml_notifications'
JSON_DIR = 'json_notifications'

if not os.path.isdir(YAML_DIR):
  raise ValueError(f"'{YAML_DIR}' is not a directory")
if not os.path.isdir(JSON_DIR):
  os.makedirs(JSON_DIR)

class YAMLtoJSONConverter:
  def __init__(self, yaml_dir, json_dir):
    self.yaml_dir = yaml_dir
    self.json_dir = json_dir

  def get_yaml_files(self):
    # Using glob's ** pattern by specifying `recursive=True`
    yaml_files = glob.glob(f'./{self.yaml_dir}/**/*.yaml', recursive=True)
    return yaml_files

  def generate_json_name(self, yaml_filepath):
    # Extract and verify the file extension
    base_name, ext = os.path.splitext(yaml_filepath)
    if ext.lower() != '.yaml':
      return None
    return f'{os.path.basename(base_name)}.json'

  def yaml_to_json(self, in_file):
    try:
      return yaml.safe_load(in_file)
    except yaml.YAMLError as e:
      print(f'Error parsing YAML file: {e}')
      return None

  def write_json(self, data_from_yaml, out_file):
    try:
      json.dump(data_from_yaml, out_file, indent=2)
    except Exception as e:
      print(f'Error writing JSON file: {e}')

  def convert(self):
    for in_fname in self.get_yaml_files():
      with open(in_fname, "r") as in_file:
        data_from_yaml = self.yaml_to_json(in_file)
        if not data_from_yaml:
          continue

        out_fname = self.generate_json_name(in_fname)
        if out_fname:
          out_path = f'{self.json_dir}/{out_fname}'
          if not os.path.exists(out_path):
            with open(out_path, "w") as f:
              self.write_json(data_from_yaml, f)

def main():
  converter = YAMLtoJSONConverter(YAML_DIR, JSON_DIR)
  converter.convert()

if __name__ == "__main__":
  main()
