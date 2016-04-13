#!/bin/sh

should_add_alias () {
    [ -f $1 ] && ! grep -q theoops $1
}

installed () {
    hash $1 2>/dev/null
}

install_theoops () {
    # Install OS dependencies:
    if installed apt-get; then
        # Debian/Ubuntu:
        sudo apt-get update -yy
        sudo apt-get install -yy python-pip python-dev command-not-found python-gdbm

        if [ -n "$(apt-cache search python-commandnotfound)" ]; then
            # In case of different python versions:
            sudo apt-get install -yy python-commandnotfound
        fi
    else
        if installed brew; then
            # OS X:
            brew update
            brew install python
        else
            # Generic way:
            wget https://bootstrap.pypa.io/get-pip.py
            sudo python get-pip.py
            rm get-pip.py
        fi
    fi

    # theoops requires fresh versions of setuptools and pip:
    sudo pip install -U pip setuptools
    sudo pip install -U .

    # Setup aliases:
    if should_add_alias ~/.bashrc; then
        echo 'eval $(theoops --alias)' >> ~/.bashrc
    fi

    if should_add_alias ~/.bash_profile; then
        echo 'eval $(theoops --alias)' >> ~/.bash_profile
    fi

    if should_add_alias ~/.zshrc; then
        echo 'eval $(theoops --alias)' >> ~/.zshrc
    fi

    if should_add_alias ~/.config/fish/config.fish; then
        theoops --alias >> ~/.config/fish/config.fish
    fi

    if should_add_alias ~/.tcshrc; then
        echo 'eval `theoops --alias`' >> ~/.tcshrc
    fi
}

install_theoops
