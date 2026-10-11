import { useState } from "react";
import "./ResultsDashboard.css";

const AGENT_LABELS = {
  cloud: "Cloud Agent",
  ai: "AI Agent",
  systems: "Systems Agent",
};

function formatValue(value) {
  if (value === null || value === undefined || value === "") {
    return "Not available";
  }

  if (typeof value === "string") {
    return value;
  }

  return JSON.stringify(value, null, 2);
}

function formatDate(value) {
  if (!value) return "Not available";

  const date = new Date(value);

  return Number.isNaN(date.getTime())
    ? String(value)
    : date.toLocaleString();
}

export default function ResultsDashboard({ task, workflow }) {
  const [copied, setCopied] = useState(false);

  if (!task || !["completed", "failed"].includes(task.status)) {
    return null;
  }

  const report = formatValue(task.final_response);
  const hasReport =
    task.final_response !== null &&
    task.final_response !== undefined &&
    task.final_response !== "";

  const selectedAgents = workflow?.selected_agents || [];
  const completedAgents = workflow?.completed_agents || [];

  const approvalStatus =
    task.approval_status ||
    workflow?.approval_status ||
    "not_required";

  async function handleCopyReport() {
    try {
      await navigator.clipboard.writeText(report);
      setCopied(true);
    } catch {
      setCopied(false);
    }
  }

  return (
    <section className="results-dashboard">
      <div className="results-header">
        <div>
          <h2>Engineering Results Dashboard</h2>
          <p>Multi-Agent Engineering Analysis</p>
        </div>

        <span className={`results-status results-${task.status}`}>
          {task.status}
        </span>
      </div>

      <div className="results-section">
        <h3>Task Overview</h3>

        <p>
          <strong>Run ID:</strong> {task.run_id}
        </p>

        <p>
          <strong>Created At:</strong>{" "}
          {formatDate(task.created_at)}
        </p>

        <p>
          <strong>Original Query:</strong>
        </p>

        <div className="results-content">
          {formatValue(task.user_query)}
        </div>
      </div>

      <div className="results-section">
        <h3>Agent Participation</h3>

        {selectedAgents.length === 0 ? (
          <p>Agent information is not available.</p>
        ) : (
          <div className="results-agent-grid">
            {selectedAgents.map((agent) => {
              const isCompleted = completedAgents.includes(agent);

              return (
                <div className="results-agent-card" key={agent}>
                  <strong>
                    {AGENT_LABELS[agent] || agent}
                  </strong>

                  <span>
                    {isCompleted ? "Completed" : "Not completed"}
                  </span>
                </div>
              );
            })}
          </div>
        )}
      </div>

      <div className="results-section">
        <h3>Approval & Execution Summary</h3>

        <p>
          <strong>Action Required:</strong>{" "}
          {workflow?.action_required ? "Yes" : "No"}
        </p>

        <p>
          <strong>Action Type:</strong>{" "}
          {workflow?.action_type || "Not available"}
        </p>

        <p>
          <strong>Approval Status:</strong>{" "}
          <span className={`approval-value approval-${approvalStatus}`}>
            {approvalStatus}
          </span>
        </p>

        <h4>Action Result</h4>

        <pre className="results-content results-pre">
          {formatValue(task.action_result)}
        </pre>

        {approvalStatus === "rejected" && (
          <p className="results-notice">
            The requested action was rejected.
            Workflow completion does not mean
            the action was authorized.
          </p>
        )}

        <p className="results-notice">
          EngineerFlow currently uses a simulated
          action executor. A completed task does
          not indicate a real AWS deployment.
        </p>
      </div>

      <div className="results-section">
        <div className="results-report-header">
          <h3>Final Engineering Report</h3>

          {hasReport && (
            <button
              type="button"
              onClick={handleCopyReport}
            >
              {copied ? "Copied!" : "Copy Report"}
            </button>
          )}
        </div>

        <div className="results-content results-report">
          {hasReport
            ? report
            : "No final report is available for this task."}
        </div>
      </div>

      {task.error_message && (
        <div className="results-section">
          <h3>Task Error</h3>
          <p className="results-error">
            {task.error_message}
          </p>
        </div>
      )}
    </section>
  );
}
