# Pre Entrega Módulo 5 — Agente RAG con conocimiento organizacional

Continuación del Checkpoint 1 (`../checkpoint1_S_Maureira.json`): el mismo agente de leads ahora responde con base en el manual comercial indexado en LlamaCloud.

| Archivo | Para qué |
|---|---|
| `base_conocimiento/Manual_Comercial_NexoDigital_v3.1.pdf` | Documento maestro para subir al Data Source de LlamaCloud (hay títulos jerárquicos y 5 tablas) |
| `n8n/PreEntrega_Modulo5_Agente_RAG_S_Maureira.json` | Workflow para importar en n8n (modelo: Groq Chat Model; Checkpoint 1 + herramienta `consultar_manual_comercial`, Top-K 4, Min Score 0.55) |
| `n8n/system_prompt_RAG.md` | System prompt del agente (citas + regla "No sé") |
| `planilla/Leads_NexoDigital.xlsx` | Planilla para Google Sheets: hoja `Leads` (la usa el agente) y hoja `Bateria_Validacion` (para anotar las 5 preguntas) |
| `entrega/informe.html` | Fuente del PDF final (5 piezas) |
| `entrega/PreEntrega_Modulo5_SMaureira.pdf` | PDF a entregar (renombrar con nombre y apellido completos) |

## Pasos
1. Subir el PDF del manual a LlamaCloud (LlamaParse en modo markdown, chunking 512 / overlap 64).
2. Importar el workflow y reemplazar `REPLACE_WITH_TU_PIPELINE_ID` y las credenciales (LlamaCloud: Header Auth `Authorization: Bearer llx-...`).
   Si tu n8n tiene el nodo nativo de Vector Store para LlamaCloud, usá ese con los mismos nombres, descripción y valores.
3. Correr las 5 preguntas de la pieza 4 y corregir en `entrega/informe.html` lo que haya respondido realmente el agente.
4. Guardar las capturas en `entrega/capturas/` como `1_llamacloud_data_source.png`, `2_retrieve_tool_topk_score.png` y `3_system_prompt.png`.
5. Regenerar el PDF: `NODE_PATH=$(npm root -g) node modulo5/build_pdf.js`
