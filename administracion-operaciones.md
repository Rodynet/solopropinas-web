# Requerimiento para Administración y Operaciones

Versión: 2 de agosto de 2026.

## Antes de contratar al PSP

- Definir un solo proveedor principal para la etapa 5: debe resolver alias, CBU y CVU, validar titularidad contra KYC, acreditar la propina directamente y soportar la separación de importes del modelo SoloPropinas.
- No contratar una integración distinta para Mercado Pago, Ualá, Naranja X o MODO: son posibles destinos de acreditación o medios de pago, cuya cobertura debe confirmar el proveedor principal.
- Solicitar al proveedor la descripción contractual de su acceso a la red interoperable aplicable para resolver alias/CBU/CVU (por ejemplo, COELSA mediante una entidad adherida), incluidos campos devueltos, cobertura, límites y tratamiento de datos.
- Exigir ambiente de prueba para validar: alias existente e inexistente, CBU/CVU, entidad, titular enmascarado, coincidencia y no coincidencia de titularidad, cuenta no habilitada y tiempos de respuesta.
- Verificar razón social, CUIT, función y registro aplicable ante BCRA.
- Confirmar por contrato que la propina se acredita directamente al trabajador.
- Exigir separación entre propina, servicio SoloPropinas, impuestos y costos del PSP.
- Confirmar APIs, webhooks, conciliación, reversos, contracargos, fraude, SLA e incidentes.
- Obtener contactos operativos, técnicos, legales y de atención al usuario.
- Validar que Mercado Pago, Naranja X, Ualá y wallet del celular estén realmente disponibles mediante la integración elegida.

## Antes de habilitar facturación

- Definir condición fiscal de SoloPropinas, punto de venta y tipos de comprobante.
- Contratar o implementar facturación electrónica integrada con ARCA.
- Aprobar reglas de Consumidor Final e identificación obligatoria según importe y normativa vigente.
- Aprobar impuestos, redondeo, numeración, almacenamiento y entrega del PDF.
- Definir el procedimiento para solicitar factura con otros datos fiscales.
- Definir notas de crédito, nueva facturación, devoluciones y reversos.

## Operación diaria

- Conciliar órdenes, webhooks, acreditaciones, servicio, costos, impuestos y facturas.
- Revisar automáticamente diferencias y asignar un número de incidencia.
- Atender pagos pendientes, rechazados, duplicados, revertidos o desconocidos.
- Verificar facturas en preparación o rechazadas por ARCA.
- Resolver solicitudes de cambio de datos fiscales conservando trazabilidad.
- Controlar vencimientos de contratos, certificados, credenciales y SLA.

## Evidencia mínima por operación

- Orden interna e idempotencia.
- Consentimiento y versión de términos.
- Identificadores del PSP y estados recibidos.
- Importe de propina, servicio 5%, impuestos y total.
- Evidencia de acreditación al trabajador.
- Factura SoloPropinas y comprobante del PSP.
- Reclamos, reversos, ajustes y responsables.

## Regla de escalamiento

Una diferencia de dinero, identidad, acreditación o factura no se corrige directamente en la base de datos. Se abre una incidencia, se preserva la evidencia y se resuelve mediante el procedimiento aprobado por Administración, Legales y Desarrollo.
