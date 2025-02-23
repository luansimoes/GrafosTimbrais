# Grafos Timbrais
Este repositório foi criado no contexto de minha dissertação "Grafos Timbrais: propriedades estruturais e aplicação musical". 
Nele, você encontrará scripts para a execução de tarefas de pesquisa, investigando aspectos como:
* Automorfismos
* Cliques máximas
* Ciclos hamiltonianos

## Arquivos
* grafo_timbral.py : Classe base que implementa a estrutura dos grafos timbrais. Inclui método recursivo para obtenção de um ciclo hamiltoniano em grafos timbrais binários, partindo da demonstração indutiva na dissertação.
* automorfismos.py : script que verifica se os grafos T(4,3,1), T(3,4,1), T(2,5,2) e T(2,7,3) são distância-transitivos, exportando tabelas dos automorfismos que certificam essa propriedade para a pasta _automorfismos\_encontrados_. 
