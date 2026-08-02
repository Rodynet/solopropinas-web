# Arquitectura de pagos, integración PSP y facturación

Versión funcional: 2 de agosto de 2026. Este documento define requerimientos para Administración, Legales y Desarrollo. La implementación final requiere validación tributaria, contractual y regulatoria antes de operar.

## 1. Principio de fondos

1. El cliente elige una propina voluntaria para un trabajador identificado.
2. SoloPropinas informa por separado:
   - propina voluntaria;
   - servicio SoloPropinas inicial del 5% de la propina;
   - impuestos aplicables al servicio;
   - total a pagar;
   - importe íntegro que recibirá el trabajador.
3. El cliente acepta esos importes y elige Mercado Pago, Naranja X, Ualá o la wallet disponible en su celular.
4. El proveedor de pagos procesa la operación y acredita la propina directamente en la cuenta verificada del trabajador.
5. SoloPropinas recibe únicamente el precio de su servicio. No recibe, custodia, compensa, distribuye ni descuenta la propina.
6. SoloPropinas factura solamente su servicio. La propina no integra sus ingresos ni su factura.

## 2. Modelo obligatorio de integración con el PSP

La integración obligatoria es una única autorización del cliente con asignaciones separadas o *split payment*. El flujo técnico debe ser:

1. SoloPropinas calcula en backend propina, servicio del 5%, impuestos y total.
2. El cliente autoriza el total una sola vez en el medio elegido.
3. El PSP crea y registra simultáneamente dos asignaciones:

- asignación 1: propina completa a la cuenta verificada del trabajador;
- asignación 2: servicio del 5% e impuestos a la cuenta de SoloPropinas;
- costos del PSP: registro separado según contrato, sin reducir la propina mostrada;
- identificadores y conciliación separados para cada concepto y acreditación.

4. El webhook informa el estado de la operación y de cada asignación.
5. SoloPropinas marca “acreditada” únicamente cuando verifica la asignación de la propina al trabajador.

El PSP debe demostrar contractualmente y mediante pruebas que SoloPropinas nunca toma posesión de la propina. Si un proveedor no admite acreditación directa, separación de conceptos, estados verificables, reversos y conciliación, no es compatible con este modelo.

Una implementación con dos cobros independientes solo puede evaluarse como alternativa después de revisar fricción, doble autorización, costos, reversos, comprobantes y encuadre legal. No se implementará por decisión técnica unilateral.

Mercado Pago, Naranja X, Ualá y la wallet del celular son opciones de pago visibles para el cliente. Su disponibilidad real depende de que el PSP contratado y el dispositivo permitan la integración correspondiente. No deben mostrarse opciones no operativas.

## 3. Responsabilidades del PSP

- Estar inscripto o habilitado para la función que efectivamente presta y figurar en los registros aplicables del BCRA.
- Verificar identidad, mayoría de edad y titularidad de la cuenta del trabajador cuando corresponda.
- Crear la orden, solicitar autorización y devolver un identificador único.
- Informar estados mediante API y webhooks firmados.
- Acreditar directamente la propina en la cuenta verificada del trabajador.
- Separar el servicio SoloPropinas y los costos propios según el contrato.
- Gestionar rechazo, cancelación, expiración, reverso, devolución y contracargo.
- Proveer comprobante o referencia de pago y datos para conciliación.
- Informar tiempos, soporte, SLA, incidentes y responsables de atención al usuario.

## 4. Requerimientos para Desarrollo

### 4.1 Creación de la orden

El backend calcula los importes. El navegador nunca define el 5% ni el total definitivo.

La orden debe registrar como mínimo:

- `payment_order_id` interno e inmutable;
- `idempotency_key` por intento;
- trabajador, perfil y cuenta de destino verificada;
- propina, porcentaje vigente, servicio, impuestos y total;
- moneda;
- proveedor y medio elegido;
- identificadores de orden, pago, asignación y acreditación del PSP;
- versión de términos, consentimiento, fecha, IP y dispositivo;
- estados de pago, acreditación, factura y conciliación.

### 4.2 Estados

- `created`: orden creada, todavía no enviada.
- `authorization_pending`: el cliente está autorizando.
- `pending`: el PSP aceptó la orden pero aún no confirmó resultado.
- `accredited`: webhook verificado confirma la acreditación.
- `rejected`: el PSP rechazó la operación.
- `cancelled`: el cliente o el sistema canceló antes de acreditar.
- `reversed`: se revirtió una operación acreditada.
- `refunded`: devolución completada cuando corresponda.

Abrir una wallet, volver a SoloPropinas o recibir un parámetro del navegador nunca equivale a éxito. El estado acreditado solo se muestra luego de verificar el webhook o consultar directamente la API del PSP.

### 4.3 Seguridad y consistencia

- TLS, secretos fuera del código y rotación de credenciales.
- Firma y validación de webhooks, protección contra repetición y lista de eventos aceptados.
- Idempotencia en creación, reintento y procesamiento de eventos.
- Cálculo monetario con enteros en la unidad mínima y reglas de redondeo documentadas.
- Registro de auditoría sin datos financieros sensibles.
- No almacenar credenciales, tokens de wallet ni datos de tarjeta.
- Reconciliación automática diaria y alerta por diferencias.
- Reintentos controlados y cola de eventos para caídas temporales.

### 4.4 Interfaces mínimas

- Crear orden y devolver opciones realmente disponibles.
- Iniciar el proveedor elegido mediante SDK, API o enlace seguro.
- Recibir y verificar webhooks.
- Consultar estado y detalle de la operación.
- Descargar comprobante del PSP cuando exista.
- Descargar factura de SoloPropinas.
- Solicitar corrección de datos fiscales por el procedimiento legal definido.
- Abrir reclamo con número de caso y vincularlo a orden, pago y factura.

## 5. Factura de SoloPropinas

### 5.1 Qué se factura

SoloPropinas emite factura electrónica exclusivamente por el servicio del 5% y sus impuestos. La propina debe aparecer únicamente como referencia informativa y nunca como concepto facturado por SoloPropinas.

### 5.2 Emisión predeterminada

- La emisión inicial será a **Consumidor Final**, cuando la normativa y el importe lo permitan.
- Se deben aplicar las reglas de identificación del receptor vigentes al momento de emitir.
- La factura se genera solo cuando el pago del servicio queda confirmado.
- La factura debe quedar vinculada al `payment_order_id`, al identificador del PSP y al comprobante de pago.
- Guardar tipo, punto de venta, número, CAE/CAEA, vencimiento, fecha, moneda, neto, impuestos, total y estado.

### 5.3 Entrega y descarga

Después de la confirmación se muestran dos documentos distintos:

1. **Ver detalle o comprobante del pago**, emitido o referenciado por el PSP.
2. **Descargar factura de SoloPropinas**, correspondiente únicamente al servicio.

El vínculo de descarga debe aparecer en:

- pantalla de operación acreditada;
- detalle de la operación;
- historial de comprobantes enviado por correo cuando el cliente lo informe.

El archivo debe poder descargarse en PDF y conservar una representación verificable de los datos autorizados por ARCA. Si la factura todavía se está generando, mostrar “Factura en preparación” y notificar cuando esté disponible.

### 5.4 Factura con datos distintos de Consumidor Final

Junto al vínculo de descarga se mostrará:

> La factura se emite a Consumidor Final. Si necesitás una factura con otros datos fiscales, consultá el procedimiento en Información legal y facturación.

El vínculo dirige a `legales.html#facturacion`. Allí se explica:

- datos requeridos: nombre o razón social, CUIT, condición frente al IVA, domicilio fiscal y correo;
- plazo y canal para solicitar el cambio;
- validación de los datos;
- que una factura ya autorizada no se edita directamente;
- que Administración definirá, según el caso y la normativa vigente, si corresponde nota de crédito y nueva factura u otro comprobante de ajuste.

No se promete un cambio automático. Toda corrección debe conservar trazabilidad entre la factura original, el ajuste y la nueva factura.

## 6. Requerimientos para Administración y Operaciones

- Seleccionar PSP por función regulada, inscripción, contrato, split, seguridad, costos, SLA, soporte, reversos y evidencia de acreditación directa.
- Mantener matriz RACI entre SoloPropinas y PSP para autorización, fraude, soporte, reversos, conciliación e incidentes.
- Definir condición fiscal, punto de venta, tipo de comprobante, impuestos, redondeo y proveedor de facturación electrónica.
- Conciliar diariamente órdenes, propinas acreditadas, servicio cobrado, costos PSP, impuestos, facturas y fondos recibidos por SoloPropinas.
- Resolver excepciones: orden sin webhook, acreditación sin factura, factura sin pago, diferencia de importes, duplicado, reverso y contracargo.
- Atender solicitudes de factura con otros datos fiscales y conservar evidencia de validación.
- Publicar identidad legal, CUIT, domicilio, contacto, canales de reclamo y procedimiento de facturación.
- Mantener contratos, términos y políticas versionados con evidencia de aceptación.
- Definir conservación documental y acceso restringido según finalidad.

## 7. Conciliación obligatoria

Cada operación debe permitir comprobar:

`orden = autorización PSP = propina acreditada + servicio cobrado + impuestos + costos PSP = factura emitida`

Las diferencias generan una incidencia automática. No se cierran manualmente sin motivo, responsable, evidencia y fecha.

## 8. Criterios de aceptación

- El trabajador recibe el 100% de la propina informada.
- SoloPropinas recibe y factura únicamente su servicio.
- El cliente ve porcentaje, importe, impuestos y total antes de aceptar.
- Solo se muestran medios de pago operativos.
- Ningún éxito depende únicamente del retorno del navegador.
- Webhooks duplicados no duplican pagos, facturas ni acreditaciones.
- La factura a Consumidor Final queda disponible para descarga.
- Existe un vínculo visible para solicitar factura con otros datos fiscales.
- Administración puede conciliar orden, PSP, acreditación, servicio y factura.
- Todo reverso o ajuste conserva trazabilidad completa.

## 9. Bloqueantes de lanzamiento

No activar pagos hasta completar: PSP contratado y verificado en registros aplicables; opinión legal y tributaria; modelo de acreditación directa probado; facturación electrónica; contratos; términos; privacidad; soporte; conciliación; fraude; SLA; incidentes; pruebas de seguridad; reversos y descarga de comprobantes.
