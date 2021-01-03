import json
import zlib
from diffupdatematcher import DiffUpdateMatcher


class DDBFile:
    """
    A class that contains code for working with diffupdate dbs, serialization, deserialization etc
    """
    def __init__(self, name: str, versions: list = None):
        """
        Loads/Saves a diffupdate db
        :param name: the file to be outputed to/ loaded from
        :param versions: the files to be included in the db
        if versions is None then the class attempts to load a db with the passed filename

        to create an empty db you should pass versions as []
        """
        self.versions = versions
        self.original_file = versions[0] if versions else None
        self.all_ops = {}
        self.out_file = name + ".ddb" if not name.endswith(".ddb") else name
        self.bin = b''
        self.updated = b''

        # Load
        if versions is None:
            try:
                with open(self.out_file, 'rb') as f:
                    self.bin = f.read()
                    self.load()
            except FileNotFoundError as e:
                print('File not found', e)
                exit(1)
            return

        # Save
        self.save()

    def update(self, version: str):
        """
        Attempts to open a file, find out its operations from the current db and apply those operations
        :param version:
        :return: void, but the updated field now contains the latest version as it was applied from passed version
        """
        with open(version, 'rb') as f:
            binary = f.read()
        crc = zlib.crc32(binary)
        if crc not in self.all_ops:
            print("file " + version + " not found in db")
            exit(1)

        d = DiffUpdateMatcher()
        try:
            d.operations = self.all_ops[crc]
        except KeyError:
            print('File is not the same as the files in the stored db')
        self.updated = d.apply_diff(binary)

    def dump(self):
        """
        Flushes db contents to file
        :return: void
        """
        with open(self.out_file, 'wb') as f:
            f.write(self.bin)
            print('Saved!')

    def save(self):
        """
        Serializes in the bin field the current db state
        :return: void
        """
        all_files = {}
        header = []
        body = b''

        try:
            for f in self.versions:
                with open(f, 'rb') as fd:
                    all_files[f] = fd.read()
        except FileNotFoundError as e:
            print('List of files is incorrect ', e)
            exit(1)

        for f in self.versions[1:]:
            d = DiffUpdateMatcher()
            d.do_diff(all_files[f], all_files[self.original_file])
            self.all_ops[f] = d.operations
            header.append([zlib.crc32(all_files[f]), len(d.operations)])
            body += d.operations

        header = json.dumps(header).encode('utf-8')
        self.bin = len(header).to_bytes(4, "little") + header + body

    def load(self):
        """
        loads a db in the current class object
        :return: void
        """
        header_sz = int.from_bytes(self.bin[:4], "little")
        sik = 4+header_sz
        header = json.loads(self.bin[4:sik].decode('utf-8'))
        for fi in header:
            self.all_ops[fi[0]] = self.bin[sik:sik+fi[1]]
            sik += fi[1]

        print('Loaded!')
