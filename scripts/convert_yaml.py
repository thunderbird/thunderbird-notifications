import os
import sys
import argparse
from pprint import pprint

from notifications.lib.notification_model import NotificationModel

DEFAULT_JSON_FILE_PATH = 'json/notifications.json'

parser = argparse.ArgumentParser(description='Converts Thunderbird notifications from YAML to JSON.')
parser.add_argument('yaml_dir', type=str, help='Directory containing notifications as YAML files')
parser.add_argument(
    'json_file_path',
    type=str,
    nargs='?',
    default=DEFAULT_JSON_FILE_PATH,
    help=f'File path of the JSON file to write (default: {DEFAULT_JSON_FILE_PATH})',
)


class YAMLtoJSONConverter:
    def __init__(self, yaml_dir, json_file_path):
        self.yaml_dir = yaml_dir
        self.json_file_path = json_file_path

        if not os.path.isdir(self.yaml_dir):
            raise ValueError(f"Argument for yaml_dir '{self.yaml_dir}' is not a directory")
        json_dir = os.path.dirname(self.json_file_path)
        if not os.path.exists(json_dir):
            os.makedirs(json_dir, exist_ok=True)

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

        with open(self.json_file_path, 'w') as f:
            print(f'Writing JSON to: {self.json_file_path}')
            pprint(schema)
            self.write_schema_as_json(schema, f)


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    converter = YAMLtoJSONConverter(args.yaml_dir, args.json_file_path)
    converter.convert()


if __name__ == '__main__':
    main()
