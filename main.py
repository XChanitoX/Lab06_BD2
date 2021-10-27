import nltk
from nltk.stem.snowball import SnowballStemmer
nltk.download('punkt')

NUM_ROOTS = 500
CANT_ARCHIVOS = 7
derivador = SnowballStemmer('spanish')
libros = ['libro1.txt', 'libro2.txt', 'libro3.txt','libro4.txt','libro5.txt','libro6.txt']
tokens = {}
stoplist = []
tokensArchivo = []


def init():
  for archivo in libros:
        with open('Libros/' + archivo, 'r') as file:
            tokensArchivo.append(nltk.word_tokenize(file.read().lower()))
  global stoplist
  with open('stoplist.txt', 'r') as file:
      fileRead = file.read()
      stoplist = fileRead.split('\n')
  stoplist += [',', '.', ';', ':', '(', ')', '«', '»']



def L(token):
    raiz = derivador.stem(token)
    #print("ROOT",root)
    lista = tokens[raiz]
    return lista

def AND(token1, token2):
    archivoA = L(token1)
    archivoB = L(token2)
    countA = countB = 0
    consulta = []
    while countA < len(archivoA) and countB < len(archivoB):
        if archivoA[countA] == archivoB[countB]:
            consulta.append(archivoA[countA])
            countA += 1
            countB += 1
        elif archivoA[countA] > archivoB[countB]:
            countB += 1
        else:
            countA += 1
    return consulta


def OR(token1, token2):
    archivoA = L(token1)
    archivoB = L(token2)
    countA = countB = 0
    consulta = []
    while countA < len(archivoA) or countB < len(archivoB):
        if countA < len(archivoA) and countB < len(archivoB):
            if archivoA[countA] == archivoB[countB]:
                consulta.append(archivoA[countA])
                countA += 1
                countA += 1
            elif archivoA[countA] < archivoB[countB]:
                consulta.append(archivoA[countA])
                countA += 1
            elif archivoA[countA] > archivoB[countB]:
                consulta.append(archivoB[countB])
                countB += 1
        elif countA < len(archivoA) and countB >= len(archivoB):
            consulta.append(archivoA[countA])
            countA += 1
        elif countA >= len(archivoA) and countB < len(archivoB):
            consulta.append(archivoB[countB])
            countB += 1
    return consulta


def ANDNOT(token1, token2):
    archivoA = L(token1)
    archivoB = L(token2)
    countA = countB = 0
    for token in archivoB:
      archivoA.remove(token)
    return archivoA

init()
tokensTemp = tokensArchivo

tokenTotal = []
for tokens_in_file in tokensTemp:
    tokens_cur = []
    for token in tokens_in_file:
        root = derivador.stem(token)
        if root not in stoplist:
            if root not in tokens_cur:
                tokens_cur.append(root)
            if root not in tokens:
                tokens[root] = 1
            else:
                tokens[root] += 1
    tokenTotal.append(tokens_cur)

tokens = dict(sorted(tokens.items(), key=lambda x: x[1], reverse=True))
tokens = dict(list(tokens.items())[:NUM_ROOTS])
tokens = dict(sorted(tokens.items(), key=lambda x: x[0]))

tokens_old = tokens
tokens = {}

for token in tokens_old:
    files = []
    for i in range(1, CANT_ARCHIVOS):
        if token in tokenTotal[i-1]:
            files.append(i)
    tokens[token] = files


print(OR('trop', 'ungol'))