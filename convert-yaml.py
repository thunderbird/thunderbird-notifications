import glob
import os
import sys
import argparse

from NotificationSchema import NotificationSchema

parser = argparse.ArgumentParser(description='Converts Thunderbird notifications from YAML to JSON.')
parser.add_argument('yaml_dir', type=str, help='Directory containing notifications as YAML files')
parser.add_argument('json_dir', type=str, help='Directory to output JSON files')
parser.add_argument('--overwrite', help='Overwrite existing JSON files',  action='store_true')
args = parser.parse_args()

class YAMLtoJSONConverter:
  def __init__(self, yaml_dir, json_dir):
    self.yaml_dir = yaml_dir
    self.json_dir = json_dir

    if not os.path.isdir(self.yaml_dir):
      raise ValueError(f"Argument for yaml_dir '{self.yaml_dir}' is not a directory")
    if not os.path.isdir(self.json_dir):
      os.makedirs(self.json_dir)

  def get_yaml_file_paths(self):
    # Using glob's ** pattern by specifying `recursive=True`
    yaml_file_paths = glob.glob(f'./{self.yaml_dir}/**/*.yaml', recursive=True)
    return yaml_file_paths

  def generate_json_file_name(self, yaml_file_path):
    # Extract and verify the file extension
    base_name, ext = os.path.splitext(yaml_file_path)
    if ext.lower() != '.yaml':
      return None
    return f'{os.path.basename(base_name)}.json'

  def write_schema_as_json(self, schema, json_file):
    try:
      json_file.write(schema.model_dump_json(indent=2))
    except Exception as e:
      print(f'Error writing JSON file: {e}')

  def convert(self):
    """Reads, validates YAML files from a directory and writes JSON files to separate directory."""
    for yaml_file_path in self.get_yaml_file_paths():
      schema = NotificationSchema.from_yaml(yaml_file_path)

      json_file_name = self.generate_json_file_name(yaml_file_path)
      if not json_file_name:
        continue

      json_file_path = os.path.join(self.json_dir, json_file_name)
      does_exist = os.path.exists(json_file_path)
      should_write = args.overwrite or not does_exist
      if should_write:
        with open(json_file_path, "w") as f:
          self.write_schema_as_json(schema, f)

def main():
  if len(sys.argv) < 3 or len(sys.argv) > 4:
      parser.print_help()
      sys.exit(1)

  converter = YAMLtoJSONConverter(args.yaml_dir, args.json_dir)
  converter.convert()

if __name__ == "__main__":
  main()

