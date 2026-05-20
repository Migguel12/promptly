#!/bin/bash

# Use o IP interno se o localhost falhar, mas localhost costuma funcionar
API_URL="http://localhost:8000/commands/"

# 1. Busca os nomes e filtra com Rofi (Double click ou Enter funciona)
selected_name=$(curl -s "$API_URL" | jq -r '.[].name' | rofi -dmenu -i -p "Promptly Search:" -normal-window)

if [ -z "$selected_name" ]; then exit 1; fi

# 2. Busca o template usando o nome selecionado (Tratando espaços para a URL)
# Usamos o jq para filtrar o objeto que tem o nome exato
template=$(curl -s "$API_URL" | jq -r --arg NAME "$selected_name" '.[] | select(.name == $NAME) | .template')

# Se o template estiver vazio, avisa e sai
if [ -z "$template" ] || [ "$template" == "null" ]; then
    notify-send "Promptly" "Erro: Template não encontrado para $selected_name"
    exit 1
fi

# 3. Lógica de Variáveis {exemplo}
final_command=$template
# Regex para encontrar tudo que está entre { }
variables=$(echo "$template" | grep -oP '\{.*?\}')

if [ ! -z "$variables" ]; then
    for var in $variables; do
        clean_var=$(echo "$var" | tr -d '{}')
        # Abre o Rofi para pedir a variável
	value=$(echo "" | rofi -dmenu -p "Valor para [$clean_var]:" -lines 0 -normal-window)

        # Se cancelar a entrada da variável, para tudo
        if [ -z "$value" ]; then exit 1; fi

        final_command="${final_command//$var/$value}"
    done
fi

# 4. Copia para o clipboard e notifica
echo -n "$final_command" | xclip -selection clipboard
notify-send "Promptly" "Copiado: $final_command"
