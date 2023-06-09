import io
import json
from django.http import HttpResponse ,  Http404
import os
from django.conf import settings
from .gera_pdf import exporta_pdf
from django.shortcuts import render
from difflib import ndiff
import boto3
from PIL import Image
from PyPDF2 import PdfReader
import environ
from dotenv import load_dotenv

from .forms import JSONUploadForm

# Create your views here.
def hello(request):
    return HttpResponse("Hello, World")

def sum(request):
    num1 = request.POST.get('num1')
    num2 = request.POST.get('num2')
    if num1 and num2:
        result = int(num1) + int(num2)
        return render(request, 'sum.html', {'result': result})
    else:
        return render(request, 'sum.html')


def form(request):
    load_dotenv()

    AMBIENTE = os.getenv('AMBIENTE')

    print(AMBIENTE)
    return render(request, 'form.html',{'AMBIENTE':AMBIENTE})

def arquivo_json(dicionario_form):

    json_string = json.dumps(dicionario_form)

    nome_arquivo = os.path.join(settings.MEDIA_ROOT, 'cadastro.json')

    arquivo = open(nome_arquivo, 'w')

    # Abre o arquivo para escrita
    with open(nome_arquivo, 'w') as arquivo:
        # Escreve o JSON no arquivo
        json.dump(json_string, arquivo)

    arquivo.close()


def download_file(request):
    if request.method == 'POST' and 'salvar' in request.POST:

        dicionario_form = {}

        lista = ['mes_ano','titulo_superior','titulo_principal','subtitulo','elaborado','titulo2','titulo_grafico','item11','item12','item13','item21','item22','item23','item31','item32','item33','item41','item42','item43']

        for i in lista:
            temp = i
            dicionario_form[i] = str(request.POST.get(i))

        # Crie uma instância do cliente boto3
        id = os.environ.get('backblaze_id')
        key = os.environ.get('backblaze_key')

        print(id)
        print(key)

        s3 = boto3.client('s3',
                          aws_access_key_id=id,
                          aws_secret_access_key=key,
                          endpoint_url='https://s3.us-east-005.backblazeb2.com')

        arquivo_json(dicionario_form)

        load_dotenv()

        VARIAVEL = os.getenv('AMBIENTE')

        if (VARIAVEL=='local'):
            file_path1 = os.path.join(settings.MEDIA_ROOT, 'arquivo.pdf')
            file_path2 = os.path.join(settings.MEDIA_ROOT, 'capa.jpg')
            file_path3 = os.path.join(settings.MEDIA_ROOT, 'grafico1.jpg')
            file_path4 = os.path.join(settings.MEDIA_ROOT, 'logo2.png')
            file_path5 = os.path.join(settings.MEDIA_ROOT, 'logo.png')
            file_path6 = os.path.join(settings.MEDIA_ROOT, 'folha.png')

            exporta_pdf(file_path1,
                        file_path2,
                        file_path3,
                        file_path4,
                        file_path5,
                        file_path6,
                        dicionario_form, s3,VARIAVEL)

            with open(file_path1, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="arquivo.pdf"'
                return response

        elif(VARIAVEL=='railway'):
            ##### RECUPERA DO BACKBRAZE ####

            # Busque o arquivo .png no Backblaze B2
            dicionario_media = {}

            nome_arquivo = ['capa.jpg','grafico1.jpg','logo2.PNG','logo.PNG','folha.png']
            local = ['file_path2','file_path3','file_path4','file_path5','file_path6']

            for elemento1, elemento2 in zip(nome_arquivo, local):

                caminho = 'media/'+ elemento1

                print(caminho)

                response = s3.get_object(Bucket='agpydajngo', Key=str(caminho))

                # Faça algo com o arquivo, como salvar na memória ou retorná-lo como resposta HTTP
                image_bytes = response['Body'].read()

                # carregar imagem a partir dos bytes
                dicionario_media[elemento2] = Image.open(io.BytesIO(image_bytes))

            # Faz a leitura do arquivo PDF do S3
            response = s3.get_object(Bucket='agpydajngo', Key='media/arquivo.pdf')
            pdf_bytes = response['Body'].read()

            # Cria um objeto de arquivo PDF com os bytes lidos
            file_path1 = PdfReader(io.BytesIO(pdf_bytes))

            s3.delete_object(Bucket='agpydajngo', Key='media/grafico1.jpg')

            exporta_pdf(file_path1,
                        dicionario_media['file_path2'],
                        dicionario_media['file_path3'],
                        dicionario_media['file_path4'],
                        dicionario_media['file_path5'],
                        dicionario_media['file_path6']
                        ,dicionario_form,s3,VARIAVEL)

            response = s3.get_object(Bucket='agpydajngo', Key='media/arquivo.pdf')

            response = HttpResponse(response['Body'].read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="arquivo.pdf"'
            return response

def limpar_campos(request):
    if request.method == 'POST':
        request.POST = {}
    return render(request, 'form.html', {})

def download_json(request):
    if request.method == 'POST':

        nome_arquivo = os.path.join(settings.MEDIA_ROOT, 'cadastro.json')

        with open(nome_arquivo, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/txt')
            response['Content-Disposition'] = 'attachment; filename="cadastro.json"'
            return response


def upload_json(request):
    if request.method == 'POST':
        #try:
        # Obtém o arquivo de upload
        arquivo = request.FILES['json_file']

        # Lê o conteúdo do arquivo JSON
        conteudo = arquivo.read().decode('utf-8')
        dados = json.loads(conteudo)

        dicionario_cadastro = json.loads(dados)

        dicionario_cadastro['susesso'] = True

        return render(request, 'form.html', dicionario_cadastro)
        #except:
            #return render(request, 'form.html', {'sucesso': False})

    return render(request, 'form.html' ,{'sucesso': 'n'})