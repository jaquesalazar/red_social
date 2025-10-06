# Lineamientos de Seguridad — Red Social

## Principios
- Principio de menor privilegio (cada cuenta solo tiene los permisos necesarios).
- Defensa en profundidad: controles en varias capas (aplicación, host, red).
- Privacidad desde el diseño: mínima recolección y anonimización cuando sea posible.
- Registro y trazabilidad de accesos y eventos de seguridad.

## Control de acceso
- Definir roles claros: admin / moderador / usuario.
- Validar tokens y permisos en el servidor para cada endpoint.
- Implementar autenticación multifactor (MFA) para cuentas administrativas.
- Revisiones periódicas de permisos (cada 30–90 días).

## Políticas de contraseñas
- Recomendado: mínimo 12 caracteres o passphrase.
- No almacenar contraseñas en texto plano; usar hashing seguro (Argon2id o bcrypt).
- Implementar bloqueo temporal tras múltiples intentos fallidos y rate limiting.
- Recuperación de cuenta mediante tokens de un solo uso que expiran.

## Acceso y validación de datos
- Validación siempre en servidor (no confiar en la validación cliente).
- Usar consultas parametrizadas / prepared statements (evitar inyección SQL/NoSQL).
- Proteger contra XSS mediante escape de salida y Content Security Policy (CSP).
- Proteger endpoints que cambian estado contra CSRF.
- Control y validación estrica de uploads (tipo MIME, tamaño, renombrado, ubicaciones seguras).

## Gestión de dependencias y vulnerabilidades
- Escaneo automático de dependencias (Dependabot, Snyk) y actualización periódica.
- Integrar análisis estático y dinámico en CI (SAST/DAST).

## Seguridad del servidor y despliegue
- Forzar HTTPS (Let’s Encrypt u otro CA), habilitar HSTS.
- Firewall (ufw) y protección SSH (usar llaves, desactivar root login).
- Monitoreo y recolección de logs (alertas sobre accesos anómalos).
- Backups cifrados y pruebas periódicas de restauración.
- Gestionar secretos fuera del repo (variables de entorno o secret manager).

## Procedimiento en caso de incidente
- Identificar y contener el incidente.
- Preservar evidencia (logs).
- Notificar a responsables internos y, si aplica, a usuarios afectados.
- Revisar y ajustar controles para evitar recurrencias.
