class dron:
    def __init__(self,id=None,status="Esperando instruccion",heigth=0,info=None):
        self.status = status
        self.heigth = heigth
        self.info = info
        self.id = id