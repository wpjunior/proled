=====================
How FTP Works in Zope
=====================

- The FTP server implementation is in `zope.server.ftp.server`.  See
  the README.txt file there.

  The publisher-based ftp server is in `zope.server.ftp.publisher`.

  The FTP server gets wired up with a request factory that creates
  ftp requests with ftp publication objects.

- The ftp request object is defined in `zope.publisher.ftp`.

- The ftp publication object is defined in `zope.app.publication.ftp`.

  The publication object gets views to handle ftp requests.  It
  looks up a separate view for each method defined in
  `zope.publisher.interfaces.ftp.IFTPPublisher`.

  We provide a single class here that implements all of these methods. 

  The view, in turn, uses adapters for the `IReadFile`, `IWriteFile`,
  `IReadDirectory`, `IWriteDirectory`, `IFileFactory`, and
  `IDirectoryFactory`, defined in `zope.app.filerepresentation.interfaces`.

