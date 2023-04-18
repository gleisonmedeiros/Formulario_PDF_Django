import io

from reportlab.pdfgen import canvas
import numpy as np
import matplotlib.pyplot as plt
import mplcyberpunk
import os
from pathlib import Path
import os
from django.conf import settings
# importing the style package
from matplotlib import style

plt.style.use("cyberpunk")

def titulo_pular_linha(pdf,titulo2,linha2,esp,lm):

    espacamento = esp

    frase = titulo2

    temp = 1000

    teste = list(frase)

    global linha

    linha =0

    linha = linha2

    limite = lm

    maximo = 0

    while (maximo != limite + 1):

        primeiros_14 = teste[:limite]

        valor = 0
        cont = 0

        for item in reversed(primeiros_14):
            cont = cont + 1
            if (item == ' '):
                valor = cont
                break

        maximo = limite - valor + 1

        palavra_maximo = primeiros_14[:maximo]

        texto = "".join(palavra_maximo)

        largura_pagina, altura_pagina = pdf._pagesize
        largura_string = pdf.stringWidth(texto)

        x = (largura_pagina - largura_string) / 2

        #print(texto)

        temp = len(teste[maximo:])

        teste = teste[maximo:]

        pdf.drawString(int(x), linha, texto)

        linha = linha - espacamento

        global linhan

        linhan = linha



def exporta_pdf(file_path1,file_path2,file_path3,file_path4,file_path5,file_path6,dicionario_form,s3):

    # Gráfico sobre notas de 3 alunos nas provas do semestre
    CAPTCAO1 = [int(dicionario_form['item11'])]
    CAPTCAO2 = [int(dicionario_form['item12'])]
    CAPTCAO3 = [int(dicionario_form['item13'])]

    ORCAMENTO1 = [int(dicionario_form['item21'])]
    ORCAMENTO2 = [int(dicionario_form['item22'])]
    ORCAMENTO3 = [int(dicionario_form['item23'])]

    VENDAS1 = [int(dicionario_form['item31'])]
    VENDAS2 = [int(dicionario_form['item32'])]
    VENDAS3 = [int(dicionario_form['item33'])]

    EQUIPE1 = [int(dicionario_form['item41'])]
    EQUIPE2 = [int(dicionario_form['item42'])]
    EQUIPE3 = [int(dicionario_form['item43'])]


    # Definindo a largura das barras
    barWidth = 2

    # Aumentando o gráfico
    plt.figure(figsize=(10, 5))

    # Criando as barras
    plt.barh([14], CAPTCAO1, color='#D03534')
    plt.barh([15], CAPTCAO2, color='#EDC657')
    plt.barh([16], CAPTCAO3, color='#719BAE')

    plt.barh([10], ORCAMENTO1, color='#D03534')
    plt.barh([11], ORCAMENTO2, color='#EDC657')
    plt.barh([12], ORCAMENTO3, color='#719BAE')

    plt.barh([6], VENDAS1, color='#D03534')
    plt.barh([7], VENDAS2, color='#EDC657')
    plt.barh([8], VENDAS3, color='#719BAE')

    plt.barh([2], EQUIPE1, color='#D03534')
    plt.barh([3], EQUIPE2, color='#EDC657')
    plt.barh([4], EQUIPE3, color='#719BAE')

    # Adiciando legendas as barras
    plt.yticks([3,7,11,15], ['EQUIPE', 'VENDAS', 'ORÇAMENTO','CAPTAÇÃO'])

    #plt.title(dicionario_form['titulo_grafico'].upper())

    buf = io.BytesIO()
    plt.savefig(buf, format='jpg')
    imagem_bytes = buf.getvalue()

    s3.put_object(Bucket='agpydajngo', Key='media/' + grafico1.jpg, Body=imagem_bytes)


    #plt.show()



    ###################################


    nome_pdf = 'arquivo'
    # = os.path.join(settings.MEDIA_ROOT, 'arquivo.pdf')
    pdf = canvas.Canvas(file_path1)
    pdf.setTitle(nome_pdf)

    #imagem2 = 'testeee.jpeg'
    pdf.drawInlineImage(file_path2,0,0,width=600,height=850)#[coluna][altura]

    pdf.setFillColor('white')
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawString(50,760, dicionario_form['mes_ano'])

    pdf.setFillColor('#DAA520')
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50,723, dicionario_form['titulo_superior'])

    pdf.setFillColor('#000000')
    pdf.setFont("Helvetica-Bold", 60)
    temp = dicionario_form['titulo_principal'].upper()
    titulo_pular_linha(pdf,temp, 425, 70, 14)

    pdf.setFillColor('#A08200')
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawString(450,linhan, dicionario_form['subtitulo'])

    pdf.setFillColor('#DAA520')
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(380,70, 'ELABORADO POR:')

    pdf.setFillColor('white')
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(380,50, dicionario_form['elaborado'])

    pdf.showPage()

    ##########  SEGUNDA PÁGINA #######

    pdf.setFillColor('#20212A')
    pdf.rect(0,0,800,1000,fill=1)

    pdf.setFillColor('#FFFFFF')
    pdf.setFont("Helvetica-Bold", 40)
    titulo_pular_linha(pdf,dicionario_form['titulo2'],750,40,15)

    pdf.drawInlineImage(file_path3,0,200, width=650, height=400)#[coluna][altura]

    pdf.drawInlineImage(file_path5, 440, 650,width=130,height=150)

    pdf.drawInlineImage(file_path4, 30, 650, width=130, height=150)

    pdf.setFillColor('White')
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 560, dicionario_form['titulo_grafico'])

    pdf.setFillColor('#709DB0')
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(120,210, '\u2588')

    pdf.setFillColor('white')
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(130,210, 'PROJEÇÃO DE RESULTADOS')

    pdf.setFillColor('#F1CB5C')
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(260,210, '\u2588')

    pdf.setFillColor('white')
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(270,210, 'APÓS ALTERAÇÕES FEITAS')

    pdf.setFillColor('#C93130')
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(400,210, '\u2588')

    pdf.setFillColor('white')
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(410,210, 'ANTES DOS TRABALHO')

    pdf.setFillColor('#808080')
    pdf.setFont("Helvetica", 16)
    pdf.drawString(100, 20, 'Gestor Milionário - 2022 todos os direitos reservados')

    pdf.save()

    print('{}.pdf criado com sucesso!'.format(nome_pdf))


###########################################
##########################################









