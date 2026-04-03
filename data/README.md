# Date pentru Chatbot Culinar

## Structură

### `raw/` - Date brute
- `intrebari_culinare.json` - 100 întrebări cu răspunsuri
- `retete_complete.json` - 40 rețete detaliate
- `conversatii.log` - 30 conversații reale

### `processed/` - Date procesate
- `date_antrenare.csv` - 400+ exemple pentru model
- `intrebari_curatate.json` - întrebări preprocesate
- `date_antrenare_curatate.csv` - date curățate
- `statistici.json` - statistici generate
- `intentii_antrenare.json` - structură intenții
- `scheme_raspuns.json` - răspunsuri predefinite

## Statistici
- Total întrebări: 100
- Total rețete: 40
- Total exemple antrenare: 400+
- Total intenții: 10

## Cum se folosesc
1. Pentru antrenare model: folosește `date_antrenare.csv`
2. Pentru API: folosește `scheme_raspuns.json`
3. Pentru testare: folosește `conversatii.log`