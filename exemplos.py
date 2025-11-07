#!/usr/bin/env python3
"""
Exemplos de uso do Buscador de Vagas LinkedIn

Este arquivo demonstra diferentes formas de usar o scraper
"""

from buscador_vagas import LinkedInJobScraper


def exemplo_basico():
    """Exemplo básico: buscar todas as vagas em Recife"""
    print("=" * 60)
    print("EXEMPLO 1: Busca básica - Todas as vagas em Recife")
    print("=" * 60)
    
    scraper = LinkedInJobScraper()
    vagas = scraper.buscar_vagas(
        keywords="",
        location="Recife, Pernambuco, Brasil",
        num_paginas=1
    )
    
    scraper.exibir_vagas(vagas)
    scraper.salvar_csv(vagas)


def exemplo_palavras_chave():
    """Exemplo com palavras-chave específicas"""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Busca com palavras-chave - Python")
    print("=" * 60)
    
    scraper = LinkedInJobScraper()
    vagas = scraper.buscar_vagas(
        keywords="Python",
        location="Recife, Pernambuco, Brasil",
        num_paginas=1
    )
    
    scraper.exibir_vagas(vagas)
    scraper.salvar_csv(vagas, "vagas_python.csv")


def exemplo_multiplas_paginas():
    """Exemplo buscando múltiplas páginas"""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Busca em múltiplas páginas - Desenvolvedor")
    print("=" * 60)
    
    scraper = LinkedInJobScraper()
    vagas = scraper.buscar_vagas(
        keywords="Desenvolvedor",
        location="Recife, Pernambuco, Brasil",
        num_paginas=3
    )
    
    scraper.exibir_vagas(vagas)
    scraper.salvar_csv(vagas, "vagas_desenvolvedor.csv")


def exemplo_diferentes_localizacoes():
    """Exemplo buscando em diferentes localizações"""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: Busca em diferentes localizações")
    print("=" * 60)
    
    scraper = LinkedInJobScraper()
    
    localizacoes = [
        "Recife, Pernambuco, Brasil",
        "São Paulo, São Paulo, Brasil",
        "Rio de Janeiro, Rio de Janeiro, Brasil"
    ]
    
    todas_vagas = []
    
    for loc in localizacoes:
        print(f"\nBuscando em: {loc}")
        vagas = scraper.buscar_vagas(
            keywords="Remote",
            location=loc,
            num_paginas=1
        )
        todas_vagas.extend(vagas)
    
    print(f"\nTotal de vagas encontradas: {len(todas_vagas)}")
    scraper.salvar_csv(todas_vagas, "vagas_todas_localizacoes.csv")


def exemplo_filtrar_resultados():
    """Exemplo de como filtrar resultados após a busca"""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: Filtrar resultados por palavra-chave no título")
    print("=" * 60)
    
    scraper = LinkedInJobScraper()
    vagas = scraper.buscar_vagas(
        keywords="Desenvolvedor",
        location="Recife, Pernambuco, Brasil",
        num_paginas=1
    )
    
    # Filtrar vagas que contenham "Senior" ou "Sênior" no título
    vagas_senior = [
        vaga for vaga in vagas 
        if 'senior' in vaga['titulo'].lower() or 'sênior' in vaga['titulo'].lower()
    ]
    
    print(f"\nVagas com 'Senior' no título: {len(vagas_senior)}")
    scraper.exibir_vagas(vagas_senior)
    
    if vagas_senior:
        scraper.salvar_csv(vagas_senior, "vagas_senior.csv")


if __name__ == "__main__":
    # Descomente o exemplo que deseja executar
    
    exemplo_basico()
    
    # exemplo_palavras_chave()
    
    # exemplo_multiplas_paginas()
    
    # exemplo_diferentes_localizacoes()
    
    # exemplo_filtrar_resultados()
