import { useEffect, useRef, useState } from "react";

import {
  checkBackendHealth,
  createEngineeringTask,
  getEngineeringTask,
  getWorkflowState,
  submitApproval,
} from "./services/api";

import WorkflowPanel from "./components/WorkflowPanel";
import ApprovalPanel from "./components/ApprovalPanel";
import ResultsDashboard from "./components/ResultsDashboard";

import "./App.css";

const POLLING_INTERVAL = 3000;

const ACTIVE_STATUSES = ["queued", "running"];
const TERMINAL_STATUSES = ["completed", "failed"];

function App() {
  // Backend connection
  const [backendStatus, setBackendStatus] = useState("Not checked");

  // Task submission
  const [userQuery, setUserQuery] = useState("");
  const [task, setTask] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  // Task polling
  const [pollingError, setPollingError] = useState("");

  // Workflow state
  const [workflow, setWorkflow] = useState(null);
  const [workflowLoading, setWorkflowLoading] = useState(false);
  const [workflowError, setWorkflowError] = useState("");

  // Human approval
  const [approvalSubmitting, setApprovalSubmitting] = useState(false);
  const [approvalError, setApprovalError] = useState("");
  const [approvalAccepted, setApprovalAccepted] = useState(false);

  const approvalLock = useRef(false);

  const runId = task?.run_id;
  const taskStatus = task?.status;

  const shouldPollTask =
    ACTIVE_STATUSES.includes(taskStatus) ||
    (approvalAccepted &&
      !TERMINAL_STATUSES.includes(taskStatus));

  // M11.4 + M11.6: Task polling
  useEffect(() => {
    if (!runId || !shouldPollTask) return;

    let active = true;
    let requestInProgress = false;

    async function refreshTask() {
      if (requestInProgress) return;

      requestInProgress = true;

      try {
        const updatedTask = await getEngineeringTask(runId);

        if (active) {
          setTask(updatedTask);
          setPollingError("");
        }
      } catch (err) {
        if (active) {
          setPollingError(err.message);
        }
      } finally {
        requestInProgress = false;
      }
    }

    refreshTask();

    const intervalId = setInterval(
      refreshTask,
      POLLING_INTERVAL
    );

    return () => {
      active = false;
      clearInterval(intervalId);
    };
  }, [runId, shouldPollTask]);

  // M11.5 + M11.6: Workflow polling
  useEffect(() => {
    if (!runId) return;

    let active = true;
    let requestInProgress = false;

    const shouldPoll =
      ACTIVE_STATUSES.includes(taskStatus) ||
      (approvalAccepted &&
        !TERMINAL_STATUSES.includes(taskStatus));

    async function refreshWorkflow() {
      if (requestInProgress) return;

      requestInProgress = true;

      if (active) {
        setWorkflowLoading(true);
      }

      try {
        const result = await getWorkflowState(runId);

        if (active) {
          setWorkflow(result);
          setWorkflowError("");
        }
      } catch (err) {
        if (active) {
          setWorkflowError(err.message);
        }
      } finally {
        requestInProgress = false;

        if (active) {
          setWorkflowLoading(false);
        }
      }
    }

    refreshWorkflow();

    if (!shouldPoll) {
      return () => {
        active = false;
      };
    }

    const intervalId = setInterval(
      refreshWorkflow,
      POLLING_INTERVAL
    );

    return () => {
      active = false;
      clearInterval(intervalId);
    };
  }, [runId, taskStatus, approvalAccepted]);

  // Backend health check
  async function handleCheckBackend() {
    setError("");
    setBackendStatus("Checking...");

    try {
      const result = await checkBackendHealth();
      setBackendStatus(result.status);
    } catch (err) {
      setBackendStatus("Disconnected");
      setError(err.message);
    }
  }

  // Submit engineering task
  async function handleSubmitTask(event) {
    event.preventDefault();

    if (submitting || approvalSubmitting) return;

    const query = userQuery.trim();

    if (!query) {
      setError("Please enter an engineering question.");
      return;
    }

    if (query.length > 5000) {
      setError("Question must be 5000 characters or fewer.");
      return;
    }

    setSubmitting(true);
    setError("");
    setPollingError("");
    setApprovalError("");
    setApprovalAccepted(false);

    approvalLock.current = false;

    setTask(null);
    setWorkflow(null);
    setWorkflowError("");
    setWorkflowLoading(false);

    try {
      const result = await createEngineeringTask(query);
      setTask(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  // M11.6: Human approval
  async function handleApprovalDecision(decision) {
    if (
      !runId ||
      taskStatus !== "awaiting_approval" ||
      approvalLock.current ||
      approvalSubmitting
    ) {
      return;
    }

    approvalLock.current = true;
    setApprovalSubmitting(true);
    setApprovalError("");

    try {
      await submitApproval(runId, decision);

      // Keep polling until terminal status
      setApprovalAccepted(true);
    } catch (err) {
      approvalLock.current = false;
      setApprovalError(err.message);
    } finally {
      setApprovalSubmitting(false);
    }
  }

  const isProcessing =
    task && ACTIVE_STATUSES.includes(task.status);

  const showApprovalPanel =
    taskStatus === "awaiting_approval" &&
    !approvalAccepted;

  const showResultsDashboard =
    task && TERMINAL_STATUSES.includes(task.status);

  return (
    <div className="app">
      <header className="app-header">
        <h1>EngineerFlow</h1>
        <p>Multi-Agent AI Engineering Copilot</p>
      </header>

      <main className="app-main">
        <section className="welcome-card">
          <h2>Engineering Task Submission</h2>

          <p>
            Submit an engineering challenge for
            analysis by specialized AI agents.
          </p>

          <button
            type="button"
            onClick={handleCheckBackend}
          >
            Check Backend Connection
          </button>

          <p>
            Backend Status: <strong>{backendStatus}</strong>
          </p>

          <form onSubmit={handleSubmitTask}>
            <label htmlFor="user-query">
              Engineering Question
            </label>

            <textarea
              id="user-query"
              value={userQuery}
              onChange={(event) =>
                setUserQuery(event.target.value)
              }
              placeholder="e.g. Design a scalable AWS architecture for an AI application."
              rows={6}
              maxLength={5000}
              required
            />

            <p>{userQuery.length} / 5000 characters</p>

            <button
              type="submit"
              disabled={submitting || approvalSubmitting}
            >
              {submitting ? "Submitting..." : "Submit Task"}
            </button>
          </form>

          {error && (
            <p className="error-message" role="alert">
              Error: {error}
            </p>
          )}

          {/* Engineering Task Status */}
          {task && (
            <section className="task-result">
              <h3>Engineering Task</h3>

              <p>
                <strong>Run ID:</strong> {task.run_id}
              </p>

              <p>
                <strong>Status:</strong>{" "}
                <span className={`status status-${task.status}`}>
                  {task.status}
                </span>
              </p>

              {isProcessing && (
                <p className="processing-message">
                  AI agents are processing your request...
                </p>
              )}

              {showApprovalPanel && (
                <p>
                  Human approval is required before
                  the workflow can continue.
                </p>
              )}

              {approvalAccepted &&
                !TERMINAL_STATUSES.includes(taskStatus) && (
                  <p className="processing-message">
                    Approval decision accepted.
                    Waiting for workflow to resume...
                  </p>
                )}

              {taskStatus === "completed" && (
                <p>
                  Engineering analysis completed successfully.
                </p>
              )}

              {taskStatus === "failed" && (
                <p className="error-message">
                  Task failed:{" "}
                  {task.error_message || "Unknown error"}
                </p>
              )}

              {pollingError && (
                <p className="error-message" role="alert">
                  Status update failed: {pollingError}
                </p>
              )}
            </section>
          )}

          {/* M11.5: Workflow Visualization */}
          {task && (
            <WorkflowPanel
              workflow={workflow}
              loading={workflowLoading}
              error={workflowError}
            />
          )}

          {/* M11.6: Human Approval */}
          {showApprovalPanel && (
            <ApprovalPanel
              task={task}
              workflow={workflow}
              onDecision={handleApprovalDecision}
              submitting={approvalSubmitting}
              error={approvalError}
            />
          )}

          {/* M11.7: Results Dashboard */}
          {showResultsDashboard && (
            <ResultsDashboard
              task={task}
              workflow={workflow}
            />
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
