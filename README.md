# Proyecto integrador n8n — S. Maureira

| Checkpoint | Archivo | Contenido |
|---|---|---|
| 1 | `checkpoint1_S_Maureira.json` | Agente base de calificación de leads (Chat Trigger + AI Agent + Google Sheets + log en Gmail) |
| 4 | `checkpoint4_S_Maureira.json` | Sincronización del cerebro agéntico con el ecosistema e-commerce (Gmail vía OAuth2; HubSpot y Slack vía tokens con permisos acotados) |

## Checkpoint 4: Sincronización del Cerebro Agéntico con Ecosistemas de Negocio

Flujo:

```
Gmail Trigger (casilla de soporte, no leídos, sin adjuntos)
   │
① IF ¿es auto-reply? ── Sí ─▶ Stop (corta el bucle infinito)
   │ No
AI Agent (Claude + memoria por hilo + salida estructurada)
   │
④ Set: limpia el payload (From, Subject, BodyText recortado y salida de la IA)
   │
IF ¿email válido? ── No ─▶ Stop (evita el 400)
   │ Sí
② Look up en HubSpot por email
   ├── existe ─▶ HubSpot Update contacto
   └── no     ─▶ HubSpot Create contacto        (evita el 409)
   │
③ Gmail Create Draft: borrador para aprobación humana (HITL)
   │
Set: payload mínimo (sin cuerpo ni binarios)
   │
Slack: aviso en #operaciones
```

### Controles que evalúa la rúbrica
1. **IF anti auto-reply**, justo después del trigger. Descarta asuntos con *Auto-reply*, *Automatic reply*, *Out of office*, *Undeliverable*, *Delivery Status Notification*, *Respuesta automática* y *Fuera de la oficina*, y remitentes `no-reply`, `noreply`, `mailer-daemon` o `postmaster`. No distingue mayúsculas de minúsculas.
2. **Look up antes de Create**: busca el contacto en HubSpot (`email EQ From`) y ramifica en Update o Create.
3. **Create Draft**: el workflow solo crea borradores en el mismo hilo y nunca envía correos.
4. **Set de limpieza**: deja solo los campos necesarios. Además, un IF valida el formato del email antes de llamar al CRM.

### Mínimo privilegio (scopes)
- **Gmail**: `gmail.readonly` para el trigger y `gmail.compose` para crear borradores. No se pide `gmail.send`.
- **HubSpot** (clave de servicio): `crm.objects.contacts.read` y `crm.objects.contacts.write`.
- **Slack** (Bot Token Scopes): `chat:write` y `channels:read`.

### Cómo importarlo
1. En n8n, ir a *Workflows › Import from File* y elegir `checkpoint4_S_Maureira.json`.
2. Reemplazar las credenciales de ejemplo (`REPLACE_WITH_...`) por las propias: Gmail OAuth2, HubSpot App Token (clave de servicio de HubSpot), Slack API (Bot Token `xoxb-`) y Anthropic. En n8n local, HubSpot ya no permite crear apps OAuth "anteriores" y Slack no acepta el redirect `http://localhost`, por eso esos dos usan tokens con scopes acotados. Hay que confirmar que cada una quede en verde.
3. Elegir el canal de Slack (por defecto `#operaciones`).
4. Hacer el test de regresión con *Execute Workflow* y *Test step* en cada nodo.
