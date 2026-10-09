palabras_positivas = [
    "feliz", "alegre","contento","excelente","increible","genial",
    "encanto","encanta","bueno","buena","maravilloso","divertido",
    "divertida","amo","ame","recomiendo","espectacular","bien"
]

palabras_negativas = [
    "triste","mal","malo","mala","pesimo","horrible","aburrido",
    "aburrida","decepcionante","odio","odie","feo","fea",
    "terrible","deprimido","deprimida","enojado","enojada"
]

conectores_de_contraste=["pero","aunque","sin embargo"]

def tokenizar(texto):
    texto= texto.lower()
    for signo in [".",",","!","?",";"]:
        texto=texto.replace(signo,"")
    return texto.split()

def analizar_sentimiento(texto):
    tokens=tokenizar(texto)

    puntaje=0
    encontro_conector=False
    for i, palabra in enumerate(tokens):
        if palabra in conectores_de_contraste:
            encontro_conector=True
            continue
        if palabra in palabras_positivas:
            puntaje+=2 if encontro_conector else 1

        elif palabra in palabras_negativas:
            puntaje=-2 if encontro_conector else -1

    if puntaje>0:
        return "sentimiento positivo", puntaje
    elif puntaje<0:
        return "sentimiento negativo",puntaje
    else: 
        return "sentimiento neutro",puntaje


if __name__=="__main__":
    print("Analizador de Sentimientos")
    print("Escribe una frase y te dire si es positiva, negativa o neutra")
    print("Escribe 'salir' para terminar el programa")
    while True:
        texto_usuario=input("Escribe tu texto: ")
        if texto_usuario.lower() =="salir":
            break

        resultado, puntaje=analizar_sentimiento(texto_usuario)
        print(f"Resultado: {resultado}  {puntaje}\n")

