import argparse
from client import get_client
from pprint import pprint


def create_additional_assignments(hit_id='', number=0, sandbox=True):
    get_client(sandbox=sandbox).create_additional_assignments_for_hit(HITId=hit_id, NumberOfAdditionalAssignments=number)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add additional assignments to existing HIT.')

    parser.add_argument('--hit_id', dest='hit_id', help='HIT ID of HIT to add assignments to', required=True)
    parser.add_argument('--number', dest='number', type=int, help='How many assignments to add', required=True)
    parser.add_argument('--sandbox', dest='sandbox', action='store_true', help='Whether to use the sandbox')

    args = parser.parse_args()

    pprint(create_additional_assignments(hit_id=args.hit_id, number=args.number, sandbox=args.sandbox))
