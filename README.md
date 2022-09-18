# 📦 toolbox-shortcuts

* [Introduction](#introduction)
* [Use cases](#use-cases)
* [Installation](#installation)
* [How to use](#how-to-use)
    * [Package Manager](#package-managers)
* [How to works](#how-to-works)
* [Limitations](#limitations)
    * [sudo](#sudo)
    * [Installation path](#installation-path)

## 📝 Introduction

The **toolbox-shortcuts** utility maps any executables from a toolbox container to the host and other containers, using symlinks. This helps maintain compatibility with host resources with executables in a container.

More informations about toolbox [here](https://github.com/containers/toolbox).


## 🔀 Use cases

* I created a action in my file manager that uses a ImageMagick scripts installed in my container. Using toolbox-shortcuts, can i just create a symlink to `convert` executable and all goes works normally.

* My IDE - which is installed on the host - requires a `javac` (java compiler) executable in my `$PATH`. In the same way, I can create a symlink with toolbox-shortcuts to provides a `javac` symlink executable in my host system.

## 🔨 Installation

Clone this repository to new folder in `~/.local/opt`:

```
$ git clone https://github.com/RuanKlein/toolbox-shortcuts.git ~/.local/opt/toolbox-shortcuts
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

### Package managers

Package managers like `dnf`, `yum`, `apt`, `apt-get`, `pacman`, `zypper`, also works with symlinks. 

For example, to install `php-cli` from host using `dnf`:
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

### sudo

Executing from `host`, does not work with any symlink created by **toolbox-shortcuts**.

However, package managers can run without sudo. The **toolbox-shortcut-handler** script has a special handle to the package managers.

### Installation path

Can only install in user folder, due to the functioning of the toolbox, which only shares the home folder.