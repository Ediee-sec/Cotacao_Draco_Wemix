from audioop import add
import requests
from PyQt5 import uic, QtWidgets
import string
class draco():
    def __init__(self):
        self.url = "https://api.mir4global.com/wallet/prices/draco/lastest"
        self.response = requests.request("POST", self.url)
        self.drDicionario = self.response.json()
        self.valorDraco = self.drDicionario['Data']["USDDracoRate"]
        self.valorWemix = self.drDicionario['Data']["USDWemixRate"]
        self.valorKlay = self.drDicionario['Data']["USDKLAYRate"]
        self.VolDraco = self.drDicionario['Data']["DracoAmount"]
        self.prevCloseDraco= self.drDicionario['Data']['USDDracoRatePrev']
        self.prevCloseWemix= self.drDicionario['Data']['USDWemixRatePrev']  
        
rDwk = draco()


class cCotacao():
    def __init__(self):
        self.url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
        self.response = requests.request("GET", self.url)
        self.ctDicionario = self.response.json()
        self.pDolar = self.ctDicionario["USDBRL"]['bid']
        self.pEuro = self.ctDicionario["EURBRL"]['bid']
        self.pCoin = self.ctDicionario["BTCBRL"]['bid']
        
rDeb = cCotacao()

class sConv(draco, cCotacao):
    def __init__(self):
        super().__init__()
        self.fDraco = float(str(rDwk.valorDraco))
        self.fWemix = float(str(rDwk.valorWemix))
        self.fKlay = float(str(rDwk.valorKlay))
        self.fPcDraco = float(str(rDwk.prevCloseDraco))
        self.fPcWemix = float(str(rDwk.prevCloseWemix))
        self.fDolar = float(str(rDeb.pDolar))
        self.fEuro = float(str(rDeb.pEuro))
        self.fBtc = (str(rDeb.pCoin))
    
    def prvD(self, qtd):
        calc = att.fPcDraco * att.fDolar * qtd
        return calc
    
    def prvW(self, qtd):
        calc = att.fPcWemix * att.fDolar * qtd
        return calc
    
    def dracoXdolar(self, qtd):
        calc = att.fDraco * att.fDolar * qtd
        return calc
    
    def wemixXdolar(self, qtd):
        calc = att.fWemix * att.fDolar * qtd
        return calc
    
    def klayXdolar(self, qtd):
        calc = att.fKlay * att.fDolar * qtd
        return calc
    
    def realXdolar(self, qtd):
        calc = att.fDolar * qtd
        return calc
#############################################
    def dracoXwemix(self, tot):
        calc = tot * (att.fDraco / att.fWemix) 
        return calc
    
    def dracoXklay(self, tot):
        calc = tot * (att.fDraco / att.fKlay) 
        return calc
    
    def dracoXreal(self, tot):
        calc = tot * att.fDraco * att.fDolar 
        return calc
    
    def dracoXbtc(self, tot):
        s = att.fBtc
        out = s.translate(str.maketrans('','', string.punctuation))
        numero = int(out)
        calc = (tot * att.fDraco * att.fDolar) / numero 
        return calc
##############################################
att = sConv()

def fPadrao(a):
    resultado = a
    vFormata = f'R$ {resultado:.2f}'
    vFormata = vFormata.replace('.',',')
    return vFormata

def prevDraco():
    qtd = 1.0
    resultado = fPadrao(att.prvD(qtd))
    return resultado

def prevWemix():
    qtd = 1.0
    resultado = fPadrao(att.prvW(qtd))
    return resultado

def strDraco():
    qtd = 1.0
    resultado = fPadrao(att.dracoXdolar(qtd))
    return resultado
    
def strWemix():
    qtd = 1.0
    resultado = fPadrao(att.wemixXdolar(qtd))
    return resultado

def strKlay():
    qtd = 1.0
    resultado = fPadrao(att.klayXdolar(qtd))
    return resultado

def strDolar():
    qtd = 1.0
    resultado = fPadrao(att.realXdolar(qtd))
    return resultado

def tDracoPwemix():
    tot = float(interface.quant_draco.value())
    resultado = att.dracoXwemix(tot)
    return resultado

def tDracoPklay():
    tot = float(interface.quant_draco.value())
    resultado = att.dracoXklay(tot)
    return resultado

def tDracoPreal():
    tot = float(interface.quant_draco.value())
    resultado = att.dracoXreal(tot)
    return resultado

def tDracoPbtc():
    tot = float(interface.quant_draco.value())
    resultado = att.dracoXbtc(tot)
    return resultado

def aCampos():
    interface.dW.setText(str(f'{tDracoPwemix():.2f}'))
    interface.dK.setText(str(f'{tDracoPklay():.2f}'))
    interface.dR.setText(str(f'{tDracoPreal():.2f}'))
    interface.dB.setText(str(f'{tDracoPbtc():.10f}'))
    

app = QtWidgets.QApplication([])
interface = uic.loadUi("interface.ui")
interface.val_draco.setText(strDraco())
interface.val_wemix.setText(strWemix())
interface.val_klay.setText(strKlay())
interface.val_dolar.setText(strDolar())
interface.prev_draco.setText(prevDraco())
interface.prev_wemix.setText(prevWemix())
interface.toolButton.clicked.connect(aCampos)
interface.show()
app.exec()

#print(type(quant()))

#print(type(att.btcXdolar(1)))
#print(f'{att.dracoXdolar(1):.2f}')




