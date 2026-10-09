const BASE_URL = "https://study-ia-4j2k.onrender.com";

function getToken() {
  return localStorage.getItem("study_token");
}

function salvarToken(token) {
  localStorage.setItem("study_token", token);
}

function removerToken() {
  localStorage.removeItem("study_token");
  localStorage.removeItem("study_usuario");
}

async function apiFetch(endpoint, method = "GET", body = null, isFormData = false) {
  const headers = {};
  const token = getToken();

  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (!isFormData) headers["Content-Type"] = "application/json";

  const config = {
    method,
    headers,
    body: isFormData ? body : body ? JSON.stringify(body) : null,
  };

  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, config);

    if (response.status === 401) {
      removerToken();
      window.location.href = "/index.html";
      return;
    }

    const data = await response.json();

    return { ok: response.ok, status: response.status, data };

  } catch (error) {
    return { ok: false, status: 0, data: { detail: "Erro de conexão com o servidor." } };
  }
}

const API = {
  login:      (dados) => apiFetch("/auth/login",    "POST", dados),
  cadastro:   (dados) => apiFetch("/auth/cadastro", "POST", dados),
  gerarPlano: (dados) => apiFetch("/plano/gerar",   "POST", dados),
  buscarPlano:(id)    => apiFetch(`/plano/${id}`),
  upload:     (form)  => apiFetch("/upload",         "POST", form, true),
  responderTeste: (dados) => apiFetch("/teste/responder", "POST", dados),
};
