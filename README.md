# 📝 API RESTful de Gestión de Tareas (To-Do API)

Proyecto backend desarrollado con **Express 5**, **Prisma ORM 7** y base de datos relacional **PostgreSQL (Neon Serverless)**. Incluye un flujo CRUD completo, middlewares de auditoría y validación, junto a la arquitectura moderna de *Driver Adapters* introducida en Prisma 7.

---

## 📋 Tabla de Contenidos
1. [Requisitos Previos](#-requisitos-previos)
2. [Stack Tecnológico](#-stack-tecnol%C3%B3gico)
3. [Estructura del Proyecto](#-estructura-del-proyecto)
4. [Guía Paso a Paso](#-gu%C3%ADa-paso-a-paso-de-construcci%C3%B3n)
   - [Paso 1: Inicialización del Proyecto](#paso-1-inicializaci%C3%B3n-del-proyecto)
   - [Paso 2: Instalación de Dependencias](#paso-2-instalaci%C3%B3n-de-dependencias)
   - [Paso 3: Base de Datos y Variables de Entorno](#paso-3-base-de-datos-y-variables-de-entorno)
   - [Paso 4: Configuración de Prisma 7](#paso-4-configuraci%C3%B3n-de-prisma-7)
   - [Paso 5: Modelado de Datos (Prisma Schema)](#paso-5-modelado-de-datos-prisma-schema)
   - [Paso 6: Migración y Generación del Cliente](#paso-6-migraci%C3%B3n-y-generaci%C3%B3n-del-cliente)
   - [Paso 7: Servidor, Middlewares y Endpoints CRUD](#paso-7-servidor-middlewares-y-endpoints-crud)
5. [Ejecución del Servidor](#-ejecuci%C3%B3n-del-servidor)
6. [Pruebas de la API (Endpoints y Ejemplos)](#-pruebas-de-la-api)
7. [Inspección Visual con Prisma Studio](#-inspecci%C3%B3n-visual-con-prisma-studio)

---

## ⚙️ Requisitos Previos
Antes de iniciar, asegúrate de tener instalado en tu sistema:
- **Node.js**: Versión 18.x o superior (se recomienda 20.x o 22.x).
- **NPM**: Gestor de paquetes incluido con Node.js.
- **Cuenta en [Neon.tech](https://neon.tech)** (o cualquier instancia de PostgreSQL local o remota).

---

## 🛠️ Stack Tecnológico
- **Entorno de Ejecución:** [Node.js](https://nodejs.org/) (usando ES Modules: `import` / `export`).
- **Framework Web:** [Express 5](https://expressjs.com/).
- **ORM:** [Prisma v7](https://www.prisma.io/).
- **Driver Adapter:** `@prisma/adapter-pg` y driver `pg`.
- **Base de Datos:** [Neon PostgreSQL](https://neon.tech) (PostgreSQL Serverless en la nube con pooling de conexiones).
- **Gestión de Entorno:** `dotenv`.
- **Recarga en caliente:** `nodemon`.

---

## 📁 Estructura del Proyecto

```text
tareas-prisma/
├── prisma/
│   ├── migrations/                 # Historial de migraciones SQL generadas
│   │   └── 20260908195120_init/
│   │       └── migration.sql       # Script DDL de creación de la tabla "Tarea"
│   └── schema.prisma               # Definición declarativa del modelo de datos
├── .env                            # Credenciales y cadena de conexión a la BD
├── .gitignore                      # Exclusión de node_modules y .env
├── index.js                        # Código fuente del servidor, middlewares y rutas
├── package.json                    # Manifiesto de dependencias y scripts
├── prisma7.config.ts               # Archivo de configuración central de Prisma 7
└── Presentacion_Proyecto_Tareas_Prisma.pptx # Presentación explicativa
```

---

## 🚀 Guía Paso a Paso de Construcción

### Paso 1: Inicialización del Proyecto
1. Abre tu terminal y crea la carpeta del proyecto:
   ```bash
   mkdir tareas-prisma
   cd tareas-prisma
   ```
2. Genera el archivo `package.json`:
   ```bash
   npm init -y
   ```
3. Configura el proyecto para soportar **ES Modules** y define los scripts de ejecución en tu `package.json`:
   ```json
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
   ```

---

### Paso 2: Instalación de Dependencias

1. **Dependencias de Producción**:
   ```bash
   npm install express @prisma/client @prisma/adapter-pg pg dotenv
   ```
   * **`express`**: Framework web para crear la API y manejar rutas HTTP.
   * **`@prisma/client`**: Cliente generado para interactuar con la base de datos de manera tipada.
   * **`@prisma/adapter-pg`**: Adaptador oficial de Prisma 7 para PostgreSQL.
   * **`pg`**: Driver de PostgreSQL para Node.js requerido por el adaptador.
   * **`dotenv`**: Para cargar variables de entorno desde el archivo `.env`.

2. **Dependencias de Desarrollo**:
   ```bash
   npm install -D prisma nodemon
   ```
   * **`prisma`**: CLI para ejecutar migraciones y generar el cliente.
   * **`nodemon`**: Reinicia automáticamente el servidor al detectar cambios en el código.

---

### Paso 3: Base de Datos y Variables de Entorno

1. Inicia sesión en [Neon](https://neon.tech) y crea un nuevo proyecto Postgres.
2. Copia la cadena de conexión (*Connection String* con pooling activado).
3. En la raíz de tu proyecto, crea el archivo `.env`:
   ```env
   DATABASE_URL="postgresql://USUARIO:PASSWORD@ep-ejemplo-pooler.aws.neon.tech/neondb?sslmode=require"
   ```
4. Crea el archivo `.gitignore` para no subir tus credenciales a GitHub:
   ```text
   node_modules/
   .env
   ```

---

### Paso 4: Configuración de Prisma 7
En Prisma 7 la configuración principal del ORM se define en un archivo dedicado (`prisma7.config.ts`):

Crea el archivo `prisma7.config.ts` en la raíz del proyecto:
```typescript
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
});
```

---

### Paso 5: Modelado de Datos (Prisma Schema)
Crea la carpeta `prisma/` y dentro el archivo `schema.prisma`:

```prisma
// prisma/schema.prisma

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
}
```

* **`id`**: Clave primaria con incremento automático gestionado por la base de datos (`SERIAL`).
* **`descripcion`**: Texto obligatorio descriptivo de la tarea.
* **`completada`**: Booleano con valor predeterminado en `false`.

---

### Paso 6: Migración y Generación del Cliente
Aplica el modelo en la base de datos de Neon ejecutando en tu terminal:

```bash
npx prisma migrate dev --name init
```

Este comando realiza dos acciones clave:
1. Genera el script SQL en `prisma/migrations/` y lo ejecuta en Neon creando la tabla `Tarea`.
2. Genera automáticamente el cliente tipado de Prisma en `node_modules/@prisma/client`.

---

### Paso 7: Servidor, Middlewares y Endpoints CRUD
Crea el archivo `index.js` en la raíz con el siguiente contenido:

```javascript
import "dotenv/config";
import express from "express";
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "@prisma/client";

const app = express();

// 1. Inicialización del Driver Adapter de PostgreSQL para Prisma 7
const adapter = new PrismaPg({
    connectionString: process.env.DATABASE_URL
});

const prisma = new PrismaClient({
    adapter
});

// 2. Middlewares globales
app.use(express.json());

// Middleware de auditoría y logging
app.use((req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
});

// Middleware de validación para la creación de tareas
const validarDescripcion = (req, res, next) => {
    if (!req.body.descripcion) {
        return res.status(400).json({
            error: "La descripcion es un campo requerido"
        });
    }
    next();
};

// 3. Rutas CRUD

// GET /tareas - Obtener todas las tareas
app.get('/tareas', async (req, res) => {
    const tareas = await prisma.tarea.findMany();
    res.json(tareas);
});

// GET /tareas/:id - Obtener una tarea por su ID
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
});

// POST /tareas - Crear una nueva tarea
app.post('/tareas', validarDescripcion, async (req, res) => {
    const { descripcion } = req.body;
    const tarea = await prisma.tarea.create({
        data: {
            descripcion
        }
    });

    res.status(201).json(tarea);
});

// PUT /tareas/:id - Actualizar una tarea existente
app.put('/tareas/:id', async (req, res) => {
    const id = parseInt(req.params.id);
    const tareaExiste = await prisma.tarea.findUnique({
        where: { id }
    });

    if (!tareaExiste) {
        return res.status(404).json({
            error: "Tarea no encontrada"
        });
    }

    const { descripcion, completada } = req.body;

    const tarea = await prisma.tarea.update({
        where: { id },
        data: {
            ...(descripcion !== undefined && { descripcion }),
            ...(completada !== undefined && { completada })
        }
    });

    res.json(tarea);
});

// DELETE /tareas/:id - Eliminar una tarea por ID
app.delete('/tareas/:id', async (req, res) => {
    const id = parseInt(req.params.id);
    const tarea = await prisma.tarea.findUnique({
        where: { id }
    });

    if (!tarea) {
        return res.status(404).json({
            error: "Tarea no encontrada"
        });
    }

    await prisma.tarea.delete({
        where: { id }
    });

    res.json({
        mensaje: "Eliminada"
    });
});

// 4. Iniciar el servidor
app.listen(3000, () => {
    console.log("Servidor en el puerto 3000");
});
```

---

## 💻 Ejecución del Servidor

* **Modo Desarrollo (con recarga automática):**
  ```bash
  npm run dev
  ```
* **Modo Producción:**
  ```bash
  npm start
  ```

Al iniciar verás el mensaje:
```text
Servidor en el puerto 3000
```

---

## 🧪 Pruebas de la API

Puedes probar los endpoints utilizando herramientas como **Postman**, **Thunder Client** (extensión de VS Code) o comandos **cURL**:

### 1. Listar todas las tareas
* **Método:** `GET`
* **URL:** `http://localhost:3000/tareas`
* **Código de respuesta:** `200 OK`

### 2. Crear una nueva tarea
* **Método:** `POST`
* **URL:** `http://localhost:3000/tareas`
* **Headers:** `Content-Type: application/json`
* **Body:**
  ```json
  {
    "descripcion": "Estudiar para el examen de Aplicada 2"
  }
  ```
* **Código de respuesta:** `201 Created`

### 3. Probar validación de campo requerido (Error 400)
* **Método:** `POST`
* **URL:** `http://localhost:3000/tareas`
* **Body:** `{}`
* **Código de respuesta:** `400 Bad Request`
* **Respuesta:**
  ```json
  {
    "error": "La descripcion es un campo requerido"
  }
  ```

### 4. Consultar tarea por ID
* **Método:** `GET`
* **URL:** `http://localhost:3000/tareas/1`
* **Código de respuesta:** `200 OK` (o `404 Not Found` si no existe)

### 5. Actualizar estado de una tarea
* **Método:** `PUT`
* **URL:** `http://localhost:3000/tareas/1`
* **Headers:** `Content-Type: application/json`
* **Body:**
  ```json
  {
    "completada": true
  }
  ```
* **Código de respuesta:** `200 OK`

### 6. Eliminar una tarea
* **Método:** `DELETE`
* **URL:** `http://localhost:3000/tareas/1`
* **Código de respuesta:** `200 OK`
* **Respuesta:**
  ```json
  {
    "mensaje": "Eliminada"
  }
  ```

---

## 🖥️ Inspección Visual con Prisma Studio

Prisma incluye una interfaz gráfica web para consultar y manipular los datos de tu base de datos sin necesidad de instalar clientes externos como DBeaver o pgAdmin:

```bash
npx prisma studio
```

Abre tu navegador en `http://localhost:5555` para ver y editar registros en tiempo real.

---

## 📌 Resumen de Comandos Principales

| Acción | Comando |
|---|---|
| Instalar paquetes | `npm install` |
| Iniciar en modo desarrollo | `npm run dev` |
| Iniciar en producción | `npm start` |
| Crear y aplicar nueva migración | `npx prisma migrate dev --name <nombre>` |
| Abrir Prisma Studio (interfaz gráfica) | `npx prisma studio` |
| Validar esquema de Prisma | `npx prisma validate` |
| Regenerar cliente Prisma | `npx prisma generate` |
