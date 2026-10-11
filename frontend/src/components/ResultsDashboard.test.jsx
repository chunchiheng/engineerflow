
import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";

import ResultsDashboard from "./ResultsDashboard";

const completedTask = {
  run_id: "test-run-123",
  status: "completed",
  user_query: "Design an AWS RAG architecture",
  final_response: "Recommended architecture: EC2, S3, RDS, ChromaDB.",
  approval_status: "not_required",
  action_result: null,
  error_message: null,
  created_at: "2026-10-11T12:00:00Z",
};

const completedWorkflow = {
  workflow_status: "completed",
  selected_agents: ["cloud", "ai", "systems"],
  completed_agents: ["cloud", "ai", "systems"],
  action_required: false,
  action_type: "none",
  approval_status: "not_required",
};

describe("ResultsDashboard", () => {
  it("renders the final engineering report", () => {
    render(
      <ResultsDashboard
        task={completedTask}
        workflow={completedWorkflow}
      />
    );

    expect(
      screen.getByText(
        "Recommended architecture: EC2, S3, RDS, ChromaDB."
      )
    ).toBeInTheDocument();
  });

  it("displays participating agents", () => {
    render(
      <ResultsDashboard
        task={completedTask}
        workflow={completedWorkflow}
      />
    );

    expect(screen.getByText("Cloud Agent")).toBeInTheDocument();
    expect(screen.getByText("AI Agent")).toBeInTheDocument();
    expect(screen.getByText("Systems Agent")).toBeInTheDocument();
  });

  it("shows approval status", () => {
    render(
      <ResultsDashboard
        task={completedTask}
        workflow={completedWorkflow}
      />
    );

    expect(screen.getByText("not_required")).toBeInTheDocument();
  });

  it("does not render while the task is running", () => {
    const { container } = render(
      <ResultsDashboard
        task={{ ...completedTask, status: "running" }}
        workflow={completedWorkflow}
      />
    );

    expect(container).toBeEmptyDOMElement();
  });

  it("shows rejection information", () => {
    render(
      <ResultsDashboard
        task={{
          ...completedTask,
          approval_status: "rejected",
        }}
        workflow={{
          ...completedWorkflow,
          approval_status: "rejected",
        }}
      />
    );

    expect(screen.getByText("rejected")).toBeInTheDocument();

    expect(
      screen.getByText(/requested action was rejected/i)
    ).toBeInTheDocument();
  });
});
