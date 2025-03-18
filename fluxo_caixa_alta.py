# O código devera listar as maiores empresas do brasil
import os # Necessário para acessar as variaveis 
from dotenv import load_dotenv # Acesso aos Arquivos 
import itertools # Loop entre as chaves
import spacy #Processamento de Lingua Natural (NPL)
import serpapi # API para Busca
from collections import defaultdict # Dic especial 
import unicodedata # Remove Acentos
from rapidfuzz import fuzz, process # Similidade em % Das Strings
import aiohttp # Requisições HTTP assíncronas
import asyncio # Execução assíncrona 
from bs4 import BeautifulSoup # Analisa os Doc em HTML e XML
from concurrent.futures import ThreadPoolExecutor # Rodando tarefa simultaneamente 

load_dotenv() # Carregando as variáveis do arquivo .env 
api_keys = [os.getenv("SERPAPI_KEY1"), os.getenv("SERPAPI_KEY2")] # Armazenando a chave

# Verifica se as chaves foram carregadas corretamente
api_keys = [key for key in api_keys if key]  # Remove valores None

if not api_keys:
    raise ValueError("⚠ ERRO: Nenhuma chave da API SerpAPI foi encontrada no arquivo .env!")

# Interador infinito para alterar entre as chaves 
api_key_cycle = itertools.cycle(api_keys)

# Carregar o modelo de linguagem 
nlp = spacy.load("pt_core_news_lg")

# Buscando os links
def buscar_links(pesquisa):    
    #Fontes mais confiáveis
    fontes_primarias = ["SEBRAE", "IBGE", "DELOITTE", "SERASA EXPERIAN", "BACEN", "MINISTÉRIO DA ECONOMIA", "PWC", "MCKINSEY", "BCG", "Valor Econômico"]
    fontes_primarias = [tratamento_texto(fonte) for fonte in fontes_primarias] # Padronizando: Removendo acentos e transformando tudo em maiúsculas
    similaridade = 75 

    api_key = next(api_key_cycle) # Alternando as chaves 
    client = serpapi.Client(api_key=api_key) # Criando uma chave de acesso client

    params = {
        "q": pesquisa,
        "location": "Brazil",
        "hl": "pt",
        "gl": "br",
        "google_domain": "google.com"
    }
    try:
        result = client.search(params)
        if not result:
            print(f"⚠ Nenhum resultado encontrado para '{pesquisa}'")
            return [], []
        busca = []
        links = []
        
        # Filtragem das informações  
        if "organic_results" in result:
            for item in result["organic_results"]:
                if "link" in item and "source" in item: # criterios para filtragem 
                    link = item ["link"]
                    source = tratamento_texto(item["source"]) # Padroniza a descrição   
                    source_o = source
                    # Encontrando a melhor correspondência na lista 
                    melhor_correspondencia, score, _ = process.extractOne(source, fontes_primarias, scorer=fuzz.partial_ratio)

                    if score >= similaridade:
                        links.append(item['link'])
                        busca.append({
                            "pesquisa": pesquisa,
                            "original": source_o,
                            "source": melhor_correspondencia,
                            "link": link
                        })
        else:
            print("⚠ A chave 'organic_results' não foi encontrada no resultado da pesquisa!")
        return busca, links  # Retorna os links filtrados
    except Exception as e:
        print(f"Erro ao buscar por '{pesquisa}': {e}")
        return [], []
    
    # Lista com setores validos 
setores_tratados = defaultdict(set)
setores_validos = [
    # Agricultura e Pecuária
    "Agronegócio", "Agropecuária", "Pecuária", "Produção Animal", "Cultivo de Grãos",
    "Produção Florestal", "Pesca", "Aquicultura",
 
    # Indústria
    "Indústria", "Indústria Automobilística", "Indústria Naval", "Indústria Aeroespacial",
    "Indústria Farmacêutica", "Indústria Química", "Indústria Têxtil", "Indústria de Bebidas",
    "Indústria de Cosméticos", "Indústria Metalúrgica", "Indústria de Papel e Celulose",
    "Indústria Eletroeletrônica", "Indústria de Embalagens", "Indústria de Plásticos",

    # Construção e Infraestrutura
    "Construção", "Construção Civil", "Engenharia Civil", "Obras de Infraestrutura",
    "Arquitetura", "Materiais de Construção",

    # Energia e Recursos Naturais
    "Energia", "Energia Renovável", "Energia Solar", "Energia Eólica", "Petróleo e Gás",
    "Mineração", "Extração de Minerais", "Exploração de Gás Natural",

    # Comércio e Varejo
    "Varejo", "Atacado","Comércio" "Comércio Exterior", "E-commerce", "Supermercados", 
    "Lojas de Departamento", "Comércio Eletrônico",

    # Tecnologia e Inovação
    "Tecnologia", "Startups", "Desenvolvimento de Software", "Hardware", "Inteligência Artificial",
    "Big Data", "Cibersegurança", "Computação em Nuvem", "Blockchain",

    # Saúde e Bem-Estar
    "Saúde", "Medicina", "Hospitalar", "Farmacêutico", "Odontologia", "Veterinária",
    "Estética e Beleza", "Academias e Fitness",

    # Educação
    "Educação", "Ensino Superior", "Ensino Fundamental e Médio", "Educação Profissional",
    "Cursos Online", "E-learning",

    # Transporte e Logística
    "Transporte", "Logística", "Aviação", "Aeroportos", "Transporte Ferroviário",
    "Transporte Marítimo", "Correios e Entregas Rápidas",

    # Finanças e Seguros
    "Finanças", "Bancário", "Seguros", "Investimentos", "Mercado Financeiro", "Fintechs",
    "Cartões de Crédito", "Pagamentos Digitais",

    # Serviços e Consultoria
    "Serviços", "Consultoria Empresarial", "Recursos Humanos", "Coworking",
    "Marketing Digital", "Publicidade", "Assessoria de Imprensa",

    # Turismo e Entretenimento
    "Turismo", "Hotelaria", "Entretenimento", "Restaurantes", "Eventos e Shows",
    "Cinema", "Esportes", "Parques Temáticos",

    # Setor Público e ONGs
    "Setor Público", "Administração Pública", "ONGs", "Terceiro Setor",
    "Defesa e Segurança", "Forças Armadas", "Educação Pública",

    # Comunicação e Mídia
    "Telecomunicações", "TV e Rádio", "Jornalismo", "Publicidade e Propaganda",
    "Streaming", "Redes Sociais",

    # Economia Criativa
    "Indústria Criativa", "Design", "Moda", "Artes Visuais", "Música", "Produção Audiovisual",

    # Outros
    "Setor Jurídico", "Advocacia", "Auditoria e Compliance", "Gestão Ambiental",
    "Sustentabilidade", "Economia Circular"
]

# Função tratamento texto
def tratamento_texto(texto: str) -> str:
    if not isinstance(texto, str):
        return ''
    return "".join(
            c for c in unicodedata.normalize('NFKD', texto.strip().upper())
            if unicodedata.category(c)!='Mn'
        )    

# Criando Dicionário com Setores Tratado
for setor in setores_validos:
    chave = tratamento_texto(setor)
    setores_tratados[chave].add(setor)



# Extrair Titulos e Listas 
async def extrair_setores(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    setores_detectados = set()  
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    print(f"Erro {response.status} ao acessar {url}")
                    return set ()
        


                soup = BeautifulSoup(await response.text(), "html.parser")
                extracoes = {
                    "h1": [tag.text.strip() for tag in soup.find_all('h1')],
                    "h2": [tag.text.strip() for tag in soup.find_all('h2')],
                    "h3": [tag.text.strip() for tag in soup.find_all('h3')],
                    "li": [tag.text.strip() for tag in soup.find_all('li')],
                    "p": [tag.text.strip() for tag in soup.find_all('p')],
                    "strong": [tag.text.strip() for tag in soup.find_all('strong')],
                    "b": [tag.text.strip() for tag in soup.find_all('b')],
                    "td": [tag.text.strip() for tag in soup.find_all('td')],
                }
                #tags_extraidos = soup.select("h1, h2, h3, li, p, strong, b , td")
                tags_extraidos = sum(extracoes.values(), [])

                texto = " ".join([p.get_text() for p in soup.find_all("p")]) # Tratamento e solitações. (for em p solicita todas as tags P ) (p.gat_taxt -> solicitação de cada texto da tag P) (" ".join solicita que cada string seja armazeenada na variavel com espaço)
                texto = tratamento_texto(texto)

                print(f"\n🔎 [DEBUG] Texto extraído de {url}: {texto[:500]}...")  # Mostra um trecho do texto

                setores_detectados = set()
                for tag in tags_extraidos:
                    texto_solicitado = unicodedata.normalize("NFKD", tag.strip().upper())  # Normaliza diretamente a string
                    if not texto_solicitado:
                        print("Erro ao solicitar texto")
                        continue
                    texto_normalizado = tratamento_texto(texto_solicitado)
                    
                    if texto_normalizado in setores_tratados:
                        print(f"✅ Setor encontrado: {setores_tratados[texto_normalizado]}")  # Confirma se encontrou o setor
                        setores_detectados.update(setores_tratados[texto_normalizado])


                return setores_detectados
    except aiohttp.ClientError as e:
        print(f"Erro ao acessar a URL {url}: {e}")
        return set()

# Indificando os setores ORG e MISC
def identificando_setores(texto: str):
    if not texto:
        return set()
    setores_detectados = set()
    doc = nlp(texto)
    for ent in doc.ents:
        if ent.label_ in ["ORG", "MISC"]:
            setores_detectados.add(ent.text)
    return setores_detectados

# Lista de pesquisa
lista_pesquisas = [
        "Quais são os setores que mais movimentam a economia das PMEs no Brasil em faturamento?" , 
        "Quais são os setores que mais faturam no Brasil atualmente, considerando empresas de todos os portes? ",
        "Quais setores tiveram o maior crescimento de receita no Brasil nos últimos dois anos"
    ]

# processando os setores 
async def processar_setores(lista_links_validos):
    setores_identificados = set()
    tarefas = [extrair_setores(url) for url in lista_links_validos]
    resultados = await asyncio.gather(*tarefas, return_exceptions=True)


    for setores in resultados:
        print(f"\n🔹 [DEBUG] Setores extraídos: {setores}")  # Verifica o que foi encontrado

        if isinstance(setores, set):
            setores_identificados.update(setores)
        # else:
        #     print(f"⚠ Aviso: Um dos resultados não retornou um conjunto válido: {setores}
                  
    print("\n📌 **Setores Identificados:**")
    print("-" * 50)
    for setor in sorted(setores_identificados):
        print(f"✅ {setor}")
    print("-" * 50)

        
    

if __name__ == "__main__":
    # Apenas será executado se rodar diretamente este arquivo
    print("Executando setores_api.py diretamente!")

    with ThreadPoolExecutor(max_workers=2) as executor:
        resultados = list(executor.map(buscar_links, lista_pesquisas))

    # Separando os resultados da busca e os links coletados
    busca_resultados = []
    lista_links = []

    for busca, links in resultados:
        busca_resultados.extend(busca)
        lista_links.extend(links)

    # Remover duplicatas nos links
    lista_links = list(set(lista_links))

    # Exibir os links encontrados
    print("\n🔎 **Links encontrados:**")
    for link in lista_links:
        print(f"✅ {link}")

    # Processar setores identificados
    lista_links_validos = [url for url in lista_links if url.startswith("http")]

    if lista_links_validos:
        asyncio.run(processar_setores(lista_links_validos))
    else:
        print("⚠ Nenhum link válido encontrado para processar os setores!")