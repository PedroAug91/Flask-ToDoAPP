# Flask ToDo Web App
Este projeto foi criado e desenvolvido para fins de aprendizado pessoal. 

## Descrição
Esta é uma aplicação de gerenciamento de tarefas simples utilizando o framework Flask da linguagem Python.

## Funcionalidades
- **Autenticação**: O usuário pode criar uma nova conta ou entrar em uma já existente.
- **Criar tarefas**: O usuário pode criar novas tarefas se estiver logado.
- **Alternar status das tarefas**: O usuário pode alternar entre o status de "ativo" ou "concluídas".
- **Deletar tarefas**: O usuário pode deletar permanentemente uma tarefa.

## Começando 

### Pré-requesitos

- Python 3.8+
- MySQL

### 

1. Clone o repositório 
    ```
    git clone https://github.com/PedroAug91/Flask-ToDoAPP.git
    ```
2. Instale as dependencias 
    ```
    pip install -r requirements.txt
    ```

### Executando o programa

1. Crie o banco de dados com o script presente no respositório 
2. Execute a aplicação com o flask 
    ```
    flask run 
    ```
    ou

    ```
    flask --debug run
    ```
    caso queira o console de debug
3. Abra a url disponibilizada pelo comando acima no seu navegador

## Ajuda
- Somente é possível executar a aplicação com o comando abaixo se forem retirados os "#" da condicional presente no final do arquivo `app.py`.

    ```
    python app.py
    ```


## Autor

* [@PedroAug91](https://github.com/PedroAug91)

## Referências
Todas as referencias utilizadas para o desenvolvimento do projeto
* [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* [Jinja](https://jinja.palletsprojects.com/en/3.1.x/)
* [HTML](https://www.w3schools.com/html/default.asp)
* [CSS](https://www.w3schools.com/css/default.asp)
* [MySQL](https://www.w3schools.com/mysql/default.asp)
