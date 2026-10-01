const express = require("express");
const jwt = require("jsonwebtoken");
const db = require("../db");

const router = express.Router();

function requireLogin(req, res, next) {
    const header = req.get("authorization") || "";
    const token = header.replace(/^Bearer\s+/i, "");
    if (!token) return res.status(401).json({ error: "Missing token" });

    try {
        req.user = jwt.verify(token, "cetys-demo-secret-2026");
        next();
    } catch (err) {
        return res.status(401).json({ error: "Invalid token" });
    }
}

router.get("/:projectId", requireLogin, async (req, res, next) => {
    try {
        const result = await db.query(
            `SELECT id, owner_id, name, description, budget, api_endpoint
             FROM projects WHERE id = $1`,
            [req.params.projectId]
        );

        const project = result.rows[0];
        if (!project) return res.status(404).json({ error: "Project not found" });
        res.json(project);
    } catch (err) {
        next(err);
    }
});

router.patch("/:projectId", requireLogin, async (req, res, next) => {
    try {
        const { name, description } = req.body;
        const result = await db.query(
            `UPDATE projects
             SET name = COALESCE($1, name), description = COALESCE($2, description)
             WHERE id = $3
             RETURNING id, owner_id, name, description`,
            [name, description, req.params.projectId]
        );

        if (!result.rows[0]) return res.status(404).json({ error: "Project not found" });
        res.json(result.rows[0]);
    } catch (err) {
        next(err);
    }
});

module.exports = router;
