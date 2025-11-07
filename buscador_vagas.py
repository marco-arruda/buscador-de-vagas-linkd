#!/usr/bin/env python3
"""
Buscador de Vagas LinkedIn
Script para buscar vagas de emprego no LinkedIn (versão pública, sem necessidade de login)
"""

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time


class LinkedInJobScraper:
    """Classe para realizar web scraping de vagas no LinkedIn"""
    
    def __init__(self):
        self.base_url = "https://www.linkedin.com/jobs/search"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def buscar_vagas(self, keywords="", location="Recife, Pernambuco, Brasil", num_paginas=1):
        """
        Busca vagas no LinkedIn
        
        Args:
            keywords (str): Palavras-chave para buscar (ex: "Python", "Desenvolvedor")
            location (str): Localização das vagas
            num_paginas (int): Número de páginas para buscar
            
        Returns:
            list: Lista de dicionários com informações das vagas
        """
        vagas = []
        
        params = {
            'keywords': keywords,
            'location': location,
            'geoId': '106236613',
            'trk': 'public_jobs_jobs-search-bar_search-submit',
            'position': '1',
            'pageNum': '0'
        }
        
        print(f"Buscando vagas para: {keywords if keywords else 'todas as categorias'}")
        print(f"Localização: {location}")
        print("-" * 60)
        
        for pagina in range(num_paginas):
            params['pageNum'] = str(pagina)
            params['start'] = str(pagina * 25)  # LinkedIn mostra 25 vagas por página
            
            try:
                print(f"\nBuscando página {pagina + 1}...")
                response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Encontrar todos os cards de vagas
                job_cards = soup.find_all('div', class_='base-card')
                
                if not job_cards:
                    # Tentar outra estrutura possível
                    job_cards = soup.find_all('li', class_='result-card')
                
                if not job_cards:
                    print(f"Nenhuma vaga encontrada na página {pagina + 1}")
                    continue
                
                print(f"Encontradas {len(job_cards)} vagas na página {pagina + 1}")
                
                for card in job_cards:
                    vaga = self._extrair_dados_vaga(card)
                    if vaga:
                        vagas.append(vaga)
                
                # Pausa para não sobrecarregar o servidor
                if pagina < num_paginas - 1:
                    time.sleep(2)
                    
            except requests.exceptions.RequestException as e:
                print(f"Erro ao buscar página {pagina + 1}: {e}")
                continue
        
        return vagas
    
    def _extrair_dados_vaga(self, card):
        """
        Extrai dados de uma vaga a partir do card HTML
        
        Args:
            card: Elemento BeautifulSoup do card da vaga
            
        Returns:
            dict: Dicionário com dados da vaga ou None se não conseguir extrair
        """
        try:
            # Tentar diferentes estruturas de HTML que o LinkedIn pode usar
            
            # Título da vaga
            titulo_elem = card.find('h3', class_='base-search-card__title')
            if not titulo_elem:
                titulo_elem = card.find('h3')
            titulo = titulo_elem.get_text(strip=True) if titulo_elem else "N/A"
            
            # Nome da empresa
            empresa_elem = card.find('h4', class_='base-search-card__subtitle')
            if not empresa_elem:
                empresa_elem = card.find('a', class_='hidden-nested-link')
            if not empresa_elem:
                empresa_elem = card.find('h4')
            empresa = empresa_elem.get_text(strip=True) if empresa_elem else "N/A"
            
            # Localização
            localizacao_elem = card.find('span', class_='job-search-card__location')
            if not localizacao_elem:
                localizacao_elem = card.find('span', class_='job-result-card__location')
            localizacao = localizacao_elem.get_text(strip=True) if localizacao_elem else "N/A"
            
            # Link da vaga
            link_elem = card.find('a', class_='base-card__full-link')
            if not link_elem:
                link_elem = card.find('a', href=True)
            link = link_elem.get('href', 'N/A') if link_elem else "N/A"
            
            # Data de postagem (se disponível)
            data_elem = card.find('time')
            data = data_elem.get('datetime', 'N/A') if data_elem else "N/A"
            
            return {
                'titulo': titulo,
                'empresa': empresa,
                'localizacao': localizacao,
                'link': link,
                'data_postagem': data
            }
            
        except Exception as e:
            print(f"Erro ao extrair dados da vaga: {e}")
            return None
    
    def salvar_csv(self, vagas, nome_arquivo=None):
        """
        Salva as vagas em um arquivo CSV
        
        Args:
            vagas (list): Lista de vagas
            nome_arquivo (str): Nome do arquivo (opcional)
        """
        if not vagas:
            print("Nenhuma vaga para salvar.")
            return
        
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"vagas_linkedin_{timestamp}.csv"
        
        try:
            with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['titulo', 'empresa', 'localizacao', 'link', 'data_postagem']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(vagas)
            
            print(f"\n✓ {len(vagas)} vagas salvas em: {nome_arquivo}")
            
        except Exception as e:
            print(f"Erro ao salvar CSV: {e}")
    
    def exibir_vagas(self, vagas):
        """
        Exibe as vagas no console de forma formatada
        
        Args:
            vagas (list): Lista de vagas
        """
        if not vagas:
            print("\nNenhuma vaga encontrada.")
            return
        
        print(f"\n{'='*60}")
        print(f"VAGAS ENCONTRADAS: {len(vagas)}")
        print(f"{'='*60}\n")
        
        for i, vaga in enumerate(vagas, 1):
            print(f"{i}. {vaga['titulo']}")
            print(f"   Empresa: {vaga['empresa']}")
            print(f"   Localização: {vaga['localizacao']}")
            print(f"   Data: {vaga['data_postagem']}")
            print(f"   Link: {vaga['link']}")
            print("-" * 60)


def main():
    """Função principal"""
    print("=" * 60)
    print("BUSCADOR DE VAGAS LINKEDIN")
    print("=" * 60)
    
    scraper = LinkedInJobScraper()
    
    # Exemplo 1: Buscar todas as vagas em Recife
    print("\n1. Buscando todas as vagas em Recife...")
    vagas = scraper.buscar_vagas(
        keywords="",
        location="Recife, Pernambuco, Brasil",
        num_paginas=1
    )
    
    # Exibir resultados
    scraper.exibir_vagas(vagas)
    
    # Salvar em CSV
    scraper.salvar_csv(vagas)
    
    # Exemplo 2: Buscar vagas específicas (comentado por padrão)
    # print("\n2. Buscando vagas de Desenvolvedor Python em Recife...")
    # vagas_python = scraper.buscar_vagas(
    #     keywords="Python Desenvolvedor",
    #     location="Recife, Pernambuco, Brasil",
    #     num_paginas=1
    # )
    # scraper.exibir_vagas(vagas_python)
    # scraper.salvar_csv(vagas_python, "vagas_python.csv")


if __name__ == "__main__":
    main()
