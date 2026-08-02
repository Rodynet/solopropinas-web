# Arquitectura de pagos y facturación

Versión de diseño: 2 de agosto de 2026. Requiere validación legal, tributaria y contractual antes de producción.

## Flujo de fondos

1. El cliente elige una propina voluntaria para un trabajador identificado.
2. SoloPropinas muestra dos conceptos separados: propina y servicio tecnológico.
3. El PSP regulado procesa la orden. La propina se acredita directamente en la cuenta verificada del trabajador.
4. SoloPropinas no utiliza una cuenta puente ni toma posesión de la propina.
5. El cliente paga el servicio SoloPropinas en concepto separado. SoloPropinas emite el comprobante fiscal correspondiente únicamente por ese servicio.

## Roles

- Trabajador: titular de la propina y de la cuenta de destino verificada.
- Cliente: decide libremente la propina y contrata el servicio tecnológico informado.
- PSP: procesa, informa estados, acredita, rechaza y coordina reversos.
- SoloPropinas: identidad, perfil, reputación, herramientas, seguridad, soporte, analítica y orquestación técnica.

## Reglas técnicas

- Idempotencia por intento de pago.
- Webhooks firmados y verificación del estado del PSP.
- Estados: creado, pendiente, acreditado, rechazado, cancelado, revertido.
- Comprobante trazable con identificadores separados para propina y servicio.
- Conciliación separada de propina ordenada, acreditada, costo PSP, precio SoloPropinas, impuesto y factura.
- Ningún éxito se muestra por el solo hecho de abrir una billetera.

## Bloqueantes

No activar pagos hasta identificar PSP, cerrar matriz RACI, opinión de encuadre BCRA, contrato de integración, modelo fiscal, comprobantes, reversos, fraude, SLA, incidentes y evidencia de acreditación directa.
