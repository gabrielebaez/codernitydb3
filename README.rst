SlitheringDB - a Pythonic database
=============================================

SlitheringDB is based on CodernityDB by `Codernity Labs`_.

SlitheringDB is opensource, pure python, multiplatform, schema-less, `NoSQL <http://en.wikipedia.org/wiki/NoSQL>`_ database. It has optional support for HTTP server version (SlitheringDB-server), and also Python client library (SlitheringDB-client).

You can call it a more advanced key-value database. With multiple key-values indexes in the same engine.


Key features
------------

* Native python database
* Multiple indexes
* Fast (more than 50 000 insert operations per second see Speed in documentation for details)
* Embeded mode (default) and Server (CodernityDB-HTTP), with client library (CodernityDB-PyClient) that aims to be 100% compatible with embeded one.
* Easy way to implement custom Storage
* Sharding support


Install
-------

from sources::

   git clone ssh://git@github.com:gabrielebaez/slitheringdb.git
   cd slitheringdb
   python setup.py install

License
-------

Copyright 2024 Gabriel E. Báez (https://github.com/gabrielebaez)

Copyright 2020 Nick M. (https://github.com/nickmasster)

Copyright 2011-2013 Codernity (http://codernity.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
