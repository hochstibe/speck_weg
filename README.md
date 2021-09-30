# speck_weg
web app

## Installation
### Backend
```
pip install -e .\server\speck_weg_backend
```
* Problems on WSL to install Python3.9 / pip / create a venv
* Pycharm cant use virtual environments on wsl anyways...

### Frontend
* [WSL on Windows](https://docs.microsoft.com/en-us/windows/wsl/install)
* [Node.js on Windows](https://docs.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-windows)
* [Node.js on WSL](https://docs.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-wsl)
* [Vue.js on WSL](https://docs.microsoft.com/en-us/windows/dev-environment/javascript/vue-on-wsl)
* NodeJS / vueJS are usually deployed on Linux systems.
* Use Windows Subsystem for Linux (wsl2)
* Use NodeVersionManager nvm
* [Vue / Flask Tutorial](https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/)
* Try Vue 3.x instead of 2.x (Tutorial)
* Set the terminal in Pycharm to `"C:\Users\stefa\AppData\Local\Microsoft\WindowsApps\ubuntu.exe" run`
```
# wsl
wsl --install -d ubuntu

# open ubuntu terminal in windows terminal
sudo apt-get install curl
# install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash

# install node
nvm install node
nvm install --lts
mkdir speck_weg
cd speck_weg
# use the current node version for the project (not the lts)
nvm use node

# install vue (ubuntu terminal, speck_weg folder)
npm install vue
npm install -g @vue/cli

```

```
# GET -> assumes, that it is a GET request
curl localhost:5000/
# Send Data (POST) -> specify header
curl -d '{json}' -H 'Content-Type: application/json' localhost:5000/
# Force a HTTP verb
curl localhost:5000 -X DELETE
```