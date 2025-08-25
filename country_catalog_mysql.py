import mysql.connector
from fastapi import FastAPI, HTTPException, Query, Body
import requests
from typing import List, Dict, Any
from pydantic import BaseModel

app = FastAPI()

# Configuração do banco de dados MySQL
DB_CONFIG = {
    "host": "localhost",
    "database": "countries_db",
    "user": "admin",
    "password": "admin",
    "auth_plugin": "mysql_native_password"
}

def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

# Cria a tabela se não existir
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            country_name VARCHAR(255) NOT NULL,
            rating BOOLEAN NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# Inicializa o banco ao iniciar a aplicação
init_db()

# Função auxiliar para obter avaliações de um ou mais países
def get_ratings(country_names: List[str]) -> Dict[str, Dict[str, int]]:
    if not country_names:
        return {}
    
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    placeholders = ','.join(['%s'] * len(country_names))
    cur.execute(f"""
        SELECT 
            country_name,
            SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END) as curtidas,
            SUM(CASE WHEN rating = 0 THEN 1 ELSE 0 END) as nao_curtidas
        FROM ratings
        WHERE country_name IN ({placeholders})
        GROUP BY country_name;
    """, country_names)
    results = cur.fetchall()
    conn.close()
    
    ratings_dict = {row['country_name']: {'curtidas': row['curtidas'] or 0, 'nao_curtidas': row['nao_curtidas'] or 0} for row in results}
    
    # Adiciona países sem avaliações
    for name in country_names:
        if name not in ratings_dict:
            ratings_dict[name] = {'curtidas': 0, 'nao_curtidas': 0}
    
    return ratings_dict

# Função auxiliar para formatar dados do país
def format_country_data(country: Dict[str, Any], ratings: Dict[str, int]) -> Dict[str, Any]:
    return {
        "nome": country['name']['common'],
        "populacao": country['population'],
        "continente": country['continents'][0] if country['continents'] else "Desconhecido",
        "curtidas": ratings['curtidas'],
        "nao_curtidas": ratings['nao_curtidas']
    }

@app.get("/paises/top10", response_model=List[Dict[str, Any]])
def get_top10():
    try:
        response = requests.get("https://restcountries.com/v3.1/all?fields=name,population,continents")
        response.raise_for_status()
        countries = response.json()
        
        # Ordena por população descendente e pega top 10
        top10 = sorted(countries, key=lambda x: x['population'], reverse=True)[:10]
        
        country_names = [c['name']['common'] for c in top10]
        ratings = get_ratings(country_names)
        
        formatted = [format_country_data(c, ratings[c['name']['common']]) for c in top10]
        return formatted
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar API: {str(e)}")

@app.get("/paises/buscar", response_model=Dict[str, Any])
def buscar_pais(nome: str = Query(..., min_length=1)):
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{nome}?fields=name,population,continents")
        response.raise_for_status()
        countries = response.json()
        
        if not countries:
            raise HTTPException(status_code=404, detail="País não encontrado")
        
        # Pega o primeiro resultado
        country = countries[0]
        ratings = get_ratings([country['name']['common']])
        formatted = format_country_data(country, ratings[country['name']['common']])
        return formatted
    except requests.RequestException as e:
        if e.response and e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="País não encontrado")
        raise HTTPException(status_code=500, detail=f"Erro ao consultar API: {str(e)}")

class AvaliacaoRequest(BaseModel):
    nome: str
    avaliacao: str  # "curti" ou "nao_curti"

@app.post("/paises/avaliar")
def avaliar_pais(request: AvaliacaoRequest = Body(...)):
    if request.avaliacao not in ["curti", "nao_curti"]:
        raise HTTPException(status_code=400, detail="Avaliação deve ser 'curti' ou 'nao_curti'")
    
    rating = 1 if request.avaliacao == "curti" else 0
    
    try:
        # Verifica se o país existe na API
        response = requests.get(f"https://restcountries.com/v3.1/name/{request.nome}?fields=name")
        response.raise_for_status()
        countries = response.json()
        if not countries:
            raise HTTPException(status_code=404, detail="País não encontrado")
        
        country_name = countries[0]['name']['common']
        
        # Insere a avaliação
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO ratings (country_name, rating) VALUES (%s, %s);
        """, (country_name, rating))
        conn.commit()
        
        # Obtém contagens atualizadas
        cur.execute("""
            SELECT 
                SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END) as curtidas,
                SUM(CASE WHEN rating = 0 THEN 1 ELSE 0 END) as nao_curtidas
            FROM ratings
            WHERE country_name = %s;
        """, (country_name,))
        result = cur.fetchone()
        conn.close()
        
        curtidas = result[0] or 0
        nao_curtidas = result[1] or 0
        total_votos = curtidas + nao_curtidas
        
        return {
            "pais": country_name,
            "status": "sucesso",
            "quantidade_votos": total_votos
        }
    except requests.RequestException as e:
        if e.response and e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="País não encontrado")
        raise HTTPException(status_code=500, detail=f"Erro ao consultar API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
