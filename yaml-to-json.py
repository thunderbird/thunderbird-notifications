import json
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

  def write_schema_as_json(self, schema, out_file):
    try:
      out_file.write(schema.model_dump_json(indent=2))
    except Exception as e:
      print(f'Error writing JSON file: {e}')

  def convert(self):
    for in_fname in self.get_yaml_files():
      schema = NotificationSchema.from_yaml(in_fname)

      out_fname = self.generate_json_name(in_fname)
      if out_fname:
        out_path = os.path.join(self.json_dir, out_fname)
        if not os.path.exists(out_path):
          with open(out_path, "w") as f:
            self.write_schema_as_json(schema, f)

  @classmethod
  def generate_json_schema(cls):
      schema = NotificationSchema.model_json_schema()  # (1)!
      with open('generated-schema.json', "w") as f:
            f.write(json.dumps(schema, indent=2))

def main():
  converter = YAMLtoJSONConverter(YAML_DIR, JSON_DIR)
  converter.convert()

if __name__ == "__main__":
  main()
