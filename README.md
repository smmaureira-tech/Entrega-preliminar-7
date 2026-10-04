# Proyecto integrador NEXA DIGITAL · Agente de leads en n8n

| Hito | Archivo | Contenido |
|---|---|---|
| Checkpoint 1 | `checkpoint1_S_Maureira.json` | Agente base de calificación de leads (chat → AI Agent → Google Sheets → log Gmail) |
| Pre-entrega 6 · Voice AI | `checkpoint6_S_Maureira.json` | Circuito cerrado de voz: Telegram → Whisper (STT) → IF de contingencia → AI Agent (RAG + CRM) → límite de 200 caracteres → ElevenLabs (TTS) → Telegram Send Audio → destrucción binaria → log de auditoría |
| Entregable PDF | `PreEntrega6_VoiceAI_S_Maureira.pdf` | Captura del lienzo y de los paneles, diagnóstico de viabilidad (ROI / fatiga cognitiva), checklist de la consigna y configuración exportada en texto |

![Lienzo checkpoint 6](checkpoint6_canvas.png)

## Cómo importar el checkpoint 6
1. En n8n: **Workflows → Import from File** y elegí `checkpoint6_S_Maureira.json`.
2. Instalá el nodo verificado de ElevenLabs (**Settings → Community nodes** → `@elevenlabs/n8n-nodes-elevenlabs`).
3. Asigná las credenciales en cada nodo: Telegram (token de @BotFather), OpenAI, Anthropic, Supabase, Google Sheets, ElevenLabs y Gmail.
4. En el nodo **RAG - Base de Conocimiento NEXA**, apuntá a la tabla vectorial del Módulo 5 (`documents` / `match_documents`).
5. Variables del servidor para compliance: `N8N_DEFAULT_BINARY_DATA_MODE=default` y `EXECUTIONS_DATA_PRUNE=true`.
