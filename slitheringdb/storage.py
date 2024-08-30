#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Nick M. (https://github.com/nickmasster)
# Copyright 2011-2013 Codernity (http://codernity.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# NOTE: ROOT Module

import os
import struct
import marshal
import io

import tempfile
import mmap
from slitheringdb import __version__


class StorageException(Exception):
    pass


class SimpleStorageEngine:
    def __init__(self, filename, record_format='if'):
        self.filename = filename
        self.wal_filename = f"{filename}.wal"
        self.record_format = record_format
        self.record_size = struct.calcsize(record_format)

        # Ensure the main file and WAL exist
        if not os.path.exists(filename):
            with open(filename, 'wb') as f:
                f.write(b'')
        
        if not os.path.exists(self.wal_filename):
            with open(self.wal_filename, 'wb') as f:
                f.write(b'')

        # Open the main file and memory-map it
        self.file = open(self.filename, 'r+b')
        self.mmap = mmap.mmap(self.file.fileno(), 0, access=mmap.ACCESS_WRITE)

        # Recover from WAL if necessary
        self.recover_from_wal()

    def _get_record_offset(self, record_id):
        return record_id * self.record_size

    def write_record(self, record_id, *values):
        packed_data = struct.pack(self.record_format, *values)
        offset = self._get_record_offset(record_id)

        # Ensure the file is large enough
        if offset + self.record_size > len(self.mmap):
            self._expand_file(offset + self.record_size)

        # Write to WAL first
        self.write_to_wal(record_id, packed_data)

        # Write to the temporary file for atomic write
        self.atomic_write(self.filename, self.mmap, offset, packed_data)

        # Clear the WAL after successful write
        self.clear_wal()

    def read_record(self, record_id):
        offset = self._get_record_offset(record_id)
        if offset + self.record_size > len(self.mmap):
            raise ValueError("Record ID out of range")

        packed_data = self.mmap[offset:offset + self.record_size]
        return struct.unpack(self.record_format, packed_data)

    def write_to_wal(self, record_id, data):
        with open(self.wal_filename, 'ab') as wal:
            wal.write(struct.pack('i', record_id) + data)
            wal.flush()
            os.fsync(wal.fileno())

    def recover_from_wal(self):
        """Replay the WAL to recover from a crash."""
        if os.path.getsize(self.wal_filename) == 0:
            return  # No WAL to recover

        with open(self.wal_filename, 'rb') as wal:
            while True:
                record = wal.read(4 + self.record_size)
                if not record:
                    break
                record_id, = struct.unpack('i', record[:4])
                data = record[4:]
                offset = self._get_record_offset(record_id)
                if offset + self.record_size > len(self.mmap):
                    self._expand_file(offset + self.record_size)
                self.mmap[offset:offset + self.record_size] = data

        # Clear WAL after recovery
        self.clear_wal()

    def atomic_write(self, filename, mmap_obj, offset, data):
        """Perform an atomic write by writing to a temp file and renaming it."""
        temp_file = tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(filename))
        try:
            # Write current mmap content
            temp_file.write(mmap_obj[:])
            # Apply the new data
            temp_file.seek(offset)
            temp_file.write(data)
            temp_file.flush()
            os.fsync(temp_file.fileno())
            temp_file.close()
            os.rename(temp_file.name, filename)
        except Exception:
            os.remove(temp_file.name)
            raise
        finally:
            self.reload_mmap()

    def clear_wal(self):
        """Clear the Write-Ahead Log after successful commit."""
        with open(self.wal_filename, 'wb') as wal:
            wal.truncate()
            wal.flush()
            os.fsync(wal.fileno())

    def _expand_file(self, size):
        """Expand the file to the given size."""
        self.file.seek(size - 1)
        self.file.write(b'\x00')
        self.file.flush()
        self.mmap.resize(size)

    def reload_mmap(self):
        """Reload the memory-mapped file after atomic write."""
        self.mmap.close()
        self.file.close()
        self.file = open(self.filename, 'r+b')
        self.mmap = mmap.mmap(self.file.fileno(), 0, access=mmap.ACCESS_WRITE)

    def close(self):
        """Close the memory-mapped file and the underlying file."""
        self.mmap.close()
        self.file.close()

class DummyStorage:
    """
    Storage mostly used to fake real storage
    """
    def create(self, *args, **kwargs):
        pass

    def open(self, *args, **kwargs):
        pass

    def close(self, *args, **kwargs):
        pass

    def data_from(self, *args, **kwargs):
        pass

    def data_to(self, *args, **kwargs):
        pass

    def save(self, *args, **kwargs):
        return 0, 0

    def insert(self, *args, **kwargs):
        return self.save(*args, **kwargs)

    def update(self, *args, **kwargs):
        return 0, 0

    def get(self, *args, **kwargs):
        return None

    # def compact(self, *args, **kwargs):
    #     pass

    def fsync(self, *args, **kwargs):
        pass

    def flush(self, *args, **kwargs):
        pass


class IU_Storage(object):

    __version__ = __version__

    def __init__(self, db_path, name='main'):
        self.db_path = db_path
        self.name = name
        self._header_size = 100
        self._f = None

    def create(self) -> None:
        if os.path.exists(os.path.join(self.db_path, self.name + "_stor")):
            raise IOError("Storage already exists!")

        with io.open(os.path.join(self.db_path, self.name + "_stor"), 'wb') as f:
            f.write(struct.pack("10s90s", self.__version__.encode('utf8'), b'|||||'))
            f.close()

        self._f = io.open(os.path.join(self.db_path, self.name + "_stor"),
                          'r+b',
                          buffering=0)
        self.flush()
        self._f.seek(0, 2)

    def open(self) -> None:
        if not os.path.exists(os.path.join(self.db_path, self.name + "_stor")):
            raise IOError("Storage doesn't exists!")
        self._f = io.open(os.path.join(self.db_path, self.name + "_stor"),
                          'r+b',
                          buffering=0)
        self.flush()
        self._f.seek(0, 2)

    def destroy(self) -> None:
        os.unlink(os.path.join(self.db_path, self.name + '_stor'))

    def close(self):
        self._f.close()
        # self.flush()
        # self.fsync()

    def data_from(self, data):
        return marshal.loads(data)

    def data_to(self, data):
        return marshal.dumps(data)

    def save(self, data):
        s_data = self.data_to(data)
        self._f.seek(0, 2)
        start = self._f.tell()
        size = len(s_data)
        self._f.write(s_data)
        self.flush()
        return start, size

    def insert(self, data):
        return self.save(data)

    def update(self, data):
        return self.save(data)

    def get(self, start, size, status='c'):
        if status == 'd':
            return None
        print(locals())
        self._f.seek(start)
        return self.data_from(self._f.read(size))

    def flush(self):
        self._f.flush()

    def fsync(self):
        os.fsync(self._f.fileno())


# classes for public use, done in this way because of
# generation static files with indexes (_index directory)


class Storage(IU_Storage):
    pass
