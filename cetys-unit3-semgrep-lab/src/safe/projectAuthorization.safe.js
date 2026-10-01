async function loadProjectForUser(db, projectId, user) {
    const result = await db.query(
        `SELECT id, owner_id, name, description
         FROM projects WHERE id = $1`,
        [projectId]
    );

    const project = result.rows[0];
    if (!project) return { status: 404, body: { error: "Project not found" } };

    const isOwner = String(project.owner_id) === String(user.sub);
    const isAdmin = user.role === "admin";
    if (!isOwner && !isAdmin) return { status: 403, body: { error: "Forbidden" } };

    return { status: 200, body: project };
}

module.exports = { loadProjectForUser };
