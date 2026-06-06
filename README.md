# Painel Hospitalar | PNAD COVID-19

Dashboard em Streamlit para o Tech Challenge PNAD COVID-19, com foco em leitura executiva, hospitalar e analítica.

## Fonte dos dados

O app lê exclusivamente os CSVs materializados da pasta `dados_dashboard/`.
Não há conexão com AWS, Athena, banco de dados, APIs externas ou internet.

Arquivos usados:

- `analise_01_barreira_economica.csv`
- `analise_02_informalidade_risco.csv`
- `analise_03_perfil_grave.csv`
- `analise_04_protecao_social.csv`
- `analise_05_mapa_desigualdade.csv`
- `analise_06_evolucao_mensal.csv`
- `analise_07_escolaridade_genero.csv`
- `analise_08_moradia_endividamento.csv`
- `analise_09_sus_privado.csv`
- `correlacoes_economico_clinico.csv`

## Como rodar no Windows PowerShell

Dentro da pasta do projeto:

```powershell
py -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m streamlit run app.py
```

Se preferir ativar o ambiente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Como rodar no Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Estrutura esperada

```text
dashboard_streamlit_pnad_final/
├── app.py
├── requirements.txt
├── README.md
└── dados_dashboard/
    ├── analise_01_barreira_economica.csv
    ├── analise_02_informalidade_risco.csv
    ├── analise_03_perfil_grave.csv
    ├── analise_04_protecao_social.csv
    ├── analise_05_mapa_desigualdade.csv
    ├── analise_06_evolucao_mensal.csv
    ├── analise_07_escolaridade_genero.csv
    ├── analise_08_moradia_endividamento.csv
    ├── analise_09_sus_privado.csv
    └── correlacoes_economico_clinico.csv
```

## Páginas do painel

1. Visão executiva
2. Sinais de alerta
3. Acesso ao cuidado
4. Perfil clínico
5. Territórios e rede
6. Trabalho e proteção social
7. Correlações e cautelas
8. Plano de ação
9. Validação técnica

## Cautelas metodológicas

- Internação é analisada entre atendidos, não sobre toda a população.
- Correlações são exploratórias e não indicam causalidade.
- Amostras pequenas devem ser comunicadas com cautela.
- Locais de atendimento não devem ser somados como partes exclusivas de um único total.
