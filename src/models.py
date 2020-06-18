from database import db

class Disciplina(db.Model):
    __tablename__ = 'disciplina'
    ficha_id = db.Column(db.Integer,db.ForeignKey('ficha.id',ondelete="CASCADE"),primary_key=True)
    codigo = db.Column(db.String(15),primary_key=True)
    ano = db.Column(db.Integer,primary_key=True)
    periodo = db.Column(db.String(1),primary_key=True)
    nome = db.Column(db.String(150))
    creditos = db.Column(db.Integer)
    categoria = db.Column(db.String(100))
    conceito = db.Column(db.String(1))
    situacao = db.Column(db.String(100))

    def verifica_situacao(self):
        if self.conceito in ['A','B','C','D']:
            self.situacao = 'Aprovado'
        elif self.conceito in ['E']:
            self.situacao = 'Disc.Equiv'
        elif self.conceito in ['F']:
            self.situacao = 'Repr.Freq'
        elif self.conceito in ['O']:
            self.situacao = 'Reprovado'
        else:
            self.situacao = '-'

class Ficha(db.Model):
    __tablename__ = 'ficha'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer,primary_key=True,autoincrement=True) 
    coeficiente_cr = db.Column(db.Float,default=0)
    coeficiente_cp = db.Column(db.Float,default=0)
    coeficiente_ca = db.Column(db.Float,default=0)
    total_de_obrigatorias = db.Column(db.Integer,default=0)
    total_de_limitadas = db.Column(db.Integer,default=0)
    total_de_livres = db.Column(db.Integer,default=0)
    creditos_de_obrigatorias = db.Column(db.Integer,default=0)
    creditos_de_limitadas = db.Column(db.Integer,default=0)
    creditos_de_livres = db.Column(db.Integer,default=0)
    meta_das_obrigatorias = db.Column(db.Integer,default=0)
    meta_das_limitadas = db.Column(db.Integer,default=0)
    meta_das_livres = db.Column(db.Integer,default=0)
    curso = db.Column(db.String(150))
    tipos = ['OBRIGATÓRIA','LIMITADA','LIVRE']
    disciplinas = db.relationship('Disciplina',backref='ficha')

    def calcula_coeficientes(self):
        self.creditos_de_obrigatorias = 0
        self.creditos_de_limitadas = 0
        self.creditos_de_livres = 0
        self.total_de_obrigatorias = 0
        self.total_de_limitadas = 0
        self.total_de_livres = 0
        # calcula CP e CR
        peso_do_conceito = 0
        soma_dos_creditos = 0
        soma_da_nota_ponderada = 0
        for disciplina in self.disciplinas:
            if disciplina.conceito in ['A','B','C','D','E'] or disciplina.situacao.lower() in ['aprovado','disc.equiv','apr.s.nota']:
                if (disciplina.categoria.lower().find('obrigatória') > -1):
                    self.creditos_de_obrigatorias = self.creditos_de_obrigatorias + disciplina.creditos
                    self.total_de_obrigatorias += 1
                elif (disciplina.categoria.lower().find('opção limitada') > -1):
                    self.creditos_de_limitadas += disciplina.creditos
                    self.total_de_limitadas += 1
                elif (disciplina.categoria.lower().find('livre escolha') > -1):
                    self.creditos_de_livres += disciplina.creditos
                    self.total_de_livres += 1
            if disciplina.conceito == 'A':
                peso_do_conceito = 4
            elif disciplina.conceito == 'B':
                peso_do_conceito = 3
            elif disciplina.conceito == 'C': 
                peso_do_conceito = 2
            elif disciplina.conceito == 'D':
                peso_do_conceito = 1
            elif (disciplina.conceito == 'F') or (disciplina.conceito == 'O'):
                peso_do_conceito = 0
            if (disciplina.conceito != 'E') and (disciplina.conceito != '-') and (disciplina.conceito != 'I') and (disciplina.categoria != '-'):
                soma_da_nota_ponderada += (peso_do_conceito * disciplina.creditos)
                soma_dos_creditos += disciplina.creditos
        if self.creditos_de_obrigatorias > self.meta_das_obrigatorias:
            self.creditos_de_obrigatorias = self.meta_das_obrigatorias
        if self.creditos_de_limitadas > self.meta_das_limitadas:
            self.creditos_de_limitadas = self.meta_das_limitadas
        if self.creditos_de_livres > self.meta_das_livres:
            self.creditos_de_livres = self.meta_das_livres
        print("creditos_de_obrigatorias = %s"%(self.creditos_de_obrigatorias))
        print("creditos_de_limitadas = %s"%(self.creditos_de_limitadas))
        print("creditos_de_livres = %s"%(self.creditos_de_livres))
        print("meta_das_obrigatorias = %s"%(self.meta_das_obrigatorias))
        print("meta_das_limitadas = %s"%(self.meta_das_limitadas))
        print("meta_das_livres = %s"%(self.meta_das_livres))
        print("coeficiente_cp = %s"%(self.coeficiente_cp))
        self.coeficiente_cp = (self.creditos_de_obrigatorias + self.creditos_de_limitadas + self.creditos_de_livres) / (self.meta_das_obrigatorias + self.meta_das_limitadas + self.meta_das_livres) 
        print("coeficiente_cp = %s"%(self.coeficiente_cp))
        self.coeficiente_cr = soma_da_nota_ponderada / soma_dos_creditos 
        # calcula CA
        soma_dos_creditos = 0
        soma_da_nota_ponderada = 0
        disciplinas_ca = []
        for disciplina in self.disciplinas:
            busca_por_nota_maior = False
            for disciplina_aux in self.disciplinas:
                if (disciplina.nome.upper() == disciplina_aux.nome.upper()):
                    if (disciplina_aux.conceito < disciplina.conceito) and (disciplina_aux.conceito != 'O') and (disciplina_aux.conceito != 'I'):
                        busca_por_nota_maior = True
            if not busca_por_nota_maior:
                busca_por_mesma_disciplina = False
                for disciplina_ca in disciplinas_ca:
                    if (disciplina.nome.upper() == disciplina_ca.nome.upper()):
                        busca_por_mesma_disciplina = True
                if not busca_por_mesma_disciplina:
                    disciplinas_ca.append(disciplina)
        for disciplina_ca in disciplinas_ca:
            if disciplina_ca.conceito == 'A':
                peso_do_conceito = 4
            elif disciplina_ca.conceito == 'B':
                peso_do_conceito = 3
            elif disciplina_ca.conceito == 'C': 
                peso_do_conceito = 2
            elif disciplina_ca.conceito == 'D':
                peso_do_conceito = 1
            elif (disciplina_ca.conceito == 'F') or (disciplina_ca.conceito == 'O'):
                peso_do_conceito = 0
            if (disciplina_ca.conceito != 'E') and (disciplina_ca.conceito != '-') and (disciplina_ca.conceito != 'I') and (disciplina_ca.categoria != '-'):
                soma_dos_creditos +=  disciplina_ca.creditos
                soma_da_nota_ponderada += (peso_do_conceito * disciplina_ca.creditos)
        self.coeficiente_ca = soma_da_nota_ponderada / soma_dos_creditos