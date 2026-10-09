const formPlano = document.getElementById("form-plano");

formPlano.addEventListener("submit", async (e) => {
  e.preventDefault();

  const materia  = document.getElementById("materia").value.trim();
  const nivel    = document.getElementById("nivel").value;
  const conteudo = document.getElementById("conteudo").value.trim();

  if (!materia || !nivel || !conteudo) {
    mostrarMensagemPlano("Preencha todos os campos.", "erro");
    return;
  }

  const btn = document.getElementById("btn-gerar");
  btn.disabled = true;
  btn.innerHTML = `<span class="spinner"></span> Gerando plano...`;

  document.getElementById("resultado-area").style.display = "none";

  const resultado = await API.gerarPlano({ materia, nivel, conteudo });

  btn.disabled = false;
  btn.innerHTML = "✨ Gerar Plano com IA";

  if (resultado.ok) {
    exibirPlano(resultado.data.plano_ia);
  } else {
    mostrarMensagemPlano(resultado.data.detail || "Erro ao gerar plano.", "erro");
  }
});

function exibirPlano(texto) {
  const area     = document.getElementById("resultado-area");
  const conteudo = document.getElementById("resultado-conteudo");


  conteudo.innerHTML = markdownParaHtml(texto);
  area.style.display = "block";
  area.scrollIntoView({ behavior: "smooth" });
}

function markdownParaHtml(md) {
  return md
    .replace(/^### (.+)$/gm,  "<h3>$1</h3>")
    .replace(/^## (.+)$/gm,   "<h2>$1</h2>")
    .replace(/^# (.+)$/gm,    "<h1>$1</h1>")
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g,     "<em>$1</em>")
    .replace(/^- (.+)$/gm,    "<li>$1</li>")
    .replace(/(<li>.*<\/li>)/gs, "<ul>$1</ul>")
    .replace(/\n{2,}/g,        "<br/><br/>")
    .replace(/\n/g,            "<br/>");
}

function mostrarMensagemPlano(texto, tipo) {
  const el = document.getElementById("mensagem-plano");
  el.textContent  = texto;
  el.className    = `mensagem-plano ${tipo}`;
  el.style.display = "block";
  setTimeout(() => (el.style.display = "none"), 4000);
}

function copiarPlano() {
  const texto = document.getElementById("resultado-conteudo").innerText;
  navigator.clipboard.writeText(texto).then(() => {
    const btn = document.querySelector(".btn-copiar");
    btn.textContent = "✅ Copiado!";
    setTimeout(() => (btn.textContent = "📋 Copiar"), 2000);
  });
}
