import argparse
import sys


class DDBFile:
    def __init__(self, name: str, versions: list = None):
        self.out_file = name + ".ddb"
        self.versions = versions

    def goto(self, version: str):
        pass

    def dump(self):
        with open(self.out_file, 'w') as f:
            f.write('')

    def load(self):
        return self


def main(argv: list):
    parser = argparse.ArgumentParser(
        description='DiffUpdate stores different versions of binary files in an efficient manner'
                    '- by retaining differences between versions instead of the entire files'
    )
    parser.add_help = True
    parser.add_argument("--create", nargs='+',
                        help='Creates a version db for the specified file'
                             'usage:'
                             'diffupdate create <file.version1> <file.version2> <...>'
                             'note: the order of the passed files does not matter, you will change between versions either by names or assigned id'
                        )
    parser.add_argument("-n", "--name", type=str,
                        help='By default, the db has the name of the first passed file, use this to change the db name'
                             'usage:'
                             'diffupdate create <file.version1> <file.version2> <...> --name my_file_history.ddb'
                        )
    parser.add_argument("--update", nargs='+',
                        help='Using a previously created db, navigate to the specified version'
                             'usage:'
                             'diffupdate update <file.version2> <db_file.ddb>'
                        )
    # parser.add_argument("list", type=str,
    #                     help='[FUTURE] Using a previously created db, list all the files in the given db'
    #                     )

    args = parser.parse_args(args=argv)

    if args.create:
        db_name = args.name if args.name else args.create[0].split('.')[0]
        db = DDBFile(db_name, args.create)

        db.dump()
        print('Created new db: ' + db.out_file)
    if args.update:
        if args.name:
            db_name = args.name
            assert len(args.update) == 1, "Expected 1 parameter but a different number was provided"
        else:
            assert len(args.update) == 2, "Incorrect parameters for update command"
            db_name = args.update[1]

        DDBFile(db_name).load().goto(args.update[0])


if __name__ == "__main__":
    main(sys.argv)
