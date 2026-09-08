import { prisma } from "../db.js";

// GET /tareas - Obtener todas las tareas
export const obtenerTareas = async (req, res) => {
    try {
        const tareas = await prisma.tarea.findMany();
        res.json(tareas);
    } catch (error) {
        console.error("Error al obtener tareas:", error);
        res.status(500).json({
            error: "Error interno del servidor al consultar las tareas"
        });
    }
};

// GET /tareas/:id - Obtener una tarea por ID
export const obtenerTareaPorId = async (req, res) => {
    try {
        const id = parseInt(req.params.id);

        if (isNaN(id)) {
            return res.status(400).json({
                error: "El parámetro ID debe ser un número entero válido"
            });
        }

        const tarea = await prisma.tarea.findUnique({
            where: { id }
        });

        if (!tarea) {
            return res.status(404).json({
                error: "Tarea no encontrada"
            });
        }

        res.json(tarea);
    } catch (error) {
        console.error("Error al buscar tarea por ID:", error);
        res.status(500).json({
            error: "Error interno del servidor al buscar la tarea"
        });
    }
};

// POST /tareas - Crear una nueva tarea
export const crearTarea = async (req, res) => {
    try {
        const { descripcion } = req.body;

        const tarea = await prisma.tarea.create({
            data: {
                descripcion
            }
        });

        res.status(201).json(tarea);
    } catch (error) {
        console.error("Error al crear tarea:", error);
        res.status(500).json({
            error: "Error interno del servidor al crear la tarea"
        });
    }
};

// PUT /tareas/:id - Actualizar una tarea existente
export const actualizarTarea = async (req, res) => {
    try {
        const id = parseInt(req.params.id);

        if (isNaN(id)) {
            return res.status(400).json({
                error: "El parámetro ID debe ser un número entero válido"
            });
        }

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
    } catch (error) {
        console.error("Error al actualizar tarea:", error);
        res.status(500).json({
            error: "Error interno del servidor al actualizar la tarea"
        });
    }
};

// DELETE /tareas/:id - Eliminar una tarea por ID
export const eliminarTarea = async (req, res) => {
    try {
        const id = parseInt(req.params.id);

        if (isNaN(id)) {
            return res.status(400).json({
                error: "El parámetro ID debe ser un número entero válido"
            });
        }

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
    } catch (error) {
        console.error("Error al eliminar tarea:", error);
        res.status(500).json({
            error: "Error interno del servidor al eliminar la tarea"
        });
    }
};
