# SDS_Grupo06_Goncalo_Eliaquim_Assignment_3
Repositório para submissão. Trabalho realizado no âmbito da cadeira Sistemas Distribuídos e Segurança, atividade laboratorial nº 3

Considerações:

A base de dados será criada automaticamente no diretório raiz do projeto (onde se executa "init_db.py").
No entanto, nenhum utilizador (ou admin, para esse efeito) é criado de forma imediata.

O ficheiro "create_user.py" serve exatamente para isso, e deve ser alterado de acordo com as preferências do individuo que deseja recriar o projeto.


Para instalar as dependências deve correr-se o comando :

>>pip install -r requirements.txt

No entanto, é possível que o software "pip" (Package Management System do Python) não esteja previamente instalado. Para isso serve o ficheiro ".env".

Selecionando o mesmo como interpretador, canto inferior direito no Visual Studio Code, todas as dependências e libs necessárias para a realização do projeto/mencionadas no código fonte passarão a ser reconhecidas pelo terminal. Trata-se de um ambiente virtual no qual o projeto pode correr sem falta de recursos.

Podem retirar-se algumas linhas do código fonte, principalmente da natureza destas:

>>
import os
import sys

##Adiciona o diretório raiz do projeto ao sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)
<<

A razão pela qual estão presentes é para garantir que, ao correr certos ficheiros, o Python encontra sempre os módulos necessários para o fazer.
Não estando no diretório correto, o administrador recebe o erro "ModuleNotFoundError:".

