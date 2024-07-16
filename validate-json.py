import os
import subprocess
import sys
import argparse

parser = argparse.ArgumentParser(description='Validate JSON schema and JSON files for Thunderbird notifications.')
parser.add_argument('schema_file', type=str, help='The schema file to validate against.')
parser.add_argument('json_dir', type=str, help='The directory containing JSON files.')
args = parser.parse_args()

class JSONValidator:
  def __init__(self, schema_file, json_dir):
    self.schema_file = schema_file
    self.json_dir = json_dir

    if not os.path.isfile(self.schema_file):
      raise ValueError(f'Argument for schema file "{schema_file}" was not found.')

    if not os.path.isdir(self.json_dir):
      raise ValueError(f'Argument for json_dir "{self.json_dir}" is not a directory')

  def validate(self):
    json_files = [f for f in os.listdir(self.json_dir) if f.endswith('.json')]
    print(json_files)
    if not json_files:
        print("No JSON files to process.")
        return 0  # Exit successfully if no JSON files are found

    command = ['jv', self.schema_file] + [os.path.join(self.json_dir, f) for f in json_files]

    try:
      result = subprocess.run(command, check=True, stdout=subprocess.PIPE,  stderr=subprocess.PIPE, text=True)
      print('Validation command completed successfully')
      return 0
    except subprocess.CalledProcessError as e:
      print(f'Error running validation command: {e.stderr}', file=sys.stderr)
      return 1

def main():
  if len(sys.argv) < 3 or len(sys.argv) > 4:
      parser.print_help()
      sys.exit(1)

  validator = JSONValidator(args.schema_file, args.json_dir)
  exit_code = validator.validate()
  sys.exit(exit_code)

if __name__ == "__main__":
  main()

