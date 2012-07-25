Rebuilding a Fedora system on new hardware
==========================================

Note: this was written for Fedora 17 in July 2012. Who knows what future
versions will bring in terms of system migration utilities...

For a while I've been running my ASUS Zenbook as a combined
gaming/development laptop by running Windows as the base OS and Fedora
under VMWare workstation.

I realised recently that I didn't really care about using it
for gaming any more, so I decided to simplify things
and just run Fedora directly on bare metal
(that decision was simplified by the fact
that the Zenbooks have been out for a while now,
and the open source driver situation is much improved
from what it was at their original release).

Since the "Oh, I forgot to reinstall X" process is rather annoying,
I decided to find a way to relatively quickly build up the
reinstalled system. It turns out there are some rather useful commands
in the ``yum-utils`` package that can be abused for this purpose. It
*is* messing around with debug commands though, so no guarantees that
this won't result in a broken target system (however, the whole point is
to do this when that target system is completely new, so no great loss
if it ends up needing to be reinstalled).

Step 1 was moving the VM to my desktop machine. If this had been
an actual reinstall rather than a virtual to physical migration
I would have instead just copied the various files described
later out to external storage as archive files, and then unpacked those
archives after doing the reinstallation. As it is, ``scp`` and ``rsync``
are my preferred tools.

Step 2 was reinstalling Fedora directly on the Zenbook.
Nothing special there - I used the Fedora 16 live USB I
still had from the original install, then used ``preupgrade``
to bring the system up to Fedora 17. (I considered this easier
than relearning the live USB creation process, but creating a live USB
isn't particularly difficult)

Step 3 was to temporarily allow SSH access to the notebook::

   $ sudo service sshd start
   $ sudo iptables -I INPUT -p tcp --dport 22 -j ACCEPT

I then checked this from the VM running on the destop::

   $ ssh <zenbook>

Step 4 was to ensure the current system was fully up to date and create
a file describing the full package state (for anyone else following
this, don't forget to install the ``yum-utils`` package if it isn't
already installed)::

   $ sudo yum update -y
   $ yum-debug-dump

Step 5 was to ensure the repo config on the bare metal install matched
that on the VM::

   $ scp /etc/yum.repos.d/* root@<zenbook>:/etc/yum.repos.d
   $ scp /etc/pki/rpm-gpg/* root@<zenbook>:/etc/pki/rpm-gpg

Step 6 duplicated my entire home directory, including the dump of the
package state created in Step 4 above::

   $ rsync -avz ~/ <zenbook>:~

Step 7 was to do a quick sanity check that everything was copied over
correctly by running the following three commands that check disk usage on
both machines (the first checks the total usage in your home directory, the
second, the normally visible files and directories, and the last, the
hidden files and directories with a bit of trickery to avoid attempting
to recurse into the parent directory reference stored at ``..``)::

   $ du -hs ~
   $ du -hs ~/*
   $ du -hs ~/.[^.]*

Step 8 was to restore the package state from the old system on the new one::

   $ sudo yum-debug-restore <dump file>

I could probably have just restarted the X server at this point, but I
figured I may as well just restart the whole machine :)

I expect I'll still need a few more tweaks, as I come across any additional
configuration tweaks needed under ``/etc/``, as well reinstallation of any
components that weren't installed using ``yum`` (I don't recall putting
any packages into the system Python with ``pip``, but it's always possible
I have done so and simply forgotten about it.
