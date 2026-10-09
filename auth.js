
function mostrarMensagem(texto, tipo = "erro") {
  const el = document.getElementById("mensagem");
  if (!el) return;
  el.textContent = texto;
  el.className = `mensagem ${tipo}`;
}

function setCarregando(btnId, carregando) {
  const btn = document.getElementById(btnId);
  if (!btn) return;
  btn.disabled = carregando;
  btn.innerHTML = carregando
    ? `<span class="spinner"></span> Aguarde...`
    : btn.dataset.label;
}

document.addEventListener("DOMContentLoaded", () => {
  ["btn-login", "btn-cadastro"].forEach((id) => {
    const btn = document.getElementById(id);
    if (btn) btn.dataset.label = btn.textContent.trim();
  });


  const paginasPublicas = ["index.html", "cadastro.html", ""];
  const paginaAtual = window.location.pathname.split("/").pop();

  if (getToken() && paginasPublicas.includes(paginaAtual)) {
    window.location.href = "dashboard.html";
  }
});


const formLogin = document.getElementById("form-login");
if (formLogin) {
  formLogin.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("senha").value;

    if (!email || !senha) {
      mostrarMensagem("Preencha todos os campos.");
      return;
    }

    setCarregando("btn-login", true);

    const resultado = await API.login({ email, senha });

    setCarregando("btn-login", false);

    if (resultado.ok) {
      salvarToken(resultado.data.access_token);
      localStorage.setItem("study_usuario", JSON.stringify(resultado.data.usuario));
      window.location.href = "dashboard.html";
    } else {
      mostrarMensagem(resultado.data.detail || "E-mail ou senha incorretos.");
    }
  });
}


const formCadastro = document.getElementById("form-cadastro");
if (formCadastro) {
  formCadastro.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nome      = document.getElementById("nome").value.trim();
    const email     = document.getElementById("email").value.trim();
    const senha     = document.getElementById("senha").value;
    const confirmar = document.getElementById("confirmar-senha").value;

    if (!nome || !email || !senha || !confirmar) {
      mostrarMensagem("Preencha todos os campos.");
      return;
    }

    if (senha.length < 6) {
      mostrarMensagem("A senha deve ter pelo menos 6 caracteres.");
      return;
    }

    if (senha !== confirmar) {
      mostrarMensagem("As senhas não coincidem.");
      return;
    }

    setCarregando("btn-cadastro", true);

    const resultado = await API.cadastro({ nome, email, senha });

    setCarregando("btn-cadastro", false);

    if (resultado.ok) {
      mostrarMensagem("Conta criada com sucesso! Redirecionando...", "sucesso");
      setTimeout(() => (window.location.href = "index.html"), 1500);
    } else {
      mostrarMensagem(resultado.data.detail || "Erro ao criar conta. Tente novamente.");
    }
  });
}
