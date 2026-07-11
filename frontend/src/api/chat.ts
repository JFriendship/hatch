const API_URL =
    import.meta.env.VITE_API_URL ?? "http://localhost:8000";

/**
 * Request sent to FastAPI
 */
export interface ChatRequest {
    prompt: string;
}

/**
 * Response returned by FastAPI
 */
export interface ChatResponse {
    model_response: string;
    char_count: number;
}

/**
 * Sends a prompt to the backend and returns the generated response.
 *
 * Throws an Error if the request fails, the backend returns a non-2xx status,
 *  or the response is malformed
 */
export async function sendPrompt(
    request: ChatRequest
): Promise<ChatResponse> {

    const response = await fetch(`${API_URL}/gentext/qweninference`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(request),
    });

    if (!response.ok) {

        let message = "Unable to generate a response.";

        try {
            const error = await response.json();

            if (typeof error.detail === "string") {
                message = error.detail;
            }
        } catch {
            // Ignore JSON parsing errors and use the default message.
        }

        throw new Error(message);
    }

    const data: ChatResponse = await response.json();

    if (typeof data.model_response !== "string" || typeof data.char_count !== "number") {
        throw new Error("Invalid response received from the server.");
    }

    return data;
}