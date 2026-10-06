# Pre Entrega Módulo 5 — Agente RAG con conocimiento organizacional

Continuación del Checkpoint 1 (`../checkpoint1_S_Maureira.json`): el mismo agente de leads ahora responde con base en el manual comercial indexado en LlamaCloud.

| Archivo | Para qué |
|---|---|
| `base_conocimiento/Manual_Comercial_NexoDigital_v3.1.pdf` | Documento maestro: se parsea en LlamaCloud → Parse (LlamaParse, tier Agentic) y se descarga el Markdown |
| `n8n/PreEntrega_Modulo5_Agente_RAG_S_Maureira.json` | Workflow para importar en n8n (Groq + formulario de carga + Simple Vector Store con embeddings de Gemini; herramienta `consultar_manual_comercial`, Top-K 4) |
| `n8n/system_prompt_RAG.md` | System prompt del agente (citas + regla "No sé") |
| `planilla/Leads_NexoDigital.xlsx` | Planilla para Google Sheets: hoja `Leads` (la usa el agente) y hoja `Bateria_Validacion` (para anotar las 5 preguntas) |
| `entrega/informe.html` | Fuente del PDF final (5 piezas) |
| `entrega/PreEntrega_Modulo5_SMaureira.pdf` | PDF a entregar (renombrar con nombre y apellido completos) |

## Pasos
1. Parsear el PDF en LlamaCloud → Parse (tier Agentic) y guardar el resultado como `Manual_Comercial_parseado.md`
   (el plan Free de LlamaCloud no permite crear Index ni Data Sources).
2. Importar el workflow, cargar las credenciales (Groq, Gemini, Google Sheets, Gmail), abrir la URL del nodo
   "Formulario - Cargar manual" y subir el .md. La base vive en memoria: si n8n se reinicia, volver a cargarlo.
3. Correr las 5 preguntas de la pieza 4 y corregir en `entrega/informe.html` lo que haya respondido realmente el agente.
4. Guardar las capturas en `entrega/capturas/` como `1_llamacloud_data_source.png`, `2_retrieve_tool_topk_score.png` y `3_system_prompt.png`.
5. Regenerar el PDF: `NODE_PATH=$(npm root -g) node modulo5/build_pdf.js`
