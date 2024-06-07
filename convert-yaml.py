import glob
import os

from NotificationSchema import NotificationSchema

YAML_DIR = 'yaml_notifications'
JSON_DIR = 'json_notifications'

class YAMLtoJSONConverter:
  def __init__(self, yaml_dir, json_dir):
    self.yaml_dir = yaml_dir
    self.json_dir = json_dir

    if not os.path.isdir(self.yaml_dir):
      raise ValueError(f"'{self.yaml_dir}' is not a directory")
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
      if not os.path.exists(json_file_path):
        with open(json_file_path, "w") as f:
          self.write_schema_as_json(schema, f)

def main():
  converter = YAMLtoJSONConverter(YAML_DIR, JSON_DIR)
  converter.convert()

if __name__ == "__main__":
  main()
