<h1 align="center" style="font-weight: bold;">MIVT 💻</h1>

<p align="center">
 <a href="#technologies">Technologies</a> • 
 <a href="#started">Getting Started</a> • 
  <a href="#routes">API Endpoints</a> •
 <a href="#colab">Collaborators</a> •
 <a href="#contribute">Contribute</a>
</p>

<p align="center">
    <b>A dynamic and user-friendly web application simulating an e-commerce platform for accessories, providing functionalities for both merchants and customers.</b>
</p>

#### Video Demo: <https://youtu.be/6bTmQTbUXRc>
 
<h2 id="technologies">💻 Technologies</h2>

- Python
- HTML/CSS
- Flask – Backend framework
- SQLite – Database system

<h2 id="started">🚀 Getting started</h2>

<h3>Prerequisites</h3>

- Python
- Flask (via pip install flask)
- CS50 package

<h3>Cloning</h3>

```bash
git clone https://github.com/emilitabuti/MIVT.git
```

<h3>Starting</h3>

1. Open your terminal or command prompt.
2. Run the following command to install the cs50 package:
   
```bash
  pip install cs50
   ```
3. Navigate to the project folder.
 ```bash
cd mivt
cd mivt
```

3. Run the project:
```bash
flask run --port=5001
```
The app should now be running locally on http://localhost:5001.



<h2 id="routes">📍 API Endpoints</h2>

Here are the main routes of the application and their descriptions:
​
| route               | description                                          
|----------------------|-----------------------------------------------------
| <kbd>GET, POST /</kbd>     | Displays the product catalog 
| <kbd>POST /remover</kbd>     |  Removes a product from the customer's cart 
| <kbd>GET, POST /compra</kbd>    | Completes a customer’s purchase 
| <kbd>GET, POST /login</kbd>     | Logs in a customer 
| <kbd>GET, POST /registro</kbd>     | Registers a new customer 
| <kbd>GET, POST /login_comerciante</kbd>     | Logs in a merchant 
| <kbd>GET, POST /adicionar_produto</kbd>    | Adds new products for a merchant 

<h2 id="colab">🤝 Collaborators</h2>
- Emili Tabuti

<h2 id="contribute">📫 Contribute</h2>

1. `git clone https://github.com/emilitabuti/MIVT.git`
2. `git checkout -b feature/NAME`
3. Follow commit patterns
4. Open a Pull Request explaining the problem solved or feature made, if exists, append screenshot of visual modifications and wait for the review!

<h3>Documentations that might help</h3>

[📝 How to create a Pull Request](https://www.atlassian.com/br/git/tutorials/making-a-pull-request)

[💾 Commit pattern](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)
