# `sshow`: turn your ssh config into a catalog, ready to multiplex

You have ssh configuration on your machine that you use to access your favorite servers.  You might even have a __lot__ of servers scattered across different projects, with different naming schemes.  `sshow` and its associated commands, `nssh` and `nscp` are here you help you navigate your ssh configuration and easily send one-off commands to groups of servers.

# Installation

Install for your user

`make install`

Install system wide in /usr/bin

`sudo make install`

Install in developer mode (symlinks to files in this repo)

`make install_dev`


# Usage

Let's say your ssh config looks something like this:

```
Host clientA-projecta-server1
Host clientA-projecta-server2
Host clientB-projecta-server1
Host clientB-projecta-server2
Host clientB-projectB-server1
Host clientB-projectB-server2
Host awesomeproject-server1

```

`sshow` by its self just shows your entire config

```
$ sshow 

clientA-projecta-server1
clientA-projecta-server2
clientB-projecta-server1
clientB-projecta-server2
clientB-projectB-server1
clientB-projectB-server2
awesomeproject-server1
```

Naturally, you can filter 

```
$ sshow  server2

clientA-projecta-server2
clientB-projecta-server2
clientB-projectB-server2
```

`grep can also filter, but you already knew that`

# Multiplexing with `nssh`

Simply pipe `sshow` to `nssh` which runs your command on all servers, sequentially.  Note that aren't interactive shells, any interactive prompts will hang (think `apt install` without `-y`).


```
sshow server2 | nssh ls
clientA-projecta-server2
-------------------------------------
conf
nohup.out
.bashrc


clientB-projecta-server2
-------------------------------------
cruft.txt

....

```

# `nscp` 

Same thing for scp with `nscp`

```
sshow server2 | nscp my_file.txt
```

`nscp` will always scp to the home dir on the remote server.  If you want something better, open an issue (or use ansible)


# Timeouts

`nscp` and `nssh` timeout if the command takes more than 15 seconds to complete on the remote server, (or if the remote server does not respond)
To alter this timeout, modify NSSH_TIMEOUT environment variable, or set the `--timeout` argument.  A timeout of 0 equals no timeout.

`sshow server2 | nssh ls --timeout 0` # will never timeout

# Just SSH interactively into first result

If you want to just ssh into the first result, add the word `go` to the end of the command


```
$ sshow projectB go

sshing into clientB-projecta-server1...

...

```


