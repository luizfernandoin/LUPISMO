<h1 align="center">LUPISMO - Compartilhe suas ideias e pensamentos!</h1>
<p align="center">
  <img alt="Versão" src="https://img.shields.io/badge/vers%C3%A3o-1.1.0-blue.svg?cacheSeconds=2592000" />
  <a href="LICENSE" target="_blank">
    <img alt="Licença: MIT" src="https://img.shields.io/npm/l/react" />
  </a>
</p>

## Sumário 
- [Descrição](#descrição)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Contribuidores](#contribuidores)
- [Mostre seu apoio](#mostre-seu-apoio)

## Descrição
Bem-vindo ao LUPISMO!

LUPISMO é uma plataforma de rede social focada em compartilhamento de pensamentos e ideias. Permite aos usuários postarem seus pensamentos, interagirem com outros usuários através de likes, e descobrirem novos conteúdos interessantes.

## Funcionalidades

- 📝 **Postagem de Pensamentos**: Os usuários podem postar seus pensamentos e ideias.

- 👍 **Interatividade**: Os usuários podem curtir pensamentos de outros usuários.

- 👤 **Perfil de Usuário**: Cada usuário possui um perfil onde podem ver suas postagens e informações.

- 🔍 **Busca**: Busca por pensamentos e outros usuários.

- ⏰ **Exibição de Tempo desde a Postagem**: Mostra quanto tempo atrás um pensamento foi postado.


## Instalação
Para usar o LUPISMO localmente, basta clona o repositório usando:
```jsx
// Precisa-se ter o git instalado!
git clone https://github.com/luizfernandoin/LUPISMO
cd lupismo
```
ou baixando um arquivo ZIP do código.

## Configuração
Aqui está um resumo de como configurar o aplicativo:

* **Passo 1** : Crie um ambiente virtual para instalar as dependencias necessárias:
    ```jsx
        python -m venv venv
    ```
    Agora é só ativar:
    ```jsx
        venv\Scripts\activate
    ```

* **Passo 2** : Instale as dependências do requirements.txt:
    ```jsx
        pip install -r requirements. txt
    ```

* **Passo 3** : Altere as variáveis de ambiente necessárias do arquivo .env:

* **Passo 4** : Inicialize o banco de dados:
    ```jsx
        flask db init
        flask db migrate -m ""
        flask db upgrade
    ```

* **Passo 6** : Execute o programa através do seguinte comando:
    ```jsx
        python run.py
    ```


## Tecnologias Utilizadas
* **Backend**: Python, Flask, Socket IO
* **Frontend**: HTML, CSS, JavaScript
* **Banco de Dados**: SQLAlchemy


## Contribuidores

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="25%"><a href="https://github.com/luizfernandoin"><img src="https://avatars.githubusercontent.com/u/106038535?v=4?s=60" width="60px;" alt="Luiz"/><br /><sub><b>Luiz Fernando</b></sub></a><br /><a href="https://github.com/luizfernandoin/NewSpace/commits?author=luizfernandoin" title="Documentation">💻</a></td>
    </tr>
  </tbody>
</table>

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests ou relatar problemas.

1. Faça um fork do projeto.
2. Crie uma branch para sua modificação (git checkout -b feature/nova-feature).
3. Faça commit das suas alterações (git commit -am 'Adiciona nova feature').
4. Faça push para a branch (git push origin feature/nova-feature).
5. Abra um pull request.

## Mostre seu apoio
Dê uma ⭐️ se este projeto ajudou você!