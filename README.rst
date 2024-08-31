SlitheringDB - a Pythonic database
=============================================

SlitheringDB is based on CodernityDB by `Codernity Labs`_.

SlitheringDB is an open-source, pure python, schema-less, `NoSQL <http://en.wikipedia.org/wiki/NoSQL>`_ database. It can operate in embeded and server mode (SlitheringDB-server).

You can call it a more advanced key-value database With multi-index support.


Key features
------------

* Native python database
* Multiple indexes
* Fast (more than 50 000 insert operations per second see Speed in documentation for details)
* Embeded mode (default) and Server (SlitheringDB-server), with client library (SlitheringDB-client) that aims to be 100% compatible with embeded one.
* Easy way to implement custom Storage
* Sharding support


Install
-------

Note: Very early version, things will break.

from sources::

   git clone ssh://git@github.com:gabrielebaez/slitheringdb.git
   cd slitheringdb
   python setup.py install


License
-------

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
