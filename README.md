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
* [Node.js on WSL](https://docs.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-wsl)
* [Vue.js on WSL](https://docs.microsoft.com/en-us/windows/dev-environment/javascript/vue-on-wsl)
* NodeJS / vueJS are usually deployed on Linux systems.
* Use Windows Subsystem for Linux (wsl2)
* Use NodeVersionManager nvm
* [Vue / Flask Tutorial](https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/)
* Try Vue 3.x instead of 2.x (Tutorial)
* Set the terminal in Pycharm to `"C:\Users\stefa\AppData\Local\Microsoft\WindowsApps\ubuntu.exe" run`
* [Vue.js](https://v3.vuejs.org/guide)
* [Vue-router](https://router.vuejs.org/guide)
* SPA: Routing is done within the application, not by the server [info](https://next.router.vuejs.org/guide/essentials/history-mode.html#html5-mode)
* Configure the server, to serve index.html, if it can't find any static asset
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
cd documents/speck_weg
# use the current node version for the project (not the lts)
nvm use node

# install vue (ubuntu terminal, speck_weg folder)
npm install vue
npm install -g @vue/cli
vue create client
cd client
npm run serve
# CLI customization -> manually select features
# - Vue Version / Babel / Router / Linter
# - Vue 3.
# - Use history mode for the router
# - linter AirBnB
# --> it creates an app with vue.js and vue-router

```

## Curl
```
# GET -> assumes, that it is a GET request
curl localhost:5000/
# Send Data (POST) -> specify header
curl -d '{json}' -H 'Content-Type: application/json' localhost:5000/
# Force a HTTP verb
curl localhost:5000 -X DELETE
```