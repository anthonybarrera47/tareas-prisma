import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    C_BG = RGBColor(15, 23, 42)
    C_CARD_BG = RGBColor(30, 41, 59)
    C_CARD_BORDER = RGBColor(51, 65, 85)
    C_CYAN = RGBColor(56, 189, 248)
    C_EMERALD = RGBColor(52, 211, 153)
    C_PURPLE = RGBColor(167, 139, 250)
    C_AMBER = RGBColor(251, 191, 36)
    C_TEXT_WHITE = RGBColor(248, 250, 252)
    C_TEXT_MUTED = RGBColor(148, 163, 184)
    C_TEXT_CODE = RGBColor(226, 232, 240)
    C_CODE_BG = RGBColor(10, 14, 23)

    def set_slide_background(slide):
        bg_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
        )
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = C_BG
        bg_shape.line.fill.background()
        return bg_shape

    def add_header(slide, title, category="GUÍA PASO A PASO"):
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category.upper()
        p_tag.font.name = "Segoe UI"
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_CYAN

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.name = "Segoe UI"
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = C_TEXT_WHITE

    def add_card(slide, left, top, width, height, bg=C_CARD_BG, border=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        if border:
            card.line.color.rgb = border
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    def add_code_box(slide, left, top, width, height, code_text):
        c_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = C_CODE_BG
        c_box.line.color.rgb = C_CARD_BORDER
        c_box.line.width = Pt(1)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        lines = code_text.strip().split("\n")
        for i, line in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = line
            p.font.name = "Consolas"
            p.font.size = Pt(10.5)
            clean_l = line.strip()
            if clean_l.startswith("//") or clean_l.startswith("#") or clean_l.startswith("--"):
                p.font.color.rgb = C_TEXT_MUTED
            elif any(clean_l.startswith(k) for k in ["import ", "export ", "const ", "let ", "app.", "model ", "datasource "]):
                p.font.color.rgb = C_CYAN
            elif any(clean_l.startswith(k) for k in ["return ", "if ", "await ", "async "]):
                p.font.color.rgb = C_PURPLE
            else:
                p.font.color.rgb = C_TEXT_CODE
        return c_box

    # Slide 1: Portada
    s1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s1)
    add_card(s1, Inches(0.8), Inches(1.2), Inches(11.733), Inches(5.1), bg=C_CARD_BG, border=C_CYAN)

    tb = s1.shapes.add_textbox(Inches(1.3), Inches(1.7), Inches(10.7), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "PROYECTO ACADÉMICO • PROGRAMACIÓN APLICADA II • UCNE"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    tb = s1.shapes.add_textbox(Inches(1.3), Inches(2.2), Inches(10.7), Inches(1.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "API RESTful con Express 5,\nPrisma ORM 7 y PostgreSQL (Neon)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_WHITE

    tb = s1.shapes.add_textbox(Inches(1.3), Inches(4.1), Inches(10.7), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Guía completa paso a paso: arquitectura, configuración moderna con Driver Adapters, modelado relacional, middlewares y operaciones CRUD."
    p.font.name = "Segoe UI"
    p.font.size = Pt(15)
    p.font.color.rgb = C_TEXT_MUTED

    badges = [
        ("Node.js (ESM)", C_EMERALD),
        ("Express v5", C_CYAN),
        ("Prisma ORM v7", C_PURPLE),
        ("Neon Serverless PG", C_AMBER),
        ("@prisma/adapter-pg", C_CYAN)
    ]
    bx = 1.3
    for text, col in badges:
        badge_shape = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(bx), Inches(5.15), Inches(1.95), Inches(0.5))
        badge_shape.fill.solid()
        badge_shape.fill.fore_color.rgb = C_CODE_BG
        badge_shape.line.color.rgb = col
        badge_shape.line.width = Pt(1.5)
        p = badge_shape.text_frame.paragraphs[0]
        p.text = text
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col
        bx += 2.1

    # Slide 2: Objetivos
    s2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s2)
    add_header(s2, "Visión General y Objetivos del Proyecto", "INTRODUCCIÓN")
    add_card(s2, Inches(0.8), Inches(1.65), Inches(5.7), Inches(5.2))
    tb = s2.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "¿Qué hace este proyecto?"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    points_left = [
        ("Servicio Backend RESTful:", " Provee una interfaz HTTP estructurada bajo los estándares REST para la administración de tareas pendientes."),
        ("Persistencia en la Nube:", " Se conecta a una base de datos PostgreSQL Serverless alojada en Neon Tech mediante SSL y pooling."),
        ("Prisma ORM 7 de Vanguardia:", " Utiliza la última versión de Prisma con Driver Adapters nativos (@prisma/adapter-pg)."),
        ("Validación y Auditoría:", " Incorpora middlewares personalizados para registro de solicitudes HTTP y validación de campos obligatorios.")
    ]
    for title, desc in points_left:
        p = tf.add_paragraph()
        p.space_before = Pt(12)
        run_t = p.add_run()
        run_t.text = "• " + title
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE
        run_t.font.size = Pt(13)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(12)

    add_card(s2, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2))
    tb = s2.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Capacidades que Desarrolla el Estudiante"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    points_right = [
        ("Configuración de Node.js Moderno:", " Migración a ES Modules (import/export) y automatización del ciclo de desarrollo con Nodemon."),
        ("Modelado Declarativo:", " Definición de esquemas de datos relacionales sin escribir SQL manual."),
        ("Ciclo de Vida de Migraciones:", " Creación, versionado y ejecución de scripts de migración DDL con Prisma Migrate."),
        ("Gestión de Respuestas HTTP:", " Uso correcto de códigos 200 OK, 201 Created, 400 Bad Request y 404 Not Found.")
    ]
    for title, desc in points_right:
        p = tf.add_paragraph()
        p.space_before = Pt(12)
        run_t = p.add_run()
        run_t.text = "✔ " + title
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE
        run_t.font.size = Pt(13)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(12)

    # Slide 3: Arquitectura
    s3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s3)
    add_header(s3, "Stack Tecnológico y Flujo Arquitectónico", "ARQUITECTURA DEL SISTEMA")
    techs = [
        ("Express 5.x", "Framework Web HTTP", "Enrutamiento modular, gestión de middlewares de logging y parseo nativo de JSON.", C_CYAN),
        ("Prisma ORM 7", "Capa de Acceso a Datos", "ORM declarativo con tipado estático, gestión de esquema y migraciones automatizadas.", C_PURPLE),
        ("@prisma/adapter-pg", "Driver Adapter Moderno", "Nuevo estándar en Prisma 7 para desacoplar el motor Rust y usar clientes SQL nativos.", C_EMERALD),
        ("Neon PostgreSQL", "Base de Datos en la Nube", "PostgreSQL Serverless, escalable, con soporte de pooling y conexiones TLS/SSL.", C_AMBER),
    ]
    for i, (t_name, t_cat, t_desc, color) in enumerate(techs):
        x = Inches(0.8 + i * 2.98)
        card = add_card(s3, x, Inches(1.65), Inches(2.78), Inches(3.2))
        tb = s3.shapes.add_textbox(x + Inches(0.2), Inches(1.85), Inches(2.38), Inches(2.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = t_cat.upper()
        p.font.name = "Segoe UI"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = color
        p2 = tf.add_paragraph()
        p2.text = t_name
        p2.space_before = Pt(4)
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT_WHITE
        p3 = tf.add_paragraph()
        p3.text = t_desc
        p3.space_before = Pt(8)
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(11)
        p3.font.color.rgb = C_TEXT_MUTED

    add_card(s3, Inches(0.8), Inches(5.1), Inches(11.733), Inches(1.75), bg=C_CODE_BG, border=C_CYAN)
    tb_flow = s3.shapes.add_textbox(Inches(1.1), Inches(5.25), Inches(11.133), Inches(1.45))
    tf_flow = tb_flow.text_frame
    tf_flow.word_wrap = True
    p_fl = tf_flow.paragraphs[0]
    p_fl.text = "FLUJO DE COMUNICACIÓN DE UNA PETICIÓN HTTP"
    p_fl.font.name = "Segoe UI"
    p_fl.font.size = Pt(11)
    p_fl.font.bold = True
    p_fl.font.color.rgb = C_CYAN
    p_fl2 = tf_flow.add_paragraph()
    p_fl2.space_before = Pt(6)
    p_fl2.text = "Cliente HTTP (Postman / Web)  ──▶  Middleware Express (Logger & Validador)  ──▶  Rutas CRUD (index.js)\n                                                                                                │\nBase de Datos PostgreSQL (Neon Cloud)  ◀──  Adapter Driver (@prisma/adapter-pg)  ◀──  Prisma Client"
    p_fl2.font.name = "Consolas"
    p_fl2.font.size = Pt(11)
    p_fl2.font.color.rgb = C_TEXT_CODE

    # Slide 4: Paso 1
    s4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s4)
    add_header(s4, "Paso 1: Inicialización del Proyecto Node.js", "PASO 01 / 11")
    add_card(s4, Inches(0.8), Inches(1.65), Inches(5.5), Inches(5.2))
    tb = s4.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(4.9), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Crear el entorno de desarrollo"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    steps_p1 = [
        ("1. Crear Directorio:", " Iniciar una nueva carpeta limpia en el sistema para albergar el proyecto (`mkdir tareas-prisma`)."),
        ("2. Inicializar package.json:", " Ejecutar `npm init -y` para generar el archivo de configuración estándar."),
        ("3. Configurar ES Modules:", " Agregar `\"type\": \"module\"` en el `package.json` para usar la sintaxis moderna `import/export`."),
        ("4. Scripts de Ejecución:", " Añadir scripts para desarrollo continuo con nodemon (`npm run dev`) y arranque normal (`npm start`).")
    ]
    for title, desc in steps_p1:
        p = tf.add_paragraph()
        p.space_before = Pt(10)
        run_t = p.add_run()
        run_t.text = title
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE
        run_t.font.size = Pt(13)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(12)

    code_p1 = """// package.json (Configuración Inicial)
{
  "name": "tareas-prisma",
  "version": "1.0.0",
  "main": "index.js",
  "type": "module",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js"
  }
}

// Comandos de terminal:
mkdir tareas-prisma
cd tareas-prisma
npm init -y"""
    add_code_box(s4, Inches(6.6), Inches(1.65), Inches(5.933), Inches(5.2), code_p1)

    # Slide 5: Paso 2
    s5 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s5)
    add_header(s5, "Paso 2: Instalación de Dependencias Clave", "PASO 02 / 11")
    add_card(s5, Inches(0.8), Inches(1.65), Inches(5.7), Inches(5.2))
    tb = s5.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Dependencias de Producción"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p_cmd1 = tf.add_paragraph()
    p_cmd1.text = "npm install express @prisma/client @prisma/adapter-pg pg dotenv"
    p_cmd1.space_before = Pt(8)
    p_cmd1.font.name = "Consolas"
    p_cmd1.font.size = Pt(10)
    p_cmd1.font.color.rgb = C_CYAN
    deps_prod = [
        ("express (v5.x):", " Framework principal para levantar el servidor web, rutas y middleware."),
        ("@prisma/client (v7.x):", " Cliente autogenerado fuertemente tipado para interactuar con la base de datos."),
        ("@prisma/adapter-pg:", " Adaptador oficial de Prisma 7 para enlazar con PostgreSQL."),
        ("pg:", " Driver oficial de PostgreSQL para Node.js."),
        ("dotenv:", " Carga automática de variables de entorno desde el archivo .env.")
    ]
    for title, desc in deps_prod:
        p = tf.add_paragraph()
        p.space_before = Pt(10)
        run_t = p.add_run()
        run_t.text = "• " + title
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE
        run_t.font.size = Pt(12)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(11)

    add_card(s5, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2))
    tb2 = s5.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "Dependencias de Desarrollo (-D)"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = C_PURPLE
    p_cmd2 = tf2.add_paragraph()
    p_cmd2.text = "npm install -D prisma nodemon"
    p_cmd2.space_before = Pt(8)
    p_cmd2.font.name = "Consolas"
    p_cmd2.font.size = Pt(10)
    p_cmd2.font.color.rgb = C_CYAN
    deps_dev = [
        ("prisma (v7.x):", " CLI encargada de gestionar migraciones, validar esquemas y generar clientes."),
        ("nodemon:", " Herramienta que monitorea cambios y reinicia el servidor automáticamente.")
    ]
    for title, desc in deps_dev:
        p = tf2.add_paragraph()
        p.space_before = Pt(12)
        run_t = p.add_run()
        run_t.text = "• " + title
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE
        run_t.font.size = Pt(13)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(12)

    # Slide 6: Paso 3
    s6 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s6)
    add_header(s6, "Paso 3: Base de Datos Neon y Variables de Entorno", "PASO 03 / 11")
    add_card(s6, Inches(0.8), Inches(1.65), Inches(5.5), Inches(5.2))
    tb = s6.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(4.9), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PostgreSQL Serverless con Neon"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    neon_points = [
        ("Registro Gratuito:", " Crear una cuenta en https://neon.tech e iniciar un nuevo proyecto de Postgres."),
        ("Connection Pooling:", " Neon provee endpoints con 'pooling' integrado, optimizando la cantidad de conexiones concurrentes."),
        ("Cifrado TLS/SSL Obligatorio:", " Requiere `sslmode=require` para transferencias seguras."),
        ("Buenas Prácticas de Seguridad:", " NUNCA incluir el archivo `.env` en repositorios públicos. Asegurarse de listarlo en `.gitignore`.")
    ]
    for title, desc in neon_points:
        p = tf.add_paragraph()
        p.space_before = Pt(12)
        run_t = p.add_run()
        run_t.text = "• " + title
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE
        run_t.font.size = Pt(12)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(11)

    code_env = """# Archivo: .env
# Cadena de conexión segura proporcionada por Neon:
DATABASE_URL="postgresql://usuario:password@ep-ejemplo-pooler.aws.neon.tech/neondb?sslmode=require"

# Archivo: .gitignore
node_modules/
.env"""
    add_code_box(s6, Inches(6.6), Inches(1.65), Inches(5.933), Inches(5.2), code_env)

    # Slide 7: Paso 4
    s7 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s7)
    add_header(s7, "Paso 4: Configuración Moderna con `prisma7.config.ts`", "PASO 04 / 11")
    add_card(s7, Inches(0.8), Inches(1.65), Inches(5.5), Inches(5.2))
    tb = s7.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(4.9), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "La Nueva Arquitectura de Prisma 7"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_PURPLE
    p_conf = [
        ("Configuración Programática:", " En Prisma 7, las opciones se configuran mediante código TypeScript/JavaScript (prisma7.config.ts)."),
        ("defineConfig():", " Helper con autocompletado y validación estricta de tipos."),
        ("Carga de Variables con dotenv:", " Se importa 'dotenv/config' para asegurar que env('DATABASE_URL') lea correctamente el archivo .env."),
        ("Rutas Explícitas:", " Define la ubicación exacta del esquema y del directorio de migraciones.")
    ]
    for title, desc in p_conf:
        p = tf.add_paragraph()
        p.space_before = Pt(10)
        run_t = p.add_run()
        run_t.text = "• " + title
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE
        run_t.font.size = Pt(12)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(11)

    code_p7 = """// prisma7.config.ts
import "dotenv/config";
import { defineConfig, env } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: {
    path: "prisma/migrations",
  },
  datasource: {
    url: env("DATABASE_URL"),
  },
});"""
    add_code_box(s7, Inches(6.6), Inches(1.65), Inches(5.933), Inches(5.2), code_p7)

    # Slide 8: Paso 5
    s8 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s8)
    add_header(s8, "Paso 5: Modelado de Datos Declarativo (`schema.prisma`)", "PASO 05 / 11")
    add_card(s8, Inches(0.8), Inches(1.65), Inches(5.5), Inches(5.2))
    tb = s8.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(4.9), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Estructura del Modelo 'Tarea'"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    model_fields = [
        ("id (Int):", " Identificador único. Con @id se marca como Clave Primaria y con @default(autoincrement()) se delega a la secuencia SERIAL de PostgreSQL."),
        ("descripcion (String):", " Texto obligatorio que detalla la tarea a realizar."),
        ("completada (Boolean):", " Estado booleano de la tarea con @default(false)."),
        ("generator client:", " Configura el generador del cliente JS de Prisma (prisma-client-js).")
    ]
    for title, desc in model_fields:
        p = tf.add_paragraph()
        p.space_before = Pt(12)
        run_t = p.add_run()
        run_t.text = "• " + title
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE
        run_t.font.size = Pt(12)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(11)

    code_schema = """// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
}

model Tarea {
  id          Int     @id @default(autoincrement())
  descripcion String
  completada  Boolean @default(false)
}"""
    add_code_box(s8, Inches(6.6), Inches(1.65), Inches(5.933), Inches(5.2), code_schema)

    # Slide 9: Paso 6
    s9 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s9)
    add_header(s9, "Paso 6: Migraciones de Base de Datos con Prisma Migrate", "PASO 06 / 11")
    add_card(s9, Inches(0.8), Inches(1.65), Inches(5.5), Inches(5.2))
    tb = s9.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(4.9), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "¿Qué es una Migración?"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    mig_points = [
        ("Comando Fundamental:", " `npx prisma migrate dev --name init`"),
        ("Generación de SQL DDL:", " Prisma detecta diferencias y genera un archivo .sql versionado con timestamp."),
        ("Ejecución Automática:", " Conecta a Neon Postgres y ejecuta la sentencia CREATE TABLE."),
        ("Actualización de Prisma Client:", " Genera automáticamente los tipos e interfaces en node_modules/@prisma/client.")
    ]
    for title, desc in mig_points:
        p = tf.add_paragraph()
        p.space_before = Pt(12)
        run_t = p.add_run()
        run_t.text = "• " + title
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE
        run_t.font.size = Pt(12)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(11)

    code_sql = """-- SQL generado automáticamente por Prisma Migrate:
-- prisma/migrations/20260908195120_init/migration.sql

CREATE TABLE "Tarea" (
    "id" SERIAL NOT NULL,
    "descripcion" TEXT NOT NULL,
    "completada" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "Tarea_pkey" PRIMARY KEY ("id")
);

-- Resultado en consola:
// ✔ Generated Prisma Client
// ✔ Applied migration `20260908195120_init`"""
    add_code_box(s9, Inches(6.6), Inches(1.65), Inches(5.933), Inches(5.2), code_sql)

    # Slide 10: Paso 7
    s10 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s10)
    add_header(s10, "Paso 7: Conexión del Servidor y Driver Adapter", "PASO 07 / 11")
    add_card(s10, Inches(0.8), Inches(1.65), Inches(5.5), Inches(5.2))
    tb = s10.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(4.9), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Integración Express + Prisma 7"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    init_points = [
        ("Cargar Variables:", " import 'dotenv/config' lee el archivo .env al arrancar."),
        ("Instanciar Adaptador PG:", " new PrismaPg({ connectionString: process.env.DATABASE_URL }) crea la conexión con el driver de PostgreSQL."),
        ("Inyectar Adaptador:", " Se pasa { adapter } al constructor de PrismaClient."),
        ("Parseo JSON:", " app.use(express.json()) habilita el análisis de payloads JSON en req.body.")
    ]
    for title, desc in init_points:
        p = tf.add_paragraph()
        p.space_before = Pt(12)
        run_t = p.add_run()
        run_t.text = "• " + title
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE
        run_t.font.size = Pt(12)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(11)

    code_init = """// index.js (Arranque y Conexión)
import "dotenv/config";
import express from "express";
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "@prisma/client";

const app = express();

const adapter = new PrismaPg({
    connectionString: process.env.DATABASE_URL
});

const prisma = new PrismaClient({ adapter });

app.use(express.json());"""
    add_code_box(s10, Inches(6.6), Inches(1.65), Inches(5.933), Inches(5.2), code_init)

    # Slide 11: Paso 8
    s11 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s11)
    add_header(s11, "Paso 8: Middlewares de Logging y Validación", "PASO 08 / 11")
    add_card(s11, Inches(0.8), Inches(1.65), Inches(5.7), Inches(5.2))
    tb1 = s11.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "1. Middleware de Logging Global"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = C_CYAN
    p_d1 = tf1.add_paragraph()
    p_d1.space_before = Pt(8)
    p_d1.text = "Audita cada petición imprimiendo marca de tiempo ISO, método HTTP y URL. Invoca next() para continuar el flujo."
    p_d1.font.name = "Segoe UI"
    p_d1.font.size = Pt(11)
    p_d1.font.color.rgb = C_TEXT_MUTED

    code_log = """app.use((req, res, next) => {
    console.log(
        `[${new Date().toISOString()}] ${req.method} ${req.url}`
    );
    next();
});"""
    tb_c1 = s11.shapes.add_textbox(Inches(1.1), Inches(3.2), Inches(5.1), Inches(3.3))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    for j, line in enumerate(code_log.split("\n")):
        p = tf_c1.paragraphs[0] if j == 0 else tf_c1.add_paragraph()
        p.text = line
        p.font.name = "Consolas"
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_CODE

    add_card(s11, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2))
    tb2 = s11.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "2. Middleware Validador de Datos"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = C_AMBER
    p_d2 = tf2.add_paragraph()
    p_d2.space_before = Pt(8)
    p_d2.text = "Filtro en rutas de creación. Si descripcion no existe o está vacía, devuelve HTTP 400 Bad Request."
    p_d2.font.name = "Segoe UI"
    p_d2.font.size = Pt(11)
    p_d2.font.color.rgb = C_TEXT_MUTED

    code_val = """const validarDescripcion = (req, res, next) => {
    if (!req.body.descripcion) {
        return res.status(400).json({
            error: "La descripcion es un campo requerido"
        });
    }
    next();
};"""
    tb_c2 = s11.shapes.add_textbox(Inches(7.1), Inches(3.2), Inches(5.1), Inches(3.3))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    for j, line in enumerate(code_val.split("\n")):
        p = tf_c2.paragraphs[0] if j == 0 else tf_c2.add_paragraph()
        p.text = line
        p.font.name = "Consolas"
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_CODE

    # Slide 12: Paso 9
    s12 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s12)
    add_header(s12, "Paso 9: Endpoints de Consulta (GET /tareas y GET /tareas/:id)", "PASO 09 / 11")
    add_card(s12, Inches(0.8), Inches(1.65), Inches(5.3), Inches(5.2))
    tb = s12.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(4.7), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Operaciones de Lectura (Read)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    get_points = [
        ("GET /tareas (Listar todas):", " Utiliza prisma.tarea.findMany() para obtener todas las filas en formato JSON."),
        ("GET /tareas/:id (Buscar por ID):", " Extrae el parámetro de la URL con req.params.id y lo convierte a entero con parseInt()."),
        ("findUnique():", " Busca la fila cuya clave primaria coincida con { where: { id } }."),
        ("Manejo de Errores 404:", " Si no existe (!tarea), retorna un código 404 Not Found con mensaje descriptivo.")
    ]
    for title, desc in get_points:
        p = tf.add_paragraph()
        p.space_before = Pt(10)
        run_t = p.add_run()
        run_t.text = "• " + title
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE
        run_t.font.size = Pt(12)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(11)

    code_get = """// GET todas las tareas
app.get('/tareas', async (req, res) => {
    const tareas = await prisma.tarea.findMany();
    res.json(tareas);
});

// GET tarea individual por ID
app.get('/tareas/:id', async (req, res) => {
    const id = parseInt(req.params.id);
    const tarea = await prisma.tarea.findUnique({
        where: { id }
    });

    if (!tarea) {
        return res.status(404).json({
            error: "Tarea no encontrada"
        });
    }

    res.json(tarea);
});"""
    add_code_box(s12, Inches(6.4), Inches(1.65), Inches(6.133), Inches(5.2), code_get)

    # Slide 13: Paso 10
    s13 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s13)
    add_header(s13, "Paso 10: Endpoints de Creación, Actualización y Eliminación", "PASO 10 / 11")
    add_card(s13, Inches(0.8), Inches(1.65), Inches(5.3), Inches(5.2))
    tb = s13.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(4.7), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Escritura, Actualización y Borrado"
    p.font.name = "Segoe UI"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    write_points = [
        ("POST /tareas (Crear):", " Protegido por validarDescripcion. Inserta con prisma.tarea.create() y responde con código 201 Created."),
        ("PUT /tareas/:id (Actualizar):", " Verifica existencia (404) y actualiza condicionalmente con spread (descripcion, completada)."),
        ("DELETE /tareas/:id (Eliminar):", " Verifica existencia y borra el registro con prisma.tarea.delete().")
    ]
    for title, desc in write_points:
        p = tf.add_paragraph()
        p.space_before = Pt(10)
        run_t = p.add_run()
        run_t.text = "• " + title
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE
        run_t.font.size = Pt(12)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(11)

    code_write = """// POST: Crear nueva tarea
app.post('/tareas', validarDescripcion, async (req, res) => {
    const { descripcion } = req.body;
    const tarea = await prisma.tarea.create({ data: { descripcion } });
    res.status(201).json(tarea);
});

// PUT: Actualización dinámica
app.put('/tareas/:id', async (req, res) => {
    const id = parseInt(req.params.id);
    const tareaExiste = await prisma.tarea.findUnique({ where: { id } });
    if (!tareaExiste) return res.status(404).json({ error: "Tarea no encontrada" });

    const { descripcion, completada } = req.body;
    const tarea = await prisma.tarea.update({
        where: { id },
        data: {
            ...(descripcion !== undefined && { descripcion }),
            ...(completada !== undefined && { completada })
        }
    });
    res.json(tarea);
});"""
    add_code_box(s13, Inches(6.4), Inches(1.65), Inches(6.133), Inches(5.2), code_write)

    # Slide 14: Paso 11
    s14 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s14)
    add_header(s14, "Paso 11: Pruebas de Endpoints y Códigos de Estado", "PASO 11 / 11")
    add_card(s14, Inches(0.8), Inches(1.65), Inches(11.733), Inches(5.2))
    tb = s14.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(11.1), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "Matriz de Verificación de Endpoints (Postman / Thunder Client / cURL)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    rows, cols = 6, 5
    table_shape = s14.shapes.add_table(rows, cols, Inches(1.1), Inches(2.45), Inches(11.133), Inches(3.2))
    table = table_shape.table
    table.columns[0].width = Inches(1.4)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(2.8)
    table.columns[3].width = Inches(1.6)
    table.columns[4].width = Inches(3.133)

    headers = ["Método", "Endpoint", "Cuerpo (JSON)", "Código HTTP", "Resultado Esperado"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_CODE_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_CYAN

    table_data = [
        ("GET", "/tareas", "Ninguno", "200 OK", "Lista completa de todas las tareas en JSON"),
        ("POST", "/tareas", '{"descripcion": "Aprender Prisma"}', "201 Created", "Crea la tarea y retorna el objeto con su nuevo ID"),
        ("POST", "/tareas", '{} (Sin descripción)', "400 Bad Request", "Rechaza la petición: 'La descripcion es requerida'"),
        ("GET", "/tareas/999", "Ninguno", "404 Not Found", "Indica que el recurso con dicho ID no existe"),
        ("PUT", "/tareas/1", '{"completada": true}', "200 OK", "Actualiza el estado de la tarea a completada"),
    ]
    for row_idx, row in enumerate(table_data, start=1):
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Consolas" if col_idx in [0, 1, 2, 3] else "Segoe UI"
            p.font.size = Pt(10)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_EMERALD if val in ["GET", "POST"] else C_AMBER
            elif col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = C_EMERALD if "20" in val else C_AMBER
            else:
                p.font.color.rgb = C_TEXT_WHITE if col_idx != 2 else C_TEXT_MUTED

    tb_tip = s14.shapes.add_textbox(Inches(1.1), Inches(5.8), Inches(11.1), Inches(0.8))
    p_tip = tb_tip.text_frame.paragraphs[0]
    p_tip.text = "💡 Herramienta Adicional: Ejecuta `npx prisma studio` en la consola para abrir una interfaz gráfica en el navegador (puerto 5555) donde puedes ver, editar y borrar registros en vivo."
    p_tip.font.name = "Segoe UI"
    p_tip.font.size = Pt(11)
    p_tip.font.color.rgb = C_AMBER

    # Slide 15: Conclusiones
    s15 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s15)
    add_header(s15, "Conclusiones y Recomendaciones Profesionales", "RESUMEN FINAL")
    add_card(s15, Inches(0.8), Inches(1.65), Inches(5.7), Inches(5.2))
    tb1 = s15.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Logros de la Arquitectura Implementada"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = C_EMERALD
    logros = [
        ("Desacoplamiento Efectivo:", " Separación clara entre enrutamiento, middlewares, capa ORM y base de datos."),
        ("Prisma 7 Ready:", " Adopción de adaptadores desacoplados de alto rendimiento."),
        ("Cero Servidores Locales:", " Integración con Neon Postgres en la nube."),
        ("Control de Errores y Validaciones:", " Flujo estructurado con códigos de estado HTTP estándar.")
    ]
    for title, desc in logros:
        p = tf1.add_paragraph()
        p.space_before = Pt(12)
        run_t = p.add_run()
        run_t.text = "✔ " + title
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE
        run_t.font.size = Pt(12)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(11)

    add_card(s15, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2))
    tb2 = s15.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "Propuestas para Escalar el Proyecto"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = C_CYAN
    mejoras = [
        ("Adopción Completa de TypeScript:", " Tipar de extremo a extremo las solicitudes y respuestas."),
        ("Validación con Zod:", " Reemplazar validaciones manuales por esquemas Zod con parsing automático."),
        ("Middleware Global de Manejo de Errores:", " Capturar excepciones en un middleware centralizado."),
        ("Autenticación y Autorización:", " Implementar JWT para control de acceso por usuario.")
    ]
    for title, desc in mejoras:
        p = tf2.add_paragraph()
        p.space_before = Pt(12)
        run_t = p.add_run()
        run_t.text = "🚀 " + title
        run_t.font.bold = True
        run_t.font.color.rgb = C_TEXT_WHITE
        run_t.font.size = Pt(12)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = C_TEXT_MUTED
        run_d.font.size = Pt(11)

    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    output_file = os.path.join(os.getcwd(), "Presentacion_Proyecto_Tareas_Prisma.pptx")
    build_presentation(output_file)
