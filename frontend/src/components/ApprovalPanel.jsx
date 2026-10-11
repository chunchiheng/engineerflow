
import { useState } from "react";
import "./ApprovalPanel.css";

export default function ApprovalPanel({
  task,
  workflow,
  onDecision,
  submitting,
  error,
}) {
  const [confirmation, setConfirmation] = useState(null);

  if (!task || task.status !== "awaiting_approval") {
    return null;
  }

  const actionType = workflow?.action_type || "unknown";

  function handleDecision(decision) {
    setConfirmation(decision);
  }

  async function confirmDecision() {
    if (!confirmation || submitting) return;

    const decision = confirmation;
    setConfirmation(null);

    await onDecision(decision);
  }

  return (
    <section className="approval-panel">
      <h3>Human Approval Required</h3>

      <p>
        The AI workflow is requesting permission
        to perform an engineering action.
      </p>

      <div className="approval-details">
        <p>
          <strong>Action Type:</strong> {actionType}
        </p>

        <p>
          <strong>Run ID:</strong> {task.run_id}
        </p>

        <p>
          <strong>Approval Status:</strong>{" "}
          {workflow?.approval_status || "pending"}
        </p>
      </div>

      <p className="approval-warning">
        Please review the requested action before
        making your decision.
      </p>

      {!confirmation ? (
        <div className="approval-buttons">
          <button
            type="button"
            className="approve-button"
            onClick={() => handleDecision("approved")}
            disabled={submitting}
          >
            Approve
          </button>

          <button
            type="button"
            className="reject-button"
            onClick={() => handleDecision("rejected")}
            disabled={submitting}
          >
            Reject
          </button>
        </div>
      ) : (
        <div className="approval-confirmation">
          <p>
            Confirm your decision:{" "}
            <strong>{confirmation}</strong>?
          </p>

          <div className="approval-buttons">
            <button
              type="button"
              className="confirm-button"
              onClick={confirmDecision}
              disabled={submitting}
            >
              {submitting
                ? "Submitting..."
                : "Confirm Decision"}
            </button>

            <button
              type="button"
              className="cancel-button"
              onClick={() => setConfirmation(null)}
              disabled={submitting}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {error && (
        <p className="approval-error" role="alert">
          {error}
        </p>
      )}
    </section>
  );
}
