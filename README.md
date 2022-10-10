Research Project Template
=========================

This template provides a starting point for computational research projects.
The aim of this template is to provide a standardized way of working on a project and documenting the work that makes it easily reproducible in the future.
The data in this repository should include all the necessary files, properly configured, to run all of the cases presented in the work, for example to reproduce results in a paper.
The documentation in this repository should provide guidance for every step of the work, from pre-processing, to solving, to post-processing.

Documentation
-------------

The documentation for the project should be written using reStructuredText and the Sphinx package.
This will make the documentation easy to visualize in either PDF or website form so that someone can easily open it and follow the steps in the work.

To generate the documentation, ensure you have a working Python3 installation with `sphinx` and `sphinx-prompt` installed.
Navigate to the `doc/` directory and execute:

```
make html
open build/html/index.html
```

When starting a new project with this template, be sure to adjust the Sphinx `conf.py` file and input the correct project details.

Repository Structure
--------------------

This part of the README should include a description of the repository structure, showing where each case is stored.
For example, a structure diagram could be:

```
project
│   README.md
│
└───case1
│   │   file1.txt
│   │   file2.txt
│   │
│   └───subfolder1
│       │   file11.txt
│       │   file12.txt
│       │   ...
│
└───case2
│    │   file1.txt
│    │   ...
│
└───doc
│    │   index.rst
│    │   ...
```

Adapt this diagram as needed to show how the repository is set up.

Non-Git Files
-------------

Some files are not git-trackable because they are in binary (non-text) form, because they are very large and would consume too much space, or because their raw data is meaningless and would produce unintelligible git diffs.
Be sure to include these files in the `.gitignore` so that they are automatically not synchronized with the repository.
To handle these files, store them somewhere else, such as Google Drive, and then include a bash stript for downloading the data.
An example script is included in the `inputData/` directory called `getData.sh` (the script does not actually work, but has the commands needed for downloading data from Google Drive).
Once the data is downloaded, it should either be automatically moved to the correct directory or remain in the `inputData/` folder and be properly referenced when required.

Dependencies
------------

Each research project may have a unique set of dependencies.
Include them here and note if they are necessary or not.
The order is arbitrary, but if there is a convenient way of ordering them it can be helpful for users.
For this template, we need only:

* Python3
* Sphinx

Contributors
------------

List the contributors to the project here, starting with those who did the most work and decreasing through the list.

* Bernardo Pacini

Additional Notes
----------------

* As the project is ongoing, there may be many added or removed files, bloating the repository's history.
It may be worthwhile working on a `develop` branch and only committing the completed project to `master` once it has reached a mature state.
