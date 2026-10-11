import "./WorkflowPanel.css";

const AGENTS = [
  { key: "cloud", label: "Cloud Agent" },
  { key: "ai", label: "AI Agent" },
  { key: "systems", label: "Systems Agent" },
];

function normalizeAgentName(name) {
  return String(name || "")
    .toLowerCase()
    .replace(/[_\s-]+agent$/, "")
    .trim();
}

function getAgentStatus(agent, workflow) {
  const selected = (workflow.selected_agents || [])
    .map(normalizeAgentName);

  const completed = (workflow.completed_agents || [])
    .map(normalizeAgentName);

  const agentKey = normalizeAgentName(agent);

  if (completed.includes(agentKey)) {
    return "completed";
  }

  if (selected.includes(agentKey)) {
    return "pending";
  }

  return "not_selected";
}

const STATUS_LABELS = {
  completed: "Completed",
  pending: "Selected / Pending",
  not_selected: "Not Selected",
};

export default function WorkflowPanel({ workflow, loading, error }) {
  if (loading && !workflow) {
    return (
      <section className="workflow-panel">
        <h3>Multi-Agent Workflow</h3>
        <p>Loading workflow state...</p>
      </section>
    );
  }

  if (error && !workflow) {
    return (
      <section className="workflow-panel">
        <h3>Multi-Agent Workflow</h3>
        <p className="workflow-error">{error}</p>
      </section>
    );
  }

  if (!workflow) {
    return null;
  }

  return (
    <section className="workflow-panel">
      <div className="workflow-heading">
        <h3>Multi-Agent Workflow</h3>
        <span className="workflow-overall-status">
          {workflow.workflow_status}
        </span>
      </div>

      <div className="workflow-agent-grid">
        {AGENTS.map((agent) => {
          const status = getAgentStatus(agent.key, workflow);

          return (
            <div
              className="workflow-agent-card"
              key={agent.key}
            >
              <strong>{agent.label}</strong>

              <span className={`agent-status agent-${status}`}>
                {STATUS_LABELS[status]}
              </span>
            </div>
          );
        })}
      </div>

      <div className="workflow-details">
        <p>
          <strong>Next Nodes:</strong>{" "}
          {workflow.next_nodes?.length
            ? workflow.next_nodes.join(", ")
            : "None"}
        </p>

        <p>
          <strong>Action Required:</strong>{" "}
          {workflow.action_required ? "Yes" : "No"}
        </p>

        {workflow.action_type && (
          <p>
            <strong>Action Type:</strong>{" "}
            {workflow.action_type}
          </p>
        )}

        <p>
          <strong>Approval Status:</strong>{" "}
          {workflow.approval_status || "N/A"}
        </p>

        {workflow.awaiting_approval && (
          <p className="workflow-approval-message">
            Workflow paused — waiting for human approval.
          </p>
        )}
      </div>

      {error && (
        <p className="workflow-error" role="alert">
          Latest workflow refresh failed: {error}
        </p>
      )}
    </section>
  );
}
