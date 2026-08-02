from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, HRFlowable
)
from pypdf import PdfReader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output/pdf/auditoria-integral-solopropinas-2026.pdf"

pdfmetrics.registerFont(TTFont("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))

GREEN = colors.HexColor("#39A96B")
DARK = colors.HexColor("#151515")
CREAM = colors.HexColor("#F7F3EC")
MINT = colors.HexColor("#E6F5ED")
RED = colors.HexColor("#B83A3A")
AMBER = colors.HexColor("#B06B00")
BLUE = colors.HexColor("#285F85")
GREY = colors.HexColor("#626262")
LIGHT = colors.HexColor("#E5E0D8")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleSP", fontName="Arial-Bold", fontSize=28, leading=31, textColor=DARK, spaceAfter=10))
styles.add(ParagraphStyle(name="SubTitleSP", fontName="Arial", fontSize=12, leading=17, textColor=GREY, spaceAfter=12))
styles.add(ParagraphStyle(name="H1SP", fontName="Arial-Bold", fontSize=18, leading=22, textColor=DARK, spaceBefore=4, spaceAfter=10))
styles.add(ParagraphStyle(name="H2SP", fontName="Arial-Bold", fontSize=13, leading=16, textColor=DARK, spaceBefore=8, spaceAfter=6))
styles.add(ParagraphStyle(name="BodySP", fontName="Arial", fontSize=9.2, leading=13, textColor=DARK, spaceAfter=6))
styles.add(ParagraphStyle(name="SmallSP", fontName="Arial", fontSize=7.4, leading=10, textColor=GREY, spaceAfter=3))
styles.add(ParagraphStyle(name="CalloutSP", fontName="Arial-Bold", fontSize=11, leading=15, textColor=DARK, backColor=MINT, borderColor=GREEN, borderWidth=0.6, borderPadding=10, spaceBefore=6, spaceAfter=10))
styles.add(ParagraphStyle(name="ScoreSP", fontName="Arial-Bold", fontSize=30, leading=34, textColor=GREEN, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="TableHeadSP", fontName="Arial-Bold", fontSize=7.2, leading=9, textColor=colors.white))
styles.add(ParagraphStyle(name="TableSP", fontName="Arial", fontSize=7.1, leading=9, textColor=DARK))
styles.add(ParagraphStyle(name="TableBoldSP", fontName="Arial-Bold", fontSize=7.2, leading=9, textColor=DARK))

def P(text, style="BodySP"):
    return Paragraph(text, styles[style])

def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(DARK)
    canvas.rect(0, h-12*mm, w, 12*mm, fill=1, stroke=0)
    canvas.setFont("Arial-Bold", 8)
    canvas.setFillColor(colors.white)
    canvas.drawString(18*mm, h-7.5*mm, "SoloPropinas · Auditoría integral 2026")
    canvas.setFont("Arial", 7)
    canvas.setFillColor(GREY)
    canvas.drawString(18*mm, 9*mm, "Informe independiente de coherencia regulatoria, tributaria, UX y arquitectura de producto")
    canvas.drawRightString(w-18*mm, 9*mm, f"{doc.page}")
    canvas.restoreState()

def section(title, subtitle=None):
    parts = [P(title, "H1SP")]
    if subtitle: parts.append(P(subtitle, "SubTitleSP"))
    parts.append(HRFlowable(width="100%", thickness=1.2, color=GREEN, spaceAfter=8))
    return parts

def bullet(text):
    return P("• " + text)

def severity(label):
    color = {"ALTO": RED, "MEDIO": AMBER, "BAJO": BLUE}[label]
    return Paragraph(f'<font color="{color.hexval()}"><b>{label}</b></font>', styles["TableBoldSP"])

story = []
story += [Spacer(1, 28*mm), P("AUDITORÍA INTEGRAL", "SubTitleSP"), P("SoloPropinas", "TitleSP"),
          P("Coherencia regulatoria, tributaria, contractual, UX y arquitectura de producto", "SubTitleSP"), Spacer(1, 9*mm),
          P('Tesis rectora: “SoloPropinas es una plataforma tecnológica para trabajadores de servicios. La propina electrónica constituye una funcionalidad dentro del ecosistema y no el objeto exclusivo del servicio.”', "CalloutSP"),
          Spacer(1, 8*mm)]

cover = Table([
    [P("Fecha de corte", "TableBoldSP"), P("2 de agosto de 2026", "TableSP")],
    [P("Jurisdicción", "TableBoldSP"), P("República Argentina", "TableSP")],
    [P("Comité", "TableBoldSP"), P("Product Owner · UX · Fintech/medios de pago · Derecho del consumidor · Tributación ARCA · Arquitectura de producto", "TableSP")],
    [P("Evidencia", "TableBoldSP"), P("Historial del proyecto; landing pública solopropinas.com; repositorio conectado Rodynet/solopropinas-web; normativa y sitios oficiales", "TableSP")],
], colWidths=[40*mm, 112*mm])
cover.setStyle(TableStyle([("BACKGROUND",(0,0),(0,-1),MINT),("GRID",(0,0),(-1,-1),0.4,LIGHT),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
story += [cover, Spacer(1, 13*mm), P("Documento de trabajo estratégico. No sustituye un dictamen legal, tributario o regulatorio emitido sobre la operatoria definitiva y los contratos ejecutados.", "SmallSP"), PageBreak()]

story += section("1. Resumen ejecutivo", "Diagnóstico de lanzamiento y decisión recomendada")
story += [P("SoloPropinas tiene una intuición de producto sólida —identidad permanente del trabajador separada de la cuenta de destino— y una landing clara y convincente. Sin embargo, la comunicación pública actual presenta el producto casi exclusivamente como mecanismo para cobrar propinas y anuncia un descuento del 0,7% sobre cada propina. Ambas decisiones debilitan la tesis rectora y elevan el riesgo regulatorio, tributario, laboral y de defensa del consumidor."),
          P("La situación no exige abandonar el producto. Exige rediseñar la arquitectura jurídica y económica antes de habilitar pagos reales: SoloPropinas debe cobrar por una prestación tecnológica independiente, con factura propia, sin descontar ni retener fondos de la propina y sin tomar posesión de ellos. El pago debe fluir desde el cliente al trabajador mediante un PSP/adquirente/agregador regulado; SoloPropinas debe limitarse a identidad, perfil, reputación, herramientas, analítica y orquestación técnica."),
          P("DECISIÓN RECOMENDADA: NO habilitar cobros reales ni comunicar disponibilidad operativa hasta cerrar el modelo PSP, contratos, facturación, privacidad, seguridad y evidencia de acreditación. Sí continuar con prototipo, validación de mercado y desarrollo bajo un 'gated launch'.", "CalloutSP")]

score_tbl = Table([
    [P("40/100", "ScoreSP"), P("Preparación global actual", "H2SP"), P("Alto riesgo / corregible", "H2SP")],
    [P("68", "TableBoldSP"), P("UX y claridad", "TableSP"), P("Fortaleza relativa", "TableSP")],
    [P("42", "TableBoldSP"), P("Coherencia con tesis", "TableSP"), P("Requiere reposicionamiento", "TableSP")],
    [P("38", "TableBoldSP"), P("Regulación de pagos", "TableSP"), P("Arquitectura no acreditada", "TableSP")],
    [P("35", "TableBoldSP"), P("Tributación y facturación", "TableSP"), P("Modelo 0,7% crítico", "TableSP")],
    [P("30", "TableBoldSP"), P("Consumidor y contratos", "TableSP"), P("Legales ausentes/no operativos", "TableSP")],
    [P("40", "TableBoldSP"), P("Privacidad y seguridad", "TableSP"), P("Promesas sin controles demostrables", "TableSP")],
    [P("36", "TableBoldSP"), P("Arquitectura de producto", "TableSP"), P("Concepto definido; implementación no evidenciada", "TableSP")],
    [P("32", "TableBoldSP"), P("Due diligence", "TableSP"), P("Repositorio incompleto y falta data room", "TableSP")],
], colWidths=[28*mm,58*mm,66*mm])
score_tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),MINT),("GRID",(0,0),(-1,-1),0.4,LIGHT),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
story += [Spacer(1,4*mm), score_tbl, PageBreak()]

story += section("2. Alcance, evidencia y límites")
story += [P("Se revisó el historial disponible del proyecto, incluyendo posicionamiento, monetización, QR permanente, onboarding, página pública del trabajador, reputación, panel, seguridad y funciones futuras. Se inspeccionó la landing pública vigente en solopropinas.com el 2/8/2026 y el repositorio conectado Rodynet/solopropinas-web."),
          P("La landing contiene una experiencia demostrativa completa, pero los CTA remiten a anclas sin alta funcional; el pie muestra 'Términos', 'Privacidad', 'Legales' y 'Contacto' como texto no enlazado. El repositorio informado posee un index.html vacío en la rama principal y no exhibe, mediante la conexión disponible, documentación, contratos, arquitectura, controles o código de la landing desplegada. Por ello, la ausencia de evidencia se califica como riesgo de preparación, no como prueba definitiva de inexistencia."),
          P("No se auditaron credenciales, acuerdos privados con PSP, estados contables, alta societaria, CUIT, inscripción fiscal, base de datos productiva, código backend, pentest ni contratos firmados porque no fueron aportados. Las conclusiones sobre BCRA y ARCA dependen de la operatoria efectiva; deberán confirmarse con asesoramiento local antes del lanzamiento."),
          P("Criterio de severidad: ALTO = puede impedir lanzamiento, afectar fondos del trabajador, inducir encuadre regulado o generar sanciones; MEDIO = exposición relevante que admite mitigación de corto plazo; BAJO = mejora de robustez, prueba o claridad."), PageBreak()]

story += section("3. Tesis rectora y arquitectura objetivo")
story += [P("La tesis es defendible únicamente si se manifiesta en cuatro capas simultáneas:"),
          bullet("Producto: identidad, perfil profesional, reputación, herramientas y beneficios tienen valor autónomo; la propina es una funcionalidad."),
          bullet("Dinero: SoloPropinas no recibe, custodia, distribuye ni compensa fondos. El PSP regulado acredita directamente en la cuenta del trabajador."),
          bullet("Contrato y factura: SoloPropinas presta y factura tecnología. La propina no integra su precio, base de facturación ni ingreso."),
          bullet("Comunicación: nunca 'vendemos propinas', 'cobramos por la propina' o garantizamos acreditación; explicamos roles y dependencia del PSP."),
          P("Arquitectura recomendada", "H2SP")]

arch = Table([
    [P("Capa", "TableHeadSP"), P("Responsable", "TableHeadSP"), P("Regla de diseño", "TableHeadSP")],
    [P("Identidad y QR", "TableBoldSP"), P("SoloPropinas", "TableSP"), P("QR permanente resuelve al perfil; no contiene CBU/CVU fijo ni credenciales.", "TableSP")],
    [P("Pago", "TableBoldSP"), P("PSP/adquirente/agregador", "TableSP"), P("Orden y acreditación directa trabajador ↔ PSP. SoloPropinas no toca fondos.", "TableSP")],
    [P("Servicio", "TableBoldSP"), P("SoloPropinas", "TableSP"), P("Perfil, reputación, seguridad, analítica, soporte y herramientas independientes.", "TableSP")],
    [P("Precio", "TableBoldSP"), P("SoloPropinas", "TableSP"), P("Abono/plan o cargo separado facturado; nunca deducido del monto de la propina.", "TableSP")],
    [P("Datos", "TableBoldSP"), P("Roles documentados", "TableSP"), P("Minimización, finalidades, consentimiento, encargados, retención y derechos.", "TableSP")],
], colWidths=[32*mm,43*mm,77*mm])
arch.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),DARK),("GRID",(0,0),(-1,-1),0.4,LIGHT),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
story += [arch, PageBreak()]

findings = [
 ("F01","Landing / posicionamiento","ALTO","El hero, navegación y casi todas las secciones describen exclusivamente propinas digitales.","Un regulador o inversor puede considerar que la tesis de plataforma es ex post y que el objeto real es intermediar propinas.","Reescribir hero y arquitectura de navegación: 'Tu identidad profesional, reputación y herramientas de trabajo, con propinas digitales integradas'. Incorporar módulos de perfil, reputación, beneficios y carrera antes de precio."),
 ("F02","Monetización 0,7%","ALTO","'Solo se descuenta un pequeño porcentaje de cada propina recibida'.","El DNU 731/2024 dispone que la propina es liberalidad directa del trabajador y prohíbe retenciones/percepciones por participantes del sistema; el descuento puede parecer apropiación o retención.","Eliminar descuento sobre la propina. Cobrar plan tecnológico separado (mensual, freemium o por funciones), emitir factura y no netear contra el pago. Validar tratamiento contractual y fiscal."),
 ("F03","Flujo de fondos / BCRA","ALTO","No se acredita quién procesa, inicia, agrega, administra QR o custodia fondos.","Según la operatoria real, SoloPropinas podría ser caracterizada como PSP, iniciador, agregador o administrador QR y requerir registro/supervisión.","Diseño direct-to-worker mediante PSP regulado; matriz RACI de pagos; opinión legal de encuadre; contrato de integración; diagrama de fondos y mensajes que identifiquen al PSP."),
 ("F04","Promesa 'al instante'","ALTO","Se afirma repetidamente acreditación inmediata sin condición.","Publicidad potencialmente engañosa si existen demoras, rechazos, mantenimiento, contracargos o validaciones del PSP.","Cambiar por 'el PSP procesa y acredita según sus tiempos y condiciones'; mostrar estado pendiente/acreditado/rechazado y comprobante trazable."),
 ("F05","Propiedad de la propina","ALTO","La pantalla dice 'Dejar propina a Juan', pero precio y operación no separan jurídicamente fondos y servicio.","Juez/ARCA pueden mirar sustancia económica: base porcentual y descuento implican mezcla de ingresos.","En checkout: 'Propina voluntaria para Juan: $X'; 'Servicio SoloPropinas: $Y' solo si corresponde y en transacción/documento separado; cuenta de destino nominada y confirmada."),
 ("F06","Términos y legales","ALTO","Términos, Privacidad y Legales aparecen sin enlaces operativos.","Falla del deber de información; contratos no incorporados; ausencia de identificación del proveedor, jurisdicción, reclamos y reglas del servicio.","Publicar T&C versionados, política de privacidad, cookies, baja, contacto, CUIT/razón social/domicilio y rol del PSP; aceptación granular y prueba de versión."),
 ("F07","CTA y disponibilidad","MEDIO","'Crear mi cuenta' y 'Empezá hoy' sugieren servicio disponible, pero remiten a anclas vacías.","Riesgo de expectativa falsa y baja confianza; due diligence detecta prototipo presentado como operación.","Etiquetar 'Sumarme a la lista de espera' o habilitar onboarding real. Distinguir demo, beta y producción."),
 ("F08","Onboarding/KYC","ALTO","El flujo histórico propone Google/Apple, WhatsApp, fotos, local y cuenta de cobro, sin identidad legal ni titularidad robusta.","Suplantación, redireccionamiento de propinas y exposición ante reclamos; validación por SMS no equivale a identidad.","Verificar identidad y mayoría de edad; titularidad CBU/CVU; consentimiento del trabajador; reautenticación y demora/cooldown para cambiar destino; alertas fuera de banda."),
 ("F09","Fotos y privacidad","MEDIO","Se promueven fotos familiares y personales como elemento de conversión.","Puede involucrar datos de terceros y menores, usos incompatibles y exposición innecesaria.","Fotos laborales como default; consentimiento de terceros; prohibir/limitar imágenes de menores; controles de visibilidad, borrado y moderación."),
 ("F10","Reseñas y reputación","MEDIO","Se anuncian estrellas, comentarios, historial y prestigio sin reglas.","Datos reputacionales inexactos pueden afectar honor, trabajo y relación con el local; riesgo de manipulación o discriminación.","Política de reseñas verificadas, réplica, denuncia, moderación, caducidad y portabilidad; separar reseña del trabajador y del establecimiento."),
 ("F11","Relación laboral/local","MEDIO","'Sin depender del local' y reputación vinculada al establecimiento no definen autorización ni obligaciones.","Conflictos con empleador, uso de marca, políticas internas y distribución colectiva; un juez puede evaluar control o injerencia.","Declaración de independencia laboral, consentimiento para asociar local, canal de disputa y modo individual/equipo claramente diferenciado."),
 ("F12","Facturación e impuestos","ALTO","No existe evidencia de alta fiscal, comprobantes ni segregación contable.","ARCA puede tratar el 0,7% como ingreso por servicio o intermediación y analizar la base bruta si los flujos se mezclan.","Factura electrónica por el servicio tecnológico; cuentas contables separadas; conciliación PSP; no facturar la propina; memo IVA/IIBB/Ganancias y regímenes de información/percepción."),
 ("F13","Seguridad y evidencia","ALTO","La landing promete validaciones extra, notificaciones y soporte, pero no hay evidencia técnica.","Promesa contractual incumplida; fraude en cambio de cuenta; débil trazabilidad ante juez o inversor.","MFA/reautenticación, cooldown, doble aviso, logs inmutables, control de sesiones, cifrado, respuesta a incidentes, backups y pruebas independientes."),
 ("F14","Repositorios y gobierno","MEDIO","El repositorio conectado muestra index.html vacío y no coincide con la landing desplegada.","Due diligence no puede reproducir el producto ni verificar propiedad intelectual, historial, dependencias o despliegue.","Repositorio canónico; pipeline reproducible; README, arquitectura, licencias, inventario de activos IA, control de secretos, tags y correspondencia commit-deploy."),
 ("F15","Funciones futuras","MEDIO","Pozo compartido, equipos y multilocal se anuncian sin reglas de titularidad/distribución.","Aumentan sustancialmente custodia, mandato, controversias laborales y riesgo PSP.","Mantenerlas como roadmap no operativo; antes de construir, definir quién decide reparto, cuenta recaudadora especial, plazos, auditoría y acuerdo del equipo/local."),
 ("F16","Baja, reclamos y reversos","ALTO","No se ven cancelación, baja, devolución por error, reclamo o soporte identificable.","Defensa del consumidor puede cuestionar información, trato digno y mecanismos de salida; el usuario queda sin remedio frente a un pago erróneo.","Centro de ayuda; baja en línea; número de reclamo; SLA; matriz de reversos y pagos equivocados coordinada con PSP; conservación probatoria."),
]

story += section("4. Matriz priorizada de hallazgos", "Hallazgos observables y correcciones concretas")
for idx, (fid, elem, sev, hall, risk, rec) in enumerate(findings):
    block = Table([
        [P(fid, "TableHeadSP"), P(elem, "TableHeadSP"), severity(sev)],
        [P("Hallazgo", "TableBoldSP"), P(hall, "TableSP"), ""],
        [P("Riesgo / lectura probable", "TableBoldSP"), P(risk, "TableSP"), ""],
        [P("Modificación", "TableBoldSP"), P(rec, "TableSP"), ""],
    ], colWidths=[35*mm,96*mm,21*mm])
    block.setStyle(TableStyle([("BACKGROUND",(0,0),(1,0),DARK),("BACKGROUND",(2,0),(2,0),CREAM),("SPAN",(1,1),(2,1)),("SPAN",(1,2),(2,2)),("SPAN",(1,3),(2,3)),("GRID",(0,0),(-1,-1),0.4,LIGHT),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    story += [KeepTogether([block, Spacer(1,3.5*mm)])]
story.append(PageBreak())

story += section("5. Lectura por autoridad y por inversor")
views = [
 ("BCRA","No decide por el marketing sino por las funciones efectivas. Si SoloPropinas define reglas de pago, inicia órdenes, administra QR interoperable, agrega comercios o recibe fondos, puede quedar dentro de categorías registrables. La mitigación es contractual y técnica: PSP regulado, flujo directo y matriz de roles."),
 ("ARCA","Separará la liberalidad del trabajador del ingreso empresarial. Un porcentaje descontado del monto puede ser evidencia de comisión/intermediación y contaminar base, facturación y regímenes de percepción. Debe existir factura propia del servicio y contabilidad segregada."),
 ("Defensa del Consumidor","Observará promesas de gratuidad, inmediatez, seguridad, precio, identidad del proveedor, términos accesibles, baja y reclamos. La información pública integra la oferta y puede ser exigible."),
 ("Juez civil/laboral","Analizará sustancia, trazabilidad y control: quién recibió el dinero, quién podía redirigirlo, cómo se obtuvo consentimiento, qué se prometió y si existía relación o autorización del establecimiento."),
 ("Inversor / comprador","Penalizará la contradicción entre tesis y unit economics, dependencia de terceros no contratada, inexistencia de data room, repositorio no reproducible, ausencia de contratos y riesgo de reclasificación como PSP."),
]
for title, textv in views:
    story += [P(title, "H2SP"), P(textv)]
story += [PageBreak()]

story += section("6. Rediseño de textos y navegación")
copy_tbl = Table([
 [P("Elemento", "TableHeadSP"),P("Actual", "TableHeadSP"),P("Propuesta", "TableHeadSP")],
 [P("Hero", "TableBoldSP"),P("Cobra sí o sí tus propinas", "TableSP"),P("Tu trabajo merece identidad, reconocimiento y mejores herramientas", "TableSP")],
 [P("Subhero", "TableBoldSP"),P("Propinas digitales en segundos", "TableSP"),P("Creá tu perfil profesional y activá propinas digitales con acreditación directa en tu cuenta", "TableSP")],
 [P("Promesa", "TableBoldSP"),P("Vos recibís la plata al instante", "TableSP"),P("El proveedor de pago procesa la propina y la acredita en la cuenta que verificaste", "TableSP")],
 [P("Precio", "TableBoldSP"),P("Se descuenta 0,7% de cada propina", "TableSP"),P("SoloPropinas cobra por herramientas tecnológicas. Tu propina no se descuenta ni se mezcla con el precio del servicio", "TableSP")],
 [P("CTA beta", "TableBoldSP"),P("Crear mi cuenta gratis", "TableSP"),P("Sumarme a la beta" if True else "", "TableSP")],
 [P("Checkout", "TableBoldSP"),P("¿Cuánto querés dejarle?", "TableSP"),P("Propina voluntaria para Juan · El monto pertenece a Juan · Procesado por [PSP]", "TableSP")],
], colWidths=[31*mm,52*mm,69*mm])
copy_tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),DARK),("GRID",(0,0),(-1,-1),0.4,LIGHT),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
story += [copy_tbl, Spacer(1,5*mm), P("Orden de navegación recomendado", "H2SP"),
          P("Producto → Perfil profesional → Reputación → Herramientas → Propinas digitales → Seguridad → Planes → Ayuda → Legales. El orden evidencia valor tecnológico autónomo y mantiene la propina como funcionalidad, sin esconderla."),
          P("Regla de consistencia", "H2SP"),
          P("Toda pantalla debe responder: (1) quién presta el servicio; (2) a quién pertenece el dinero; (3) quién procesa el pago; (4) qué cobra SoloPropinas; (5) cómo reclamar; (6) qué dato se usa y por qué."), PageBreak()]

story += section("7. Contratos, privacidad y facturación mínima")
story += [P("Paquete contractual previo a beta con dinero real", "H2SP"),
          bullet("Términos del trabajador: licencia tecnológica, precio, facturación, uso aceptable, propiedad del perfil/QR, baja, PSP, disputas y ausencia de relación laboral."),
          bullet("Términos del pagador/cliente: voluntariedad y monto, destinatario, procesamiento por tercero, errores, reclamos, datos mínimos y comprobante."),
          bullet("Acuerdo con PSP: roles regulatorios, onboarding/KYC, liquidación directa, conciliación, reversos, fraude, SLA, incidentes y subencargados."),
          bullet("Política de privacidad: responsable, finalidades, bases, destinatarios, transferencias, conservación, seguridad, derechos y canal AAIP."),
          bullet("Políticas de contenido/reseñas, consentimiento de imagen, cookies y marketing."),
          P("Modelo fiscal recomendado", "H2SP"),
          P("La propina se registra como monto ajeno y no como venta de SoloPropinas. El ingreso de SoloPropinas es el precio del servicio tecnológico, documentado con factura electrónica según su condición fiscal y la del destinatario. Debe definirse el tratamiento de IVA, Ingresos Brutos, Ganancias, regímenes de retención/percepción y facturación masiva con asesor tributario. La exención del impuesto sobre débitos y créditos del Decreto 737/2024 se refiere a cuentas recaudadoras especiales bajo el esquema normativo; no debe extrapolarse automáticamente a cualquier cuenta de SoloPropinas."),
          P("Control contable esencial", "H2SP"),
          P("Conciliar por separado: propina ordenada, propina acreditada al trabajador, comisión/costo del PSP, precio del servicio SoloPropinas, impuesto y factura. Si SoloPropinas no toca fondos, la conciliación usa identificadores y estados del PSP, no una cuenta puente propia."), PageBreak()]

story += section("8. Arquitectura funcional y controles")
controls = [
 ("QR permanente","Token aleatorio no predecible; resolución servidor; revocación; sin CBU/CVU embebido."),
 ("Destino de cobro","Titularidad verificada; cambio con reautenticación, cooldown, alerta al canal anterior y nuevo; bloqueo de emergencia."),
 ("Pago","PSP regulado; idempotencia; estados; comprobante; webhook firmado; sin custodia SoloPropinas."),
 ("Identidad","Verificación proporcional al riesgo; mayoría de edad; prevención de duplicados y suplantación."),
 ("Privacidad","Minimización; separación público/privado; consentimientos; borrado; retención; control de fotos y reseñas."),
 ("Auditoría","Logs inmutables para cambios de cuenta, identidad, consentimientos, publicaciones y pagos."),
 ("Operaciones","Soporte trazable, respuesta a incidentes, continuidad, recuperación, monitoreo y métricas de fraude."),
 ("Gobierno","Registro de decisiones; owner por riesgo; revisión legal de cambios en dinero, precio, QR y reparto."),
]
ct = Table([[P("Control", "TableHeadSP"),P("Requisito mínimo", "TableHeadSP")]] + [[P(a,"TableBoldSP"),P(b,"TableSP")] for a,b in controls], colWidths=[40*mm,112*mm])
ct.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),DARK),("GRID",(0,0),(-1,-1),0.4,LIGHT),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
story += [ct, PageBreak()]

story += section("9. Plan de remediación y criterios de salida")
road = [
 ("0-15 días","Congelar promesas de operación; cambiar CTA; retirar 0,7%; publicar identidad institucional y legales básicos; definir owner legal/regulatorio."),
 ("15-45 días","Elegir PSP y cerrar matriz de roles/flujo de fondos; memo BCRA y tributario; contratos; modelo de facturación; diseño KYC y cambio de cuenta."),
 ("45-90 días","Implementar onboarding, aceptación versionada, estados de pago, conciliación, soporte, privacidad, logs y controles; pruebas de fraude y seguridad."),
 ("Antes de beta","Verificar 100% acreditación directa en pruebas; factura separada; comprobante; baja/reclamo; incident response; pentest; data room y despliegue reproducible."),
 ("Post-beta","Medir conversión, errores, tiempos PSP, fraude, reclamos, baja, reputación y costo de soporte; revisión trimestral de normativa y contratos."),
]
rt = Table([[P("Horizonte", "TableHeadSP"),P("Acciones", "TableHeadSP")]]+[[P(a,"TableBoldSP"),P(b,"TableSP")] for a,b in road], colWidths=[34*mm,118*mm])
rt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),DARK),("GRID",(0,0),(-1,-1),0.4,LIGHT),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
story += [rt, Spacer(1,5*mm), P("Go / No-Go", "H2SP"),
          P("GO limitado: landing reposicionada, lista de espera, prototipo sin movimiento de dinero, entrevistas y pruebas moderadas."),
          P("NO-GO: pagos reales, deducción porcentual de propinas, pozo compartido, promesas de acreditación inmediata o lanzamiento público sin PSP/contratos/facturación/controles."), PageBreak()]

story += section("10. Nota evaluatoria final y conclusión")
story += [P("40/100", "ScoreSP"), P("Madurez estratégica: PROMETEDORA, PERO NO APTA PARA LANZAMIENTO TRANSACCIONAL", "CalloutSP"),
          P("La propuesta resuelve una fricción real, la experiencia es comprensible y el principio 'el QR representa a la persona' es una base arquitectónica fuerte. No obstante, el producto visible hoy narra una empresa de propinas, no una plataforma tecnológica para trabajadores; monetiza directamente sobre la propina y carece de evidencia contractual, fiscal y técnica suficiente. Ese desajuste es material en una due diligence y puede afectar la lectura de BCRA, ARCA, Defensa del Consumidor y un juez."),
          P("La corrección es viable y no exige sacrificar conversión. Al contrario: separar claramente la propina, el procesador y el servicio tecnológico aumenta confianza. La recomendación del comité es rediseñar primero la economía y el flujo de fondos; luego alinear landing, onboarding, checkout, contratos, facturas y registros técnicos. Con esos hitos verificados, el proyecto podría subir a una banda estimada de 75-82/100 y quedar en condiciones de beta controlada."),
          P("Conclusión", "H2SP"),
          P("SoloPropinas debe avanzar, pero como plataforma tecnológica con pagos integrados por terceros, nunca como comercializador, custodio o descontador de propinas. La propina debe permanecer íntegra, identificable y atribuida al trabajador; el precio de SoloPropinas debe ser separado, transparente y facturado. Esa decisión es el punto de inflexión que protege la tesis, la escalabilidad y la valuación futura."), PageBreak()]

story += section("11. Fuentes oficiales y trazabilidad")
sources = [
 ("DNU 731/2024 - Propinas", "https://www.argentina.gob.ar/normativa/nacional/decreto-731-2024-402820/texto", "Liberalidad directa; no remunerativa; voluntariedad; prohibición de retenciones/percepciones; acreditación y cuentas especiales."),
 ("Decreto 737/2024", "https://www.argentina.gob.ar/normativa/nacional/decreto-737-2024-402912/texto", "Exención del impuesto a débitos/créditos para cuentas recaudadoras especiales bajo el esquema del DNU 731/2024."),
 ("BCRA - Texto ordenado Proveedores de Servicios de Pago", "https://bcra.gob.ar/Pdfs/Texord/t-snp-psp.pdf", "Funciones dentro de esquemas de pago minorista y categorías regulatorias."),
 ("BCRA - Registro de PSP", "https://www.bcra.gob.ar/registro-de-proveedores-de-servicios-de-pago/", "Categorías: cuentas de pago, aceptador, administrador QR, iniciador, adquirente y agregador."),
 ("Ley 24.240 - Defensa del Consumidor", "https://www.argentina.gob.ar/normativa/nacional/ley-24240-638/actualizacion", "Deber de información, oferta, contratación a distancia, protección y reclamos."),
 ("Código Civil y Comercial", "https://www.argentina.gob.ar/normativa/nacional/ley-26994-235975/actualizacion", "Contratos de consumo a distancia e información sobre medios electrónicos."),
 ("Ley 25.326 - Datos Personales", "https://www.argentina.gob.ar/normativa/nacional/ley-25326-64790/actualizacion", "Licitud, calidad, información, consentimiento, seguridad y derechos de titulares."),
 ("ARCA - Facturación y comprobantes", "https://www.arca.gob.ar/facturacion/comprobantes/fe-vs-cf.asp", "Obligación y modalidades de facturación electrónica."),
 ("ARCA - Régimen general de comprobantes", "https://www.arca.gob.ar/facturacion/regimen-general/comprobantes.asp", "Clases de comprobantes según emisor y receptor."),
 ("ARCA - Operaciones en plataformas digitales", "https://arca.gob.ar/economia-digital/operaciones-plataformas-digitales/determinacion.asp", "Referencia para analizar bases de percepción, precios y comisiones; aplicabilidad a confirmar según operatoria."),
]
for i,(name,url,use) in enumerate(sources,1):
    story += [KeepTogether([P(f"<b>{i}. {name}</b>", "SmallSP"), P(f'<link href="{url}" color="#285F85">{url}</link>', "SmallSP"), P(use, "SmallSP"), Spacer(1,1.5*mm)])]
story += [Spacer(1,4*mm), P("Trazabilidad de producto", "H2SP"),
          P("Landing pública revisada: https://solopropinas.com/ (2/8/2026). Repositorio conectado revisado: Rodynet/solopropinas-web, rama principal. Historial: conversación 'Mi Propina Proyecto', con definiciones de monetización 0,7%, QR permanente, onboarding, reputación, panel y roadmap."),
          P("Metodología y cautela", "H2SP"),
          P("Las fuentes se consultaron en sitios oficiales. Las inferencias regulatorias se presentan como evaluación de riesgo, no como afirmación de encuadre definitivo. El encuadre depende de contratos, APIs, titularidad de cuentas, instrucciones de pago, tiempos de acreditación y control efectivo de fondos."),
          P("Fin del informe", "SmallSP")]

doc = BaseDocTemplate(str(OUT), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=20*mm, bottomMargin=16*mm, title="Auditoría Integral SoloPropinas 2026", author="Comité multidisciplinario")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=header_footer)])
doc.build(story)

reader = PdfReader(str(OUT))
assert len(reader.pages) >= 12, f"PDF inesperadamente corto: {len(reader.pages)} páginas"
print(f"{OUT}|pages={len(reader.pages)}")
