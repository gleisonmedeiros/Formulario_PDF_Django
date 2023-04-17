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
    return render(request, 'form.html')

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

        file_path1 = os.path.join(settings.MEDIA_ROOT, 'arquivo.pdf')
        file_path2 = os.path.join(settings.MEDIA_ROOT, 'capa.jpg')
        file_path3 = os.path.join(settings.MEDIA_ROOT, 'grafico1.jpg')
        file_path4 = os.path.join(settings.MEDIA_ROOT, 'logo2.png')
        #file_path5 = os.path.join(settings.MEDIA_ROOT, 'logo.png')
        file_path6 = os.path.join(settings.MEDIA_ROOT, 'folha.png')

        ##### RECUPERA DO BACKBRAZE ####

        # Crie uma instância do cliente boto3
        id = os.environ.get('backblaze_id')
        key = os.environ.get('backblaze_key')

        print(id)
        print(key)

        s3 = boto3.client('s3',
                          aws_access_key_id=id,
                          aws_secret_access_key=key,
                          endpoint_url='https://s3.us-east-005.backblazeb2.com')

        # Busque o arquivo .png no Backblaze B2
        response = s3.get_object(Bucket='agpydajngo', Key='media/logo.PNG')

        # Faça algo com o arquivo, como salvar na memória ou retorná-lo como resposta HTTP
        image_bytes = response['Body'].read()

        # carregar imagem a partir dos bytes
        file_path5 = Image.open(io.BytesIO(image_bytes))

        arquivo_json(dicionario_form)

        exporta_pdf(file_path1,file_path2,file_path3,file_path4,file_path5,file_path6,dicionario_form)

        with open(file_path1, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
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