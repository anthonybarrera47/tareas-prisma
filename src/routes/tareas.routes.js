import { Router } from "express";
import {
    obtenerTareas,
    obtenerTareaPorId,
    crearTarea,
    actualizarTarea,
    eliminarTarea
} from "../controllers/tareas.controller.js";
import { validarDescripcion } from "../middlewares/validaciones.middleware.js";

const router = Router();

// Definición de rutas asociadas al recurso /tareas
router.get("/", obtenerTareas);
router.get("/:id", obtenerTareaPorId);
router.post("/", validarDescripcion, crearTarea);
router.put("/:id", actualizarTarea);
router.delete("/:id", eliminarTarea);

export default router;
