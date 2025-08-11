# Saúde Fácil
#Em construção
Sistema web para gerenciamento de consultas médicas, prescrições, histórico e agenda, desenvolvido em Django.

## Tecnologias Utilizadas

<table>
  <tr>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" alt="Python"/><br>Python
    </td>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg" width="40" alt="Django"/><br>Django
    </td>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" width="40" alt="HTML5"/><br>HTML5
    </td>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" width="40" alt="CSS3"/><br>CSS3
    </td>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" width="40" alt="JavaScript"/><br>JavaScript
    </td>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg" width="40" alt="Bootstrap"/><br>Bootstrap
    </td>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg" width="40" alt="SQLite"/><br>SQLite
    </td>
    <td align="center">
      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg" width="40" alt="Linux"/><br>Linux
    </td>
  </tr>
</table>

## Funcionalidades

- **Agenda de Consultas:**  
  Visualize próximas consultas, agende novas, veja detalhes e cancele agendamentos.

- **Prescrições e Atestados:**  
  Gerencie prescrições médicas e emita atestados.

- **Histórico de Consultas:**  
  Consulte o histórico completo de atendimentos.

- **Gerenciamento de Horários:**  
  Defina e edite disponibilidade de horários para médicos.

- **Configurações:**  
  Altere senha e preferências do usuário.

## Estrutura do Projeto

```
Projeto_saude_facil/
├── tela_principal/
│   ├── migrations/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   │   └── tela_principal/
│   │       ├── base_interna.html
│   │       └── agenda/
│   │           └── agenda.html
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── manage.py
└── README.md
```

## Como Executar

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Realize as migrações:**
   ```bash
   python manage.py migrate
   ```

3. **Crie um superusuário (opcional):**
   ```bash
   python manage.py createsuperuser
   ```

4. **Inicie o servidor:**
   ```bash
   python manage.py runserver
   ```

5. **Acesse no navegador:**
   ```
   http://localhost:8000/
   ```

## Organização dos Templates

- **base_interna.html:**  
  Template base para páginas internas, inclui menu, mensagens e área de conteúdo.

- **agenda/agenda.html:**  
  Página de agenda de consultas, exibe consultas do banco de dados.

## Contribuição

1. Fork este repositório
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas alterações (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.

---

**Saúde Fácil** &copy; {% now "Y"
