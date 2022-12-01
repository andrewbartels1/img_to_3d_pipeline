# 2d 3d Pipeline Project Repo

taking images and 3d models, and making sense of it all.

This repo is the final result of many hours of hard work for a class project in CS 6743 at [Georgia Tech M.S. Data Analytics](https://catalog.gatech.edu/programs/analytics-ms/)

<!-- ![Demo Gif](images/demo.gif) a gif of it working once it's done! -->

## Setup and Introduction

`im23D_pipeline` can be pip installed as well. (this is mostly in progress)

### Development Environment

To install the `conda` environment and the `jupyter` kernel with the full development environment,
clone the repo and run: 

```bash
$ cd ~/dev-or-some-folder/im23D_pipeline
$ bash install.sh
$ conda activate im23D_pipeline
$ bash install_pytorch3d.sh
```

To uninstall the environment and kernel run:

```bash
$ cd ~/dev-or-some-folder/im23D_pipeline
$ bash uninstall.sh
```

**_NOTE:_** Depending on the platform the user is running, pytorch3d might need to be compiled from source. This repo assumes that the user is running on Linux (for right now), if possible, Windows users should setup something like [WSL, with miniconda, and vscode](https://www.bradleysawler.com/engineering/python-conda-wsl-2-ubuntu-setup-on-windows-10/) or [this How-to](https://gist.github.com/kauffmanes/5e74916617f9993bc3479f401dfec7da) 

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.


## License


[MIT](https://choosealicense.com/licenses/mit/) © [Andrew Bartels](https://github.com/andrewbartels1)

