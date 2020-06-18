# UFABC Helper
Aplicação web onde o aluno entra com sua ficha de aluno e o sistema retorna o calculo dos coeficientes CR, CA e CP - como o Portal do Aluno faz.
O diferencial da aplicação é que nela o usuário pode inserir as disciplinas que está cursando e simular o cálculo dos coeficientes dependendo da nota dessas disciplinas.

**Demo:** <a href="https://ufabchelper.herokuapp.com/" target="_blank">https://ufabchelper.herokuapp.com</a>

## Configurar ambiente

#### Criar o ambiente virtual, ativá-lo e instalar as dependências do projeto

```bash
sudo pip install virtualenvwrapper
```

Adicionar no final do arquivo “~/.bashrc”
```conf
### Configurando os ambientes virtuais pro Python ###
# Exportando onde os ambientes serão criados.
export WORKON_HOME=~/.virtualenvs
# Rodando o script que prepara os ambientes criados.
source /usr/local/bin/virtualenvwrapper.sh
```

Executar
```bash
source ~/.bashrc
mkvirtualenv --no-site-packages -p /usr/bin/python3 ufabc-helper
git clone git@github.com:williamsenasilva/ufabc-helper.git
cd ufabc-helper
pip install -r requirements
```

## Rodar localmente

#### Habilitar ambiente virtual
```bash
workon ufabc-helper
```

#### Rodar aplicação
```bash
python src/run.py
```
