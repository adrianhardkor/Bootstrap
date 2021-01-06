#!/usr/bin/python3

# USAGE: ./convert_report_to_cucumber_format.py --behave-report bdd/report.json [--json-schema cucumber-report-schema.json]

import argparse, json, sys
from jsonschema import Draft4Validator

def main(argv=None):
    args = parse_args(argv)

    with open(args.json_schema, 'r') as json_file:
        schema = json.load(json_file)
    with open(args.behave_report, 'r') as json_file:
        report = json.load(json_file)

    convert_report(report)
    print(json.dumps(report, sort_keys=True, indent=2))
    validate_json(schema, report)

def convert_report(report):
    # delete_tags param has been introduced for XRay integration purpose
    def common_processing(item, delete_tags):
        item['uri'], item['line'] = item.pop('location').split(':')
        item['line'] = int(item['line'])
        if delete_tags:
            item['tags'] = []
        else:
            item['tags'] = [{'name': '@' + tag} for tag in item.get('tags', [])]
        if 'id' not in item:
            item['id'] = item['name'].replace(' ', '-').lower()
        if 'description' in item:
            #assert len(item['description']) == 1
            item['description'] = item['description'][0]
        else:
            item['description'] = ''

    for feature in report:
        common_processing(feature, True)
        for scenario in feature['elements']:
            common_processing(scenario, False)
            for step in scenario['steps']:
                step['uri'], step['line'] = step.pop('location').split(':')
                step['line'] = int(step['line'])
                if 'result' in step:
                    step['result']['duration'] = int(1000000000 * step['result']['duration'])
                else:
                    step['result'] = {'status': 'skipped', 'duration': 0}
                if 'table' in step:
                    step['rows'] = [{'cells': step['table']['headings']}] + [{'cells': cells} for cells in step['table']['rows']]
                    del step['table']
                if 'match' in step:
                    if 'arguments' in step['match']:
                        step['match']['arguments'] = [{'val': '{}'.format(arg['value']), 'offset': 0} for arg in step['match']['arguments']]
                else:
                    step['match'] = {'arguments': [], 'location': 'UNKNOWN - SKIPPED'}

def validate_json(schema, report):
    errors = list(Draft4Validator(schema).iter_errors(report))
    for error in errors:
        print('#/' + '/'.join([str(path) for path in error.path]), error.message, file=sys.stderr)
    if errors:
        sys.exit(1)

def parse_args(argv):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--json-schema', required=True, help=' ')
    parser.add_argument('--behave-report', required=True, help=' ')
    return parser.parse_args(argv)

if __name__ == '__main__':
    main()
