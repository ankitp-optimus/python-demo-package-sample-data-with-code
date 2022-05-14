# Introduction
## Goals of this project
This package doesn’t do anything useful. It exists only as a vehicle to demonstrate:
*  how to prepare a Python project that can be uploaded to the
[Python Package Index (PyPI)](https://pypi.org/) as a release, from which it can then be installed on user systems using the
[pip](https://pypi.org/project/pip/) package installer
*  how static text files (for example, templates, sample data, etc.) can be packaged and then—using
`importlib.resources`—referenced and read from their host package or any other package, even if these files don’t
actually reside on the file system (e.g., if they reside in a .zip archive). This is relevant because:
    * [“[T]he PyPA recommends that any data files you wish to be accessible at run time be included **inside the package**.”](https://setuptools.pypa.io/en/latest/userguide/datafiles.html#non-package-data-files)
    * [PEP 302](https://peps.python.org/pep-0302/) added hooks to import from .zip files and Python Eggs.
* use of a `src/` directory intermediate between the project directory and the outermost package directory—with multiple benefits
*  how to install the project in “editable”/“development” mode during development so that you can test the
functionalities that access resources in packages—without having to rebuild and reinstall the package after every change.
* how to use a `__main__.py` file as an entry point to the package, which will execute when the *package* is invoked on
the command line with the `-m` flag (as opposed to executing the module).
* how to tell the `build` mechanism to identify a specific version of Python, e.g., `py39`, in the “Python Tag” in
the file name of the resulting “wheel” (`.whl`) distribution file, so that users will be better informed of the
Python-version requirement before attempting to install the package.

## Python requirement; timeliness
***NOTE: This package requires Python 3.9+.*** This package has been tested only on Python 3.9.12, with pip 22.0.4,
on a Mac (macOS 12.3.1). All citations/quotations to documentation and other sources were valid as of May 1, 2022.

## Terminology
For my use of “project” and “package” (including “import package” and “distribution package”) see Jim Ratliff,
“[Unpacking ‘package’ terminology in Python](https://gist.github.com/jimratliff/fc799e74e8104e6b05e6894ce8555144),” GitHub Gist.

## Resources for topics not well covered here
I will not go into a detailed explanation of many aspects of packaging more generally that are well covered
elsewhere, e.g., the `LICENSE`,  `README`, `pyproject.toml`, and `setup.cfg` files (or why I’m
using `setup.cfg` rather than `setup.py`). For these and other such topics, see for example:
* “[Python Packaging User Guide](https://packaging.python.org/en/latest/),” by the
[Python Packaging Authority](https://www.pypa.io/en/latest/), and in particular
    * the tutorial
“[Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)”
    * § [Configuring metadata](https://packaging.python.org/en/latest/tutorials/packaging-projects#configuring-metadata).
    (“Static metadata (`setup.cfg`) should be preferred. Dynamic metadata (`setup.py`) should be used only as an escape
    hatch when absolutely necessary.”)
    * § “[Including files in source distributions with `MANIFEST.in`](https://packaging.python.org/en/latest/guides/using-manifest-in/#)”
* § “[Configuring setuptools using `setup.cfg` files](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html)”
of the [Setuptools User Guide](https://setuptools.pypa.io/en/latest/userguide/index.html).
* Mark Smith’s presentation at EuroPython 2019: “Publishing (Perfect) Python Packages on PyPi”
([YouTube](https://www.youtube.com/watch?v=GIF3LaRqgXo),
[GitHub](https://github.com/judy2k/publishing_python_packages_talk))
* Vytautas Bielinskas,
“[Build a Python Module and Share it with Pip Install](https://www.youtube.com/watch?v=FkmtmYFTlYE),” YouTube » Data
Science Garage, April 11, 2021.

I’m also not going to address here any issues about testing, as important as they are.

## Problem considered: Reliably accessing resources included in the package
Instead, I focus here on the particular problem, as
[explained by Barry Warsaw at PyCon US 2018](https://www.youtube.com/watch?v=ZsGFU2qh73E):
> Resources are files that live within Python packages. Think test data files, certificates, templates, translation
catalogs, and other static files you want to access from Python code. Sometimes you put these static files in a package
directory within your source tree, and then locate them by importing the package and using its `__file__` attribute. But
this doesn’t work for zip files! 

The previous standard method, `pkg_resources`, is not a great solution:
> You could use `pkg_resources`, an API that comes with `setuptools` and hides the differences between files on the file
system and files in a zip file. This is great because you don't have to use` __file__`, but it’s not so great because
`pkg_resources` is a big library and can have potentially severe performance problems, even at import time. … 

>The biggest problem with `pkg_resources` is that it has import-time side effects. Even if you’re never going to access
your sample data, you’re paying the cost of it because as soon as you import `pkg_resources` you pay this penalty. …
`pkg_resources` crawls over every entry in your `sys.path` and it builds up these working sets and does all this runtime 
work. … If you have a lot on things on your `sys.path`, this can be very, very slow. … 

The better solution is:
> Welcome to `importlib.resources`, a new module and API in Python 3.7 that is also available as a standalone library
for older versions of Python. `importlib.resources` is built on top of Python’s existing import system, so it is very
efficient. 

See also §§ [Accessing Data Files at Runtime](https://setuptools.pypa.io/en/latest/userguide/datafiles.html#accessing-data-files-at-runtime)
of § [Data Files Support](https://setuptools.pypa.io/en/latest/userguide/datafiles.html) of
[Building and Distributing Packages with Setuptools](https://setuptools.pypa.io/en/latest/userguide/index.html) by PyPA:
>Typically, existing programs manipulate a package’s `__file__` attribute in order to find the location of data files.
However, this manipulation isn’t compatible with PEP 302-based import hooks, including importing from zip files and
Python Eggs. It is strongly recommended that, if you are using data files, you should use `importlib.resources` to
access them. 

The following sources explicitly discuss using `importlib.resources` to access resources integrated within a package:
* Barry Warsaw, “Get your resources faster, with `importlib.resources`,”  PyCon US 2018.
([YouTube](https://www.youtube.com/watch?v=ZsGFU2qh73E), [slides](https://speakerdeck.com/pycon2018/barry-warsaw-get-your-resources-faster-with-importlib-dot-resources))
* James Briggs, “How to Build Python Packages for Pip,” YouTube » James Briggs, April 2, 2021.
([GitHub](https://github.com/jamescalam/aesthetic_ascii)) 
* Damien Martin, “[Making a Python Package](https://kiwidamien.github.io/making-a-python-package.html),”
GitHub » kiwidamien. See especially
“[Making a Python Package VI: including data files](https://kiwidamien.github.io/making-a-python-package.html).”

If the advent of `importlib.resources` in Python 3.7 weren’t enough, an additional function, viz., `files()`, was added
in Python 3.9. I rely upon the `files()` function in this package, and for that reason this package requires
Python 3.9.

## Road map for the remainder of this README document

* [`importlib.resources`: Selected basics](#importlibresources-selected-basics)
* [File and directory structure; rationale for `src/` directory](#file-and-directory-structure-rationale-for-src-directory)
* [Noncomprehensive comments on selected elements of project metadata](#noncomprehensive-comments-on-selected-elements-of-project-metadata)
    * Here I address those aspects of the project’s metadata that are particularly relevant to the particular goals of
    this package.
* [Finish development and upload to PyPI](#finish-development-and-upload-to-pypi)
    * Here I walk through—stage by stage, and command by command—the process of:
        * creating a virtual environment,
        * finishing your development in a local “editable” or “development” install,
        * building your project and turning it into a distribution package that can be uploaded to PyPI,
        * uploading it to TestPyPI, 
        * testing your distribution by created a new virtual environment and installing your project from TestPyPI.

# `importlib.resources`: Selected basics
## Background
[`importlib`](https://docs.python.org/3/library/importlib.html), a Python built-in library, appeared in Python 3.1 and
provides the Python 3 implementation of the `import` statement.

Within `importlib`, the module
[`importlib.resources`](https://docs.python.org/3/library/importlib.html#module-importlib.resources) was added in
Python 3.7:
> This module leverages Python’s import system to provide access to resources within packages. If you can import a
package, you can access resources within that package. Resources can be opened or read, in either binary or text mode.
>
>Resources are roughly akin to files inside directories, though it’s important to keep in mind that this is just a
metaphor. Resources and packages do not have to exist as physical files and directories on the file system.

(Note that the
[documentation for `importlib.resources`](https://docs.python.org/3/library/importlib.html#module-importlib.resources)
actually refers readers to the
[documentation for `importlib_resources`](https://importlib-resources.readthedocs.io/en/latest/using.html), which is the
standalone backport of `importlib.resources` for earlier versions of Python, for more information on using
`importlib.resources`.)
## The `files()` function
This demo package calls the
[function `importlib.resources.files(`*`package`*`)`](https://docs.python.org/3/library/importlib.html#importlib.resources.files),
where *`package`* can be either a name or a module object that conforms to the `Package` requirements.The function
returns an instance of abstract base class `importlib.abc.Traversable`. This object has available a subset of
`pathlib.Path` methods suitable for traversing directories and opening files:
* `joinpath(`*child*`)`
* `__truediv__(`*child*`)`
* `name()`
* `is_dir()`
* `is_file()`
* `iterdir()`
* `open(`*mode*`='r',`*\*args*`,`*\*\*kwargs*`)`
* `read_bytes()`
* `read_text(`*encoding=None*`)`

You can specify the location of a resource from (a) the name of the package immediately enclosing the resource and
(b) the name of the resource  by either:

```my_resource_location_as_string = importlib.resources.files('mypackage').joinpath('resource_name')```

or

```my_resource_location_as_string = importlib.resources.files('mypackage') / 'resource_name'```

where the latter corresponds to `__truediv__(`*child*`)` method.

To read the text into a variable:

```text_in_file = my_resource_location_as_string.read_text()```

# This project
## File and directory structure; rationale for `src/` directory
This project has the following initial directory/file structure:
```
├── LICENSE
├── MANIFEST.in
├── README.md
├── pyproject.toml
├── setup.cfg
├── docs
├── src
│   ├── demo_package_and_read_data_files
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── constants.py
│   │   ├── example.py
│   │   ├── sample_data
│   │   │   ├── __init__.py
│   │   │   └── sample_data_e.txt
│   │   └── sample_data_pi.txt
└── tests
```
By “initial directory/file structure,” I acknowledge that additional directories will be generated as a result of
(a) creating a virtual environment, which adds a `venv/` directory, (b) installing the project in an
“editable”/“development” mode, which adds a `src/demo_package_sample_data_with_code.egg-info` directory, and
(c) the `build` process, which adds a `dist/` directory. 

Note the presence of the `src/` directory at the root level of the project directory and which contains the import 
package `demo_package_and_read_data_files`. This structure—the presence of this `src/` directory—is certainly not yet a
standard but is gaining mindshare. I won’t attempt to justify it myself here, but instead I’ll point you to the
following resources:
* § “[A simple project](https://packaging.python.org/en/latest/tutorials/packaging-projects/#a-simple-project)” in
PyPA’s tutorial “[Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects)”
* § “[The structure](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure)” in Ionel Cristian Mărieș,
“[Packaging a python library](https://blog.ionelmc.ro/2014/05/25/python-packaging),” ionel’s codelog, September 30, 2019.
    * E.g., the `src/` structure (a) ensures that you test your code from the same working directory that your users
    will see when they install your package, (b) allows simpler packaging code and a simpler `MANIFEST.in`, and
    (c) results in a much cleaner editable install.
* Mark Smith’s presentation at EuroPython 2019: “Publishing (Perfect) Python Packages on PyPi”
([YouTube](https://www.youtube.com/watch?v=GIF3LaRqgXo),
[GitHub](https://github.com/judy2k/publishing_python_packages_talk)), at 26:00:
    * “Here’s why we use the `src/` directory. Our root directory is the directory we’ve been working in. If our code was in
this directory—if we import `helloworld` while running the tests—it would run the code in our current directory. But we
don’t want it to do that. We want it to test installing the package and using the code from there. By having the `src/`
directory, you’re forcing it to use the version you’ve just installed into the versioned environment.”

## Noncomprehensive comments on selected elements of project metadata
Without going generally in how to prepare the various metadata files, here I highlight particular ways in which
particular files must be changed or created so that our data files will be properly packaged.

### The directory that immediately encloses each resource must be a package and thus must have an `__init__.py` file
`importlib.resources` considers a file a resource only if the file is in the root directory of a package. A directory
cannot be a package unless it includes a `__init__.py` file. (It’s fine if this `__init__.py` file is empty. It’s its
filename that counts.)

Here the relevant resources are two text files:
* "sample_data_pi.txt"
    * located at the root of the import package, i.e.,
    * src/demo_package_and_read_data_files/sample_data_pi.txt
* "sample_data_e.txt"
    * located within a subfolder, "sample_data", of the import package, i.e.,
    * src/demo_package_and_read_data_files/sample_data/sample_data_e.txt

(Soley to demonstrate throwing a `FileNotFoundError` exception, `example.py` also attempts to open `meaning_of_life.txt`,
but, unsurprisingly, it does not exist.)

In our case the requirement that each data file be in the root directory of a package  means that the following
directories each must have an `__init__.py` file:
*  `src/demo_package_and_read_data_files`
    * This directory would have been a package (and thus would have had an `__init__.py` file) even if we had no data
    files to worry about, so no additional `__init__.py` file is created for this directory on account of the data
    files.
*  `src/demo_package_and_read_data_files/sample_data`
    * This directory is *not* a directory of Python files, so it would not normally have an `__init__.py` file. Thus,
    in order to read the data file from inside, we need to “artificially” add an `__init__.py` file inside.
### Telling `setuptools` about data files that need to be included in the package
`setuptools` will not by default incorporate arbitrary non-Python text files into the package when it builds it. Thus,
you must tell `setuptools` which such files you want it to include.

In the methodology I use here, this requires:
* telling the configuration file `setup.cfg` that you *do* have such files to be included, but not there saying which
ones
* creating a `MANIFEST.in` file that specifies the data files (including their paths) to be included.

(If you’re using a different methodology, like using `setup.py` rather than `setup.cfg`, see the corresponding
discussion at § [Data File Support](https://setuptools.pypa.io/en/latest/userguide/datafiles.html#) of the
[Setuptools User Guide](https://setuptools.pypa.io/en/latest/userguide/index.html).)

#### `setup.cfg`: `include_package_data`
In the configuration file `setup.cfg`, in its `[options]` section, specify:
`include_package_data = True`
#### Create `MANIFEST.in` and itemize the data files
See, generally:
§ “[Including files in source distributions with `MANIFEST.in`](https://packaging.python.org/en/latest/guides/using-manifest-in/#)”
of “[Python Packaging User Guide](https://packaging.python.org/en/latest/).” 

In the present case, the `MANIFEST.in` file contains the following and only the following:
```
include src/demo_package_sample_data_with_code/sample_data_pi.txt
graft src/demo_package_sample_data_with_code/sample_data
```
where `graft` ensures, without itemizing them, that all data files in `/sample_data` are included. (See
§ [`MANIFEST.in` commands](https://packaging.python.org/en/latest/guides/using-manifest-in/#manifest-in-commands) in the
Python Packaging User Guide.)

Thanks to the structure adopted here, where the `src/` directory separates all the project metadata from the project
code/data, the  `MANIFEST.in` perhaps could be made even simpler:
```
graft src
```
which would ensure that all files within `src/` are included in the distribution.
(See [Ionel Cristian Mărieș](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure): “Without `src` writting a `MANIFEST.in` is tricky. … It’s much easier with a `src` directory: just add `graft src` in `MANIFEST.in`.)


### `setup.cfg`: Add a `python-tag` tag to force file name of resulting “wheel” distribution file to reflect partticular minimum version of Python
This discussion will make more sense after you get to the later section § “[The wheel file](#the-wheel-file),” but this discussion
nevertheless logically belongs here.

This package requires Python 3.9. My `setup.cfg` file originally contained the following excerpt:
```
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent

[options]
package_dir =
    = src
packages = find:
python_requires = >=3.9
include_package_data = True
```
However, notwithstanding the `python_requires = >=3.9`, the resulting wheel file’s filename contained a “Python Tag” 
that was simply `py3` rather than `py39` (which would have indicated a minimum Python version of 3.9).

So I next changed the `Python` tag in the `Classifiers` section to explicitly state version 3.9. However, that did not
affect the Python Tag in the file name of the resulting wheel file.

I finally—inspired by [this answer on Stack Overflow](https://stackoverflow.com/a/52613394/8401379)—solved the problem by adding the following section to `setup.cfg`:
```
[bdist_wheel]
python-tag = py39
```
After this change, the file name of the resulting wheel file including the Python Tag string `py39` as I desired.

### Considerations regarding the inter-word separate character in a multiword project name
The `name` field in `setup.cfg` (or `setup.py`) defines the name of your *project* as it will appear on PyPI. ([Examples
will often misleadingly suggest](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html) that this is the
*package* name, in some incompletely specified notion of “package,” but the only effect of this field is to determine the
*project* name on PyPI.)

When, for better readability, you want your project name to have multiple words, you need to have a nonspace delimiter
between these words. However, no matter what delimiter you prefer, e.g., underscore (`_`), hyphen (`-`), or dot (`.`),
PyPI will ignore your expressed intention and “[normalize](https://peps.python.org/pep-0503/#normalized-names)” the name
so that each such delimiter (or even runs of delimiters) is replaced with a single hyphen. So, to avoid confusion, I
suggest that, when the project name has two or more words joined by delimiters, you specify hyphens for the delimiter
from the get go, since that’s the form it will ultimately take.

Of course, you might want the *import package* of your project to have the same name as your project; that’s common.
But if your project has multiple words separted by delimiters, this won’t be exactly possible. The best you could do is
name your import package the same as the project, but substituting an underscore for each delimiter. E.g.,
* Project name: `my-cool-thing`
* Import package name: `my_cool_thing`

### `__main__.py` is executed when package invoked from command line with `-m` flag; allows for a CLI
Although not appropriate in all cases, including a `__main__.py` file establishes an entry point for the case where
the package name is invoked directly from the command line with the `-m` flag, e.g.,:
```
python -m demo_package_and_read_data_files
```
(Note that the import package name, `demo_package_and_read_data_files` must use underscores as the inter-word delimiter,
even though the project name uses hyphens for the delimiter.)

(In general, the `-m` flag
[tells Python to search `sys.path` for the named module and execute its contents as the `__main__` module](https://docs.python.org/3/using/cmdline.html#cmdoption-m). Since the argument is a module name, you must not give a file extension (.py). What’s crucial
for us here is that package names (including namespace packages) are also permitted. When a package name is supplied
instead of a normal module, the interpreter will execute `<pkg>.__main__` as the main module.)

Thus the user can simply reference the package rather than a particular module within the package.

This can also be combined with reading additional arguments entered on the command line.

See § “[`__main__.py` in Python Packages](https://docs.python.org/3/library/__main__.html#main-py-in-python-packages)”
in “[`__main__` — Top-level code environment](https://docs.python.org/3/library/__main__.html),” docs.python.org.

Note that [the contents of `__main__.py` typically aren’t fenced with `if __name__ == '__main__'` blocks](https://docs.python.org/3/library/__main__.html#id1).

Loosely, `__main__.py` is to a package what a `main()` function is to a console script. (E.g., “[main functions are often used to create command-line tools by specifying them as entry points for console scripts](https://docs.python.org/3/library/__main__.html#packaging-considerations).”)

# Finish development and upload to PyPI
Here I walk through—stage by stage, and command by command—the process of:
* creating a virtual environment,
* finishing your development in a local “editable” or “development” install,
* building your project and turning it into a distribution package that can be uploaded to PyPI,
* uploading it to TestPyPI, 
* testing your distribution by created a new virtual environment and installing your project from TestPyPI.


A full transcript (where only some of the output is condensed) of this process is available at: [docs/Transcript_of_installation_and_testing.txt)](https://github.com/jimratliff/python-demo-package-sample-data-with-code/blob/main/docs/Transcript_of_installation_and_testing.txt).

## Create a virtual environment
From here on, I’m assuming that you’re using a virtual environment. I use
[venv](https://docs.python.org/3/library/venv.html), noting that, per the Python Packaging User Guide
(§ “[Installing packages using pip and virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)”):
“If you are using Python 3.3 or newer, the `venv` module is the preferred way to create and manage virtual
environments.”

Generally, see:
* [§ 12. Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html) of Python Docs.
* Brett Cannon, “[A quick-and-dirty guide on how to install packages for Python](https://snarky.ca/a-quick-and-dirty-guide-on-how-to-install-packages-for-python/),” *Tall, Snarky Canadian*, January 21, 2020. Though not
signaled by its title, there is substantial discussion of the why and how of using a virtual environment.

## Install the project in “editable mode”/“development mode” in order to test and further develop it
When still developing the package, and before ever publishing it to PyPI (or even TestPyPI), we want to install the
package from the local source (and therefore *not* from PyPI). Moreover, we do so in “editable mode,” which is
essentially “[setuptools develop mode](https://setuptools.pypa.io/en/latest/userguide/development_mode.html).” In this
mode, you continue to work on the code without needing to rebuild and reinstall the project every time you make a
change.

(See generally § “[Local project installs](https://pip.pypa.io/en/latest/topics/local-project-installs/)” in the
[`pip` documentation](https://pip.pypa.io/en/latest/), and in particular
§§ “[Editable installs](https://pip.pypa.io/en/latest/topics/local-project-installs/#editable-installs).”)

To install this package in “editable mode”/“development mode,” we use `pip install` with the `-e` option:
```
python -m pip install -e path/to/SomeProject
```
(See “[‘Editable’ Installs](https://pip.pypa.io/en/stable/cli/pip_install/#editable-installs)” in the
[`pip` » commands » `install` documentation](https://pip.pypa.io/en/stable/cli/pip_install/#).) (Also, here’s
[an argument by Brett Cannon for using `python -m pip install -e .` instead of ` pip install -e .`](https://snarky.ca/why-you-should-use-python-m-pip/).)

As the [documentation](https://pip.pypa.io/en/stable/cli/pip_install/#editable-installs) well explains:
> Editable installs allow you to install your project without copying any files. Instead, the files in the development
directory are added to Python’s import path. This approach is well suited for development and is also known as a
“development installation”.
>
> With an editable install, you only need to perform a re-installation if you change the project metadata (eg: version,
what scripts need to be generated etc). You will still need to run build commands when you need to perform a compilation
for non-Python code in the project (eg: C extensions).

For example, to navigate to the project directory, create and activate a virtual environment, and install the project
in editable mode:
```
% cd path/to/demo_package_and_read_data_files
% python3 -m venv venv
% source venv/bin/activate
% python -m pip install --upgrade pip
% python -m pip install -e .
```
(In the `pip` command the “.” in `pip install -e .` represents the path to the project.) 

Installing in editable mode allows you to edit the code and immediately see the changes without having to rebuild and
reinstall the package.

## Build the distribution package to upload to PyPI
When development matures to the point of having a version of the project you want to distribute via PyPI, the next step is
to generate a [distribution package](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package) for the
project.

### Install `build`
The first step is to install [`build`](https://pypa-build.readthedocs.io/en/stable/index.html) into your virtual environment (or upgrade if it already exists there) with
```
% python -m pip install --upgrade build
```

### Build the distribution
See
§ “[Generating distribution archives](https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives)
of “[Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/),” Python
Packaging User Guide » Tutorials.
```
% cd path/to/demo_package_and_read_data_files
% python -m build
```

This generates a fair amount of output and creates a `dist` directory at the project root, which now contains the 
following two files:
```
demo_package_sample_data_with_code-0.0.1-py39-none-any.whl
demo-package-sample-data-with-code-0.0.1.tar.gz
```
#### The wheel file
The first of these, with the `.whl` extension is a “wheel” file, or
“[built distribution](https://packaging.python.org/en/latest/glossary/#term-Built-Distribution).” It contains files
and metadata that need only to be moved to an appropriate location on the target system in order to be installed.

To better understand the file name of the wheel file (and in particular the
[platform compatibility tags](https://packaging.python.org/en/latest/specifications/platform-compatibility-tags/) after
the version number), see
§ “[File name convention](https://peps.python.org/pep-0427/#file-name-convention)” of
[PEP 427 – The Wheel Binary Package Format 1.0](https://peps.python.org/pep-0427/#file-name-convention), supplemented
by [PEP 425 – Compatibility Tags for Built Distributions](https://peps.python.org/pep-0425/). See also Brett Cannon,
“[The challenges in designing a library for PEP 425 (aka wheel tags)](https://snarky.ca/the-challenges-in-designing-a-library-for-pep-425/),” *Tall, Snarky Canadian*, June 1, 2019.

In the present case:
* `py39`: (“Python Tag”) Iindicates that the package requires Python 3.9.
* `none`: (“ABI Tag,” referring to
[Application Binary Interface](https://en.wikipedia.org/wiki/Application_binary_interface)) Indicates which Python ABI
is required by any included extension modules. `none` “[represent[s] the case of not caring. This is typically seen with py interpreter tags since you shouldn't care about what ABI an interpreter supports if you're targeting just the Python language and not a specific interpreter](https://snarky.ca/the-challenges-in-designing-a-library-for-pep-425/).”
* `any`: (“Platform Tag”) 
#### The source archive
The second of these, with the `tar.gz` extension, is a
“[source archive](https://packaging.python.org/en/latest/glossary/#term-Source-Archive),” that contains raw source code.

You should always upload a source archive and provide built archives for the platforms your project is compatible with.
In this case, our example package is compatible with Python on any platform so only one built distribution is needed.

## Upload the distribution
### Install `twine`
```
% pip install --upgrade twine
```
### `check` your `dist/*` with `twine`
```
% twine check dist/*
Checking dist/demo_package_and_read_data_files-0.0.1-py39-none-any.whl: PASSED
Checking dist/demo_package_and_read_data_files-0.0.1.tar.gz: PASSED
```
### Test with test.pypi.org
#### Upload to test.pypi.org
See “[Using TestPyPI](https://packaging.python.org/en/latest/guides/using-testpypi/#using-test-pypi),” of the Python
Packaging User Guide, PyPA.

```
% twine upload --repository testpypi dist/*
Uploading distributions to https://test.pypi.org/legacy/
Enter your username: myusername
Enter your password: ••••••••
Uploading demo_package_and_read_data_files-0.0.1-py39-none-any.whl
Uploading demo_package_and_read_data_files-0.0.1.tar.gz
View at:
https://test.pypi.org/project/demo-package-and-read-data-files/0.0.1/
```

#### Test install the package locally from TestPyPI
When visiting the above link, the page displays a command for installing the package:
```
pip install -i https://test.pypi.org/simple/ demo-package-and-read-data-files==0.0.1
```

##### Create a new directory and corresponding new virtual environment and install package from TestPyPI

```
% cd GitHub_repos 
% mkdir test_package
% python3 -m venv venv
% source venv/bin/activate
% python -m pip install --upgrade pip
% pip install -i https://test.pypi.org/simple/ demo-package-and-read-data-files==0.0.1
        …
        …
Successfully installed demo-package-and-read-data-files-0.0.1
% python -m demo-package-and-read-data-files
No module named demo-package-and-read-data-files
% pip list
Package                          Version
-------------------------------- -------
demo-package-and-read-data-files 0.0.1
pip                              22.0.4
setuptools                       60.10.0

% python -m demo_package_and_read_data_files
I am here, in __main__.py.

# # # # # # # # # # # # # # # 

π: 3.14159265358979323846
e: 2.71828182845904523536

Oops! The data file «meaning_of_life.txt» wasn’t found at this location:
»» /Volumes/Avocado/Users/ada/Documents/GitHub_repos/test_package/venv/lib/python3.9/site-packages/demo_package_and_read_data_files/sample_data/meaning_of_life.txt.
[Errno 2] No such file or directory: '/Volumes/Avocado/Users/ada/Documents/GitHub_repos/test_package/venv/lib/python3.9/site-packages/demo_package_and_read_data_files/sample_data/meaning_of_life.txt'
Meaning of life: I have no clue 🤪

* * * * * * * * * * * * * * * 

```
