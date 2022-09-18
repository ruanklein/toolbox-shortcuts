# 📦 toolbox-shortcuts

## 📝 Introduction

The **toolbox-shortcuts** utility maps any executables from a toolbox container to the host and other containers, using symlinks. This helps maintain compatibility with host resources with executables in a container.

More informations about toolbox [here](https://github.com/containers/toolbox).


## 🔨 Installation

Clone this repository to new folder in `~/.local/opt`:

```
$ git clone https://github.com/RuanKlein/toolbox-shortcuts.git ~/.local/opt
```

Assuming the `~/.local/bin` folder is in your `$PATH`, create symlink to cli utility:
```
$ ln -s ~/.local/opt/toolbox-shortcuts/toolbox-shortcuts ~/.local/bin
```

**NOTE**: due to how the toolbox works, the **toolbox-shortcuts** only works inside the user's folder.

## 🚀 How to use

Scenario:

* `code` executable in `container1`
* `node` executable in `container2`
* `yarn` executable in `container2`
* `java` executable in `container3`


In terminal:

```
$ toolbox-shortcuts create ~/.local/bin/code container1
Shortcut created: code [ ⬢ container1 ]

$ toolbox-shortcuts create ~/.local/bin/node container2
Shortcut created: node [ ⬢ container2 ]

$ toolbox-shortcuts create ~/.local/bin/yarn container2
Shortcut created: yarn [ ⬢ container2 ]

$ toolbox-shortcuts create ~/.local/bin/java container3
Shortcut created: java [ ⬢ container3 ]
```

Now you can run the `code`, `node`, `yarn`, and `java` from the **host** or from the **container1**, **container2**, or **container3**.

## 📚 How to works

Considering the previous scenario, the symlinks were created in `~/.local/bin`:

```
# From host
$ ls -l ~/.local/bin/{code,node,yarn,java}
~/.local/bin/code -> ~/.local/opt/toolbox-shortcuts/containers/container1
~/.local/bin/node -> ~/.local/opt/toolbox-shortcuts/containers/container2
~/.local/bin/yarn -> ~/.local/opt/toolbox-shortcuts/containers/container2
~/.local/bin/java -> ~/.local/opt/toolbox-shortcuts/containers/container3
```

All containers files are also symlinks:

```
$ ls -l ~/.local/opt/toolbox-shortcuts/containers
~/.local/opt/toolbox-shortcuts/containers/container1 -> ~/.local/opt/toolbox-shortcuts/toolbox-shortcuts-handler
~/.local/opt/toolbox-shortcuts/containers/container2 -> ~/.local/opt/toolbox-shortcuts/toolbox-shortcuts-handler
~/.local/opt/toolbox-shortcuts/containers/container2 -> ~/.local/opt/toolbox-shortcuts/toolbox-shortcuts-handler
~/.local/opt/toolbox-shortcuts/containers/container3 -> ~/.local/opt/toolbox-shortcuts/toolbox-shortcuts-handler
```

 The magic is done by the script **toolbox-shortcut-handler**, which can identify if the execution is being done on the host or in a container. The executable name is used to be called in the correct container.

## ❗ Limitations

**sudo**: does not work with any symlink created by **toolbox-shortcuts** from the  **host**, because the container was created at user level, and *sudo* starts running in at root level.

However, package managers can run without sudo; `dnf`, `yum`, `apt`, `apt-get`, `pacman`, and `zypper`. The **toolbox-shortcut-handler** script has a special handle on package managers.

For example, to install `php` command line utility with `dnf` from **host**:
```
$ toolbox-shortcuts create ~/.local/bin/dnf containername
Shortcut created: dnf [ ⬢ containername ]

$ dnf update
...

$ dnf install php-cli
...

$ toolbox-shortcuts create ~/.local/bin/php containername
Shortcut created: php [ ⬢ containername ]

$ php -v
...
```