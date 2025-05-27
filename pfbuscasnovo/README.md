# Instruções de Uso - PFBuscas

## Sobre o Sistema
O PFBuscas é um sistema completo para consulta de dados por CPF, com interface personalizada, sistema de autenticação e histórico de buscas. O sistema foi desenvolvido com Flask no backend e HTML/CSS/JavaScript no frontend.

## Características Principais
- Sistema de cadastro e login de usuários
- Consulta de CPF via API externa
- Exibição organizada dos dados retornados
- Personalização de temas e cores
- Histórico de consultas realizadas
- Interface responsiva para desktop e mobile
- Logo exclusiva inspirada na Polícia Federal

## Acesso ao Sistema Online
O sistema está disponível temporariamente no seguinte endereço:
https://5000-ijpukfa7ozio3j4fut5ae-c5d42775.manusvm.computer

## Instruções para Instalação Local

### Requisitos
- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)

### Passos para Instalação

1. Descompacte o arquivo `pfbuscas.zip` em uma pasta de sua preferência

2. Crie um ambiente virtual Python:
```
python -m venv venv
```

3. Ative o ambiente virtual:
   - No Windows: `venv\Scripts\activate`
   - No Linux/Mac: `source venv/bin/activate`

4. Instale as dependências:
```
pip install -r requirements.txt
```

5. Execute o aplicativo:
```
python -m src.main
```

6. Acesse o sistema no navegador:
```
http://localhost:5000
```

## Funcionalidades

### Autenticação
- Cadastro de novos usuários com nome, email e senha
- Login com validação de credenciais
- Proteção de rotas para usuários autenticados

### Consulta de CPF
- Busca de dados por CPF em API externa
- Exibição organizada dos resultados
- Tratamento de erros e validações

### Personalização
- Escolha entre tema claro e escuro
- Personalização das cores primária e secundária
- Visualização em tempo real das alterações

### Histórico
- Registro de todas as consultas realizadas
- Possibilidade de repetir consultas anteriores

## Estrutura do Projeto
- `src/main.py`: Arquivo principal do aplicativo Flask
- `src/templates/`: Templates HTML para as páginas
- `src/static/`: Arquivos estáticos (CSS, JS, imagens)
- `src/models/`: Modelos de dados
- `src/routes/`: Rotas e controladores

## Customização Adicional
Para personalizar ainda mais o sistema, você pode:
- Modificar os templates HTML em `src/templates/`
- Alterar os estilos CSS em `src/static/css/style.css`
- Adicionar novas funcionalidades no arquivo `src/main.py`

## Suporte
Para qualquer dúvida ou problema, entre em contato com o desenvolvedor.

---

Aproveite o PFBuscas!
