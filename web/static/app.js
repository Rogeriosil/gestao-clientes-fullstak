const API = "";
const $ = (id) => document.getElementById(id);

const state = {
  token: localStorage.getItem("token") || null,
  editId: null,
};

function setToken(token) {
  state.token = token;
  if (token) localStorage.setItem("token", token);
  else localStorage.removeItem("token");
}

function show(el, yes=true){ el.style.display = yes ? "" : "none"; }

function toastOk(msg){
  const ok = $("okCliente");
  ok.textContent = msg;
  show(ok, true);
  setTimeout(()=>show(ok,false), 2200);
}

function erroOnde(id, msg){
  const el = $(id);
  el.textContent = msg;
  show(el, !!msg);
}

async function api(path, { method="GET", body=null } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (state.token) headers["Authorization"] = `Bearer ${state.token}`;

  const res = await fetch(`${API}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null
  });

  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.erro || `Erro HTTP ${res.status}`);
  return data;
}

function atualizarUIAutenticado() {
  const logado = !!state.token;
  show($("cardLogin"), !logado);
  show($("cardClientes"), logado);
  show($("btnSair"), logado);
}

async function login() {
  erroOnde("erroLogin", "");
  const email = $("loginEmail").value.trim();
  const senha = $("loginSenha").value;

  if (!email || !senha) return erroOnde("erroLogin", "Informe email e senha.");

  try {
    const r = await api("/auth/login", { method:"POST", body:{ email, senha } });
    setToken(r.access_token);
    atualizarUIAutenticado();
    await listar();
  } catch (e) {
    erroOnde("erroLogin", e.message);
  }
}

async function registrar() {
  erroOnde("erroLogin", "");
  const email = $("loginEmail").value.trim();
  const senha = $("loginSenha").value;

  if (!email || !senha) return erroOnde("erroLogin", "Informe email e senha.");

  try {
    await api("/auth/registrar", { method:"POST", body:{ email, senha } });
    toastOk("Usuário registrado! Agora faça login.");
  } catch (e) {
    erroOnde("erroLogin", e.message);
  }
}

function sair() {
  setToken(null);
  state.editId = null;
  limparFormulario();
  atualizarUIAutenticado();
}

function limparFormulario() {
  $("cliNome").value = "";
  $("cliEmail").value = "";
  $("cliTelefone").value = "";
  state.editId = null;
  show($("modoEdicao"), false);
  erroOnde("erroCliente", "");
}

function entrarModoEdicao(cliente) {
  $("cliNome").value = cliente.nome || "";
  $("cliEmail").value = cliente.email || "";
  $("cliTelefone").value = cliente.telefone || "";
  state.editId = cliente.id;
  $("modoEdicao").textContent = `Editando ID #${cliente.id}`;
  show($("modoEdicao"), true);
}

async function salvarCliente() {
  erroOnde("erroCliente", "");
  const nome = $("cliNome").value.trim();
  const email = $("cliEmail").value.trim();
  const telefone = $("cliTelefone").value.trim();

  if (!nome) return erroOnde("erroCliente", "Nome é obrigatório.");

  try {
    if (state.editId) {
      await api(`/clientes/${state.editId}`, { method:"PUT", body:{ nome, email: email||null, telefone: telefone||null } });
      toastOk("Cliente atualizado!");
    } else {
      await api("/clientes", { method:"POST", body:{ nome, email: email||null, telefone: telefone||null } });
      toastOk("Cliente criado!");
    }
    limparFormulario();
    await listar();
  } catch (e) {
    erroOnde("erroCliente", e.message);
  }
}

async function deletarCliente(id) {
  if (!confirm(`Excluir cliente #${id}?`)) return;
  try {
    await api(`/clientes/${id}`, { method:"DELETE" });
    toastOk("Cliente removido!");
    await listar();
  } catch (e) {
    alert(e.message);
  }
}

async function listar() {
  const tbody = $("tbodyClientes");
  tbody.innerHTML = "";
  $("vazio").style.display = "none";

  try {
    const clientes = await api("/clientes");
    if (clientes.length === 0) {
      show($("vazio"), true);
      return;
    }
    for (const c of clientes) {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${c.id}</td>
        <td>${escapeHtml(c.nome || "")}</td>
        <td>${escapeHtml(c.email || "")}</td>
        <td>${escapeHtml(c.telefone || "")}</td>
        <td>
          <div class="acoes">
            <button class="btn secundario" data-editar="${c.id}">Editar</button>
            <button class="btn" data-excluir="${c.id}">Excluir</button>
          </div>
        </td>
      `;
      tbody.appendChild(tr);
    }

    // bind buttons
    tbody.querySelectorAll("[data-editar]").forEach(btn => {
      btn.addEventListener("click", async () => {
        const id = btn.getAttribute("data-editar");
        const cliente = await api(`/clientes/${id}`);
        entrarModoEdicao(cliente);
      });
    });
    tbody.querySelectorAll("[data-excluir]").forEach(btn => {
      btn.addEventListener("click", () => deletarCliente(btn.getAttribute("data-excluir")));
    });

  } catch (e) {
    // token inválido/expirado
    alert(e.message);
    sair();
  }
}

function escapeHtml(str){
  return String(str)
    .replaceAll("&","&amp;")
    .replaceAll("<","&lt;")
    .replaceAll(">","&gt;")
    .replaceAll('"',"&quot;")
    .replaceAll("'","&#039;");
}

// eventos
$("btnLogin").addEventListener("click", login);
$("btnRegistrar").addEventListener("click", registrar);
$("btnSair").addEventListener("click", sair);
$("btnSalvar").addEventListener("click", salvarCliente);
$("btnLimpar").addEventListener("click", limparFormulario);
$("btnRecarregar").addEventListener("click", listar);

// Enter no login
["loginEmail","loginSenha"].forEach(id => {
  $(id).addEventListener("keydown", (e) => {
    if (e.key === "Enter") login();
  });
});

// iniciar
atualizarUIAutenticado();
if (state.token) listar();
