import argparse
import sys
from notifications.lib.notification_model import NotificationModel

parser = argparse.ArgumentParser(description='Generates JSON Schema file.')
parser.add_argument('schema_file_name', type=str, help='Name of file to write')
args = parser.parse_args()

def main():
  if len(sys.argv) != 2:
      parser.print_help()
      sys.exit(1)
  NotificationModel.generate_json_schema(args.schema_file_name)

if __name__ == "__main__":
  main()
