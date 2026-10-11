const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function apiRequest(path, options = {}) {
  const response = await fetch(
    `${API_BASE_URL}${path}`,
    {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : `API request failed: ${response.status}`
    );
  }

  return data;
}

export function checkBackendHealth() {
  return apiRequest("/health");
}

export function createEngineeringTask(userQuery) {
  return apiRequest("/api/tasks", {
    method: "POST",
    body: JSON.stringify({
      user_query: userQuery,
    }),
  });
}

export function getEngineeringTask(runId) {
  return apiRequest(`/api/tasks/${runId}`);
}

export function getWorkflowState(runId) {
  return apiRequest(`/api/tasks/${runId}/state`);
}

export function submitApproval(runId, decision) {
  return apiRequest(`/api/tasks/${runId}/approval`, {
    method: "POST",
    body: JSON.stringify({
      decision,
    }),
  });
}
