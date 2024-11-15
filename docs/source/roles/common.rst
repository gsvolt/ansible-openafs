openafs_common - OpenAFS Common Role
====================================

Description
-----------

Common definitions for OpenAFS clients and servers.

Variables
---------

afs_cell
  The OpenAFS cell name. Default: ``example.com``

afs_realm
  The Kerberos realm name. Defaults to the uppercased cell name. Default: ``EXAMPLE.COM``

afs_cell_files
  Location of cell specific files on the controller. Default: ``~/.ansible_openafs/cell/<cell>``

afs_csdb
  The CellServDB information for this cell. Undefined by default.
  The ``afs_csdb`` should be provided in your inventory. If not defined, the
  ``afs_csdb`` is read from the external yaml file located at the
  fully qualified path given by the variable ``afs_csdb_file``.

.. code-block:: yaml

    afs_csdb:
      cell: example.com
      desc: Cell name
      hosts:
        - ip: 192.168.122.219
          name: afs02
          clone: no
        - ip: 192.168.122.154
          name: afs03
          clone: no
        - ip: 192.168.122.195
          name: afs04
          clone: no

afs_csdb_file
  The path to the external yaml file containing CellServDB information for the
  cell. This file is read when the ``afs_csdb`` is not defined in the inventory.
  The ``afs_csdb_file`` can be created in a playbook with the ``generate_csdb``
  task. This can be useful in to automatically create a usable CellServDB file
  in a test environment.

  The CellServDB information for the cell. This must be provided as a inventory
  variable or an external yaml file, the path specified by ``afs_csdb_file``.

  Default: ``<afs_cell_files>/csdb.yaml``

afs_admin
  An administrative user name. This is the ``pts`` user name, for example: ``jdoe.admin``
  Can also be a list.
  Default: ``<ansible_user>.admin``

afs_install_method
  The method used to install the OpenAFS client and/or server software on this
  remote node. Must be one of: ``managed``, ``packages``, ``bdist``, ``source``.

  Default: platform dependent

afs_checkout_method
  The method used to checkout source code when the ``afs_install_method`` is
  ``source``.  Must be one of: ``none``, ``git``, ``sdist_upload``, ``gerrit``
  Specify ``none`` to skip the checkout during the Ansible play.

  Default: ``git``

afs_yum_repo
  The yum repo url when ``afs_install_method`` is ``managed``.

  Default: ``https://download.sinenomine.net/openafs/rpms/el$releasever/$basearch``

afs_install_archive
  Path or URL to the compressed archive containing the packages or binary files
  when the ``afs_install_method`` is ``packages``, ``bdist``, or ``sdist``.

  The tarball will be downloaded to the remote node automatically when
  ``afs_install_archive`` startes with ``http://``.  Otherwise, the path is to a
  file already existing on the remote node.

  Set ``afs_install_archive_remote_src`` to ``false`` to indicate the file should
  be uploaded from the controller to the target machine.

afs_install_archive_remote_src
  When set to ``false``, the path indicated in ``afs_install_archive`` is a
  local path (on the controller) and the archive will be uploaded from the controller
  to the remote node. It can be an absolute or relative path.

afs_git_repo
  The git repository URL when the ``afs_install_method`` is ``source``.

  Default: ``git://git.openafs.org/openafs.git``

afs_git_version
  The git branch or tag to check out and build when the ``afs_install_method`` is ``source``.

  Default: ``master``

afs_gerrit_host
  The gerrit hostname when ``afs_checkout_method`` is ``gerrit``.

  Default: ``gerrit.openafs.org``

afs_gerrit_number
  The gerrit number to be fetched when ``afs_checkout_method`` is ``gerrit``.  The most
  recent patchset is fetched.  This variable is manditory when ``afs_checkout_method`` is
  ``gerrit``.

afs_configure_options
  Overrides the options given to configure when building from source.
  This variable can be a simple string, such as ``"--enable-debug
  --enable-transarc-paths"``, or may be specified as a dictionary, for example:

.. code-block:: yaml

    afs_configure_options:
      prefix: /usr
      bindir: /usr/bin
      libdir: /usr/lib64
      sbindir: /usr/sbin
      disable:
        - strip_binaries
        - kernel_module
      enable:
        - debug
        - redhat_buildsys
        - transarc_paths
      with:
        - krb5: /path/to/krb5.lib

  Default: detected, platform dependent

afs_nolibafs_configure_options
  Overrides the `configure` arguments whe building the userspace binaries
  from source (no kernel module).  This variable can be a simple string,
  such as ``"--enable-debug --enable-transarc-paths"``, or may be specified
  as a dictionary.

  Default: detected, platform dependent

afs_always_build
  When the ``afs_install_method`` is ``sdist`` or ``source``, force a rebuild
  and reinstall even if a change in the source code checkout was not detected.

  Default: no

afs_clean_build
  When the ``afs_install_method`` is ``sdist`` or ``source``, clean any build
  artifacts that may be left from a previous build. Set to no to let make only
  rebuild binaries which are out of date with the sources, which should be
  faster when rebuilding the same branch as the previous build.

  Default: yes
