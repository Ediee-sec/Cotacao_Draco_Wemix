## Programa de cotação da criptoema NFT Draco

* ### *Contexto da aplicação:*

**Baseado na quantidade de draco informada pelo usuário, faz o calculo e retorna quanto ganharia em <span style="color:red">Reais,Wemix,Klay e Bitcoin</span>**

**Outra Funcionalidade interessante é o valor de cada moeda atualiaza na barra superior**

**Possui também a quantidade prevista de fechamento das moedas <span style="color:red">Draco</span> e <span style="color:red">Wemix</span> as 00:00**


<img src = img_md/img.png>

****

 ### *Mapa do código:*
****
1. **Bibliotecas Python/ Comandos**

```Python
from audioop import add
import requests
from PyQt5 import uic, QtWidgets
import string
```
****
2. **Classe que irá fazer a integração entre o programa e a API do Draco**
```Python
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
```
****
3. **Classe que faz a integração entre o programa e a cotação atualizada do dolar para reais e bitcoin**
```Python
class cCotacao():
    def __init__(self):
        self.url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
        self.response = requests.request("GET", self.url)
        self.ctDicionario = self.response.json()
        self.pDolar = self.ctDicionario["USDBRL"]['bid']
        self.pEuro = self.ctDicionario["EURBRL"]['bid']
        self.pCoin = self.ctDicionario["BTCBRL"]['bid']
        
rDeb = cCotacao()
```
****
4. **Classe responsável por fazer a conversão do valor em String Para Float**
*Observe que a ultima instância eu não faço essa convensão neste momento, ma a frnte irei explicar o porque*
```Python
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
```
****
5. **Métodos da Classe <span style = "color:purple">sConv()</span>, Responsáveis por fazer o calculo que retorna o valor base das Moedas**
*Estas informações ficam no canto superior da tela*

```Python
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
```
****
6. **Funções sem Classe, depois de fazer os calculos em <span style = "color:blue">Float</span>, aqui eu converso novamente para <span style = "color:blue">String</span>**
*Por padrão a tela do PyQt5 o método **setText** aceita apenas entradas em String se eu passar um valor em float para este metodo irá dar erro em tempo de execução*
*A Função **<span style = "color:Purple">fPadrao()</span>** é respinsável por criar a formatação correta para todas as outras funções abaixo*

```Python
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
```

****

7. **Funções responsáveis por capturar o valor digitado de Draco e chamar os Métodos da classe <span style = "color:purple">sConv()</span>**
*Estas informações ficam no canto superior da tela*

```Python
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
```
****

8. **Função responsável por toda vez que o usuário clicar em atualizar, ela irá refazer os valores nos campos das Moedas, com base no valor de Draco informado, está função também chama as funções acima**

```Python
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
```
****
9. **Bloco de código reponsável por chamar as funções corretas para imprimir o valor na tela, este bloco referencia-se as cotações no canto superior da tela**

```Python
interface.val_draco.setText(strDraco())
interface.val_wemix.setText(strWemix())
interface.val_klay.setText(strKlay())
interface.val_dolar.setText(strDolar())
interface.prev_draco.setText(prevDraco())
interface.prev_wemix.setText(prevWemix())
interface.toolButton.clicked.connect(aCampos) #Botão de Atualizar
```
****

10. **Carrega a tela grafica do programa**

```Python
app = QtWidgets.QApplication([])
interface = uic.loadUi("interface.ui")
interface.show()
app.exec()
```
****

* ### UPDATES

AUTHOR | DATA | HORARIO | LINHAS |
:--------- | :-------: | -------: | --------:
Emerson Pereira | 18/01/2022 | 00:23 | EX:Linha 50 a 55 (ALTER)

****

* ### Redes Sociais
<https://www.linkedin.com/in/emerson-santos-9358041b7/>
