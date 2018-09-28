# to engage the awesome

just run install.sh

sshow shows your configured ssh hosts

```
sshow pp
```

```
AWSEC2-hopmedia-ceb-pp
AWSEC2-hopmedia-colas-pp
AWSEC2-hopmedia-ekopdm-pp
AWSEC2-hopmedia-hgi-pp
AWSEC2-hopmedia-primagaz-pp
AWSEC2-hopmedia-saf-pp
```

Now pipe that to nssh which runs your command on all servers, sequentially

```
sshow pp | nssh ls
```

```
sshow pp | nssh ls
AWSEC2-hopmedia-ceb-pp
-------------------------------------
conf
install_hopmedia.sh
nohup.out
primagaz


AWSEC2-hopmedia-colas-pp
-------------------------------------
colas
COLAS
colas_prod
conf
install_hopmedia.sh
sashimi-collector-aws_2.1.ubuntu16.04_noarch.deb

```

Same thing for scp with nscp

```
sshow pp | nscp my_file.txt
```


# Timeouts

nscp and nssh timeout after 15 seconds if the remote server does not respond =)
To alter this timeout, modify NSSH_TIMEOUT environment variable.  To have no timeout, set NSSH_TIMEOUT to  0 or lower


