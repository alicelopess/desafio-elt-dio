import constants
import pandas as pd
import requests
import json
import time
import openai

# 1 - Extract
#TODO: Extrair os dados do arquivo CSV.

##Ler csv - Atribuir a uma variável
df = pd.read_csv('booksID.csv')

#Coletar apenas dados da coluna BookID - Atribuir a uma variável
books_ids = df['BookID'].tolist()

#Teste
##print(books_ids)

#TODO: Obter os dados de cada ID utilizando a API de livros

def get_book(id):
  response = requests.get(f'{constants.BOOKS_API_URL}/books/{id}')
  return response.json() if response.status_code == 200 else None

books = []
for id in books_ids:
  if get_book(id) is not None:
    books.append(get_book(id))

#Teste
##print(books)
##print(json.dumps(books, indent=4))

#OBS: Compreensão de listas 
##  books = [book for id in books_ids if (book := get_book(id)) is not None]


# 2 - Transform
#TODO: Implementar a integração com o ChatGPT usando o modelo GPT-4

openai.api_key = constants.OPENAI_API_KEY

def generate_ai_description(book):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {"role": "system", "content": "Você trabalha em uma livraria, é um especialista em livros e leitor entusiasta. Seu papel na livraria é criar descrições atraentes para os livros."},
        {"role": "user", "content": f"Crie uma descrição atraente para o livro {book['title']}. Coloque o título do livro. Use no máximo 200 caracteres."}
    ]
  )
  return response['choices'][0]['message']['content'].strip('\"')

descriptions = []
for book in books:
  descriptions = generate_ai_description(book)
  book['description'] = descriptions
  print(descriptions)
  time.sleep(20)
print(books)

# 3 - Load
#TODO: Atualizar os usuários na API de livros com os dados enriquecidos
def update_book(book, json):
  print(book['id'])
  response = requests.put(f'{constants.BOOKS_API_URL}/books/{book["id"]}', data=json)
  return True if response.status_code == 200 else False

for book in books:
  json_book = json.dumps(book)
  print(json_book)
  sucess = update_book(book, json_book)
  print(f"Book {book['title']} updated? {sucess}")

##Teste
def get_books():
  response = requests.get(f'{constants.BOOKS_API_URL}/books')
  print(response.content)
  return response.json() if response.status_code == 200 else None

print(get_books())
