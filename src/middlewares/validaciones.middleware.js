// Middleware de validación para campos obligatorios en creación de tareas
export const validarDescripcion = (req, res, next) => {
    if (!req.body || !req.body.descripcion || req.body.descripcion.trim() === "") {
        return res.status(400).json({
            error: "La descripcion es un campo requerido"
        });
    }

    next();
};
