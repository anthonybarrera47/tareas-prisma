// Middleware de auditoría y registro de peticiones HTTP en consola
export const loggerMiddleware = (req, res, next) => {
    console.log(
        `[${new Date().toISOString()}] ${req.method} ${req.url}`
    );
    next();
};
