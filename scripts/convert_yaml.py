import glob
import os
import sys
import argparse

from notifications.lib.notification_model import NotificationModel

JSON_FILE_NAME = 'notifications.json'

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

  def generate_json_file_name(self, yaml_file_path):
    # Extract and verify the file extension
    base_name, ext = os.path.splitext(yaml_file_path)
    if ext.lower() != '.yaml':
      return None
    return f'{os.path.basename(base_name)}.json'

  def write_schema_as_json(self, schema, json_file):
    try:
      dump = schema.model_dump_json(indent=2)
      json_file.write(dump)
    except Exception as e:
      print(f'Error writing JSON file: {e}')

  def convert(self):
    """Reads, validates YAML files from a directory and writes JSON files to separate directory."""

    schema = NotificationModel.from_yaml_dir(self.yaml_dir)
    json_file_path = os.path.join(self.json_dir, JSON_FILE_NAME)
    with open(json_file_path, "w") as f:
      print(f'Writing JSON to: {json_file_path}')
      self.write_schema_as_json(schema, f)

def main():
  if len(sys.argv) < 3 or len(sys.argv) > 4:
      parser.print_help()
      sys.exit(1)

  converter = YAMLtoJSONConverter(args.yaml_dir, args.json_dir)
  converter.convert()

if __name__ == "__main__":
  main()
