# NAPP Academy 2023 - 1º Bimestre (Nós Vamos Invadir sua Praia) 🌴
Projeto desenvolvido para o primeiro bimestre do curso de 'Projetos em Python'.

[![NPM](https://img.shields.io/npm/l/react)](https://github.com/rafael-piress/Napp_Academy_2023_1_Bimestre/blob/main/LICENCE) 


# Tecnologias utilizadas
- Python;
- Banco de dados: Postgresql.
 
  <h3>Tópicos que serão encontrados nesse repositório<br></h3>
  • Códigos desenvolvidos em Python;<br>
  • Testes desenvolvidos baseados na Framework Pytest;<br>
  • Utilização do paradigma de programação OO (Object-oriented);<br>
  
## Escopo  
 Paulo Pena, vulgo 'Paulão', é proprietário de quatro quadras de Beach Tennis e o objetivo proposto para o projeto foi a criação de um programa que auxiliasse o 'Paulão' na organização dos clientes e disponibilidade das respectivas quadras para locação, por horário específico.

  O empreendimento do Paulão funciona de terça à sábado, entre 10hs e 22hs e aos domingos, entre 9hs e 18hs. Cada quadra possui uma agenda de locação e cada cliente, identificado por nome e telefone pode agendar a quadra por blocos de uma e três horas.

  O programa foi criado para rodar em CLI (_Command Line Interface_) e sendo Paulão o único usuário, não foi necessário criar um sistema de controle de usuário. As informações de agendamento são armazenados em um banco de dados estruturado de forma não relacional e o sistema projetado permite a inclusão de novos clientes, gestão dos horários disponíveis e locados, desistência, saldo devedor e a geração de relatório.
 
## No sistema é possível encontrar:
 •	Estrutura para as entidades que se relacionam no sistema; <br> 
 •	Interação entre diferentes objetos para integração do sistema; <br>
 •	Agendamento de horário de quatro quadras diferentes em 7 dias diferentes com 12 horários cada; <br>
 •	Exclusão de agendamento com avalização do horário em específico; <br>
 •	Cadastro de cliente e atribuição imediata de horário se assim ser necessário; <br>
 •	Banco de dados em PostgreSQL que armazena os dados com nível superior a terceira Forma Normal; <br>
 •	Alto nível de abstração do banco de dados; <br>
 •	Testes que asseguram os outputs e funcionalidades das estruturas; <br>

## Configurações
\* Instale os pacotes necessários por meio do comando `pip install -r requirements.txt` <br>
\* Execute o arquivo principal `python main.py` <br> 
\* Navegue no sistema por meio das configurações ancoradas no menu que aparecerá <br> 
### Testes
\* Entre no diretório em que está contido o arquivo principal `main.py` e execute o comando `pytest`

## Contribuidores

<table>
  <tr>
    <td align="center"><a href="https://github.com/Attenuare"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/102560265?v=4" width="100px;" alt=""/><br /><sub><b>Leandro Alves</b></sub></a><br /><a href="https://github.com/Attenuare" title="Attenuare's Cafeteria">☕</a></td>
    <td align="center"><a href="https://github.com/PedNeto"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/102253548?v=4" width="100px;" alt=""/><br /><sub><b>Pedro Rufino</b></sub></a><br /><a href="https://github.com/PedNeto" title="(Nós Vamos Invadir sua Praia)">🌴</a></td>
    <td align="center"><a href="https://github.com/pie172"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/103082349?v=4" width="100px;" alt=""/><br /><sub><b>Pietra Alves</b></sub></a><br /><a href="" title="(Nós Vamos Invadir sua Praia)">🌴</a></td>
  </tr>
      <td align="center"><a href="https://github.com/rafael-piress"><img style="border-radius: 50%;" src="https://ca.slack-edge.com/T1Q8S1AN8-U030FGEQG1K-a9ec8b725ccb-512" width="100px;" alt=""/><br /><sub><b>Rafael Pires</b></sub></a><br /><a href="" title="(Nós Vamos Invadir sua Praia)">🌴</a></td>
  </tr>
</table>
