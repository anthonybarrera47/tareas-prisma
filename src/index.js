import "dotenv/config";
import express from "express";
import { loggerMiddleware } from "./middlewares/logger.middleware.js";
import tareasRoutes from "./routes/tareas.routes.js";

const app = express();
const PORT = process.env.PORT || 3000;

// Middlewares globales
app.use(express.json());
app.use(loggerMiddleware);

// Rutas modulares
app.use("/tareas", tareasRoutes);

// Ruta base informativa
app.get("/", (req, res) => {
    res.json({
        mensaje: "API RESTful de Tareas con Express 5 y Prisma 7",
        estado: "En línea",
        documentacion: {
            "GET /tareas": "Listar todas las tareas",
            "GET /tareas/:id": "Obtener tarea por ID",
            "POST /tareas": "Crear nueva tarea ({ descripcion })",
            "PUT /tareas/:id": "Actualizar tarea ({ descripcion, completada })",
            "DELETE /tareas/:id": "Eliminar tarea"
        }
    });
});

app.listen(PORT, () => {
    console.log(`Servidor en el puerto ${PORT}`);
});
