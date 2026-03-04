// Base da URL da API.
// Como está vazio (""), significa que as requisições serão feitas
// para o mesmo domínio/porta onde o front está rodando.
const API = "";

// Atalho para pegar elemento pelo ID (equivalente a document.getElementById)
const $ = (id) => document.getElementById(id);


// Objeto que guarda o estado da aplicação no frontend
const state = {
  // Token JWT salvo no navegador (mantém login após atualizar a página)
  token: localStorage.getItem("token") || null,

  // ID do cliente que está sendo editado (null = modo criação)
  editId: null,
};


// Salva ou remove o token no estado e no localStorage
function setToken(token) {
  state.token = token;
  if (token) localStorage.setItem("token", token);
  else localStorage.removeItem("token");
}


// Função utilitária para mostrar ou esconder elementos
function show(el, yes=true){ 
  el.style.display = yes ? "" : "none"; 
}


// Mostra mensagem de sucesso na área "okCliente"
// e esconde automaticamente após 2,2 segundos
function toastOk(msg){
  const ok = $("okCliente");
  ok.textContent = msg;
  show(ok, true);
  setTimeout(()=>show(ok,false), 2200);
}


// Mostra erro em um elemento específico pelo ID
// Se msg for vazio, ele oculta o elemento
function erroOnde(id, msg){
  const el = $(id);
  el.textContent = msg;
  show(el, !!msg);
}


// Função central para chamadas à API
// Recebe caminho (path), método HTTP e corpo opcional
async function api(path, { method="GET", body=null } = {}) {
  const headers = { "Content-Type": "application/json" };

  // Se estiver autenticado, envia o token no header Authorization
  if (state.token) headers["Authorization"] = `Bearer ${state.token}`;

  const res = await fetch(`${API}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null
  });

  // Tenta converter resposta para JSON
  const data = await res.json().catch(() => ({}));

  // Se resposta HTTP for erro, lança exceção
  if (!res.ok) throw new Error(data.erro || `Erro HTTP ${res.status}`);
  
  return data;
}


// Atualiza interface dependendo se usuário está logado ou não
function atualizarUIAutenticado() {
  const logado = !!state.token;
  show($("cardLogin"), !logado);
  show($("cardClientes"), logado);
  show($("btnSair"), logado);
}


// ==================== LOGIN ====================

// Realiza login chamando /auth/login
async function login() {
  erroOnde("erroLogin", "");
  const email = $("loginEmail").value.trim();
  const senha = $("loginSenha").value;

  if (!email || !senha) 
    return erroOnde("erroLogin", "Informe email e senha.");

  try {
    const r = await api("/auth/login", { 
      method:"POST", 
      body:{ email, senha } 
    });

    // Espera receber { access_token: "..." }
    setToken(r.access_token);

    atualizarUIAutenticado();
    await listar();
  } catch (e) {
    erroOnde("erroLogin", e.message);
  }
}


// ==================== REGISTRO ====================

// Registra novo usuário chamando /auth/registrar
async function registrar() {
  erroOnde("erroLogin", "");
  const email = $("loginEmail").value.trim();
  const senha = $("loginSenha").value;

  if (!email || !senha) 
    return erroOnde("erroLogin", "Informe email e senha.");

  try {
    await api("/auth/registrar", { 
      method:"POST", 
      body:{ email, senha } 
    });

    toastOk("Usuário registrado! Agora faça login.");
  } catch (e) {
    erroOnde("erroLogin", e.message);
  }
}


// ==================== LOGOUT ====================

// Remove token e volta para tela de login
function sair() {
  setToken(null);
  state.editId = null;
  limparFormulario();
  atualizarUIAutenticado();
}


// ==================== FORMULÁRIO ====================

// Limpa formulário e sai do modo edição
function limparFormulario() {
  $("cliNome").value = "";
  $("cliEmail").value = "";
  $("cliTelefone").value = "";
  state.editId = null;
  show($("modoEdicao"), false);
  erroOnde("erroCliente", "");
}


// Entra no modo edição preenchendo os campos
function entrarModoEdicao(cliente) {
  $("cliNome").value = cliente.nome || "";
  $("cliEmail").value = cliente.email || "";
  $("cliTelefone").value = cliente.telefone || "";
  state.editId = cliente.id;
  $("modoEdicao").textContent = `Editando ID #${cliente.id}`;
  show($("modoEdicao"), true);
}


// ==================== SALVAR CLIENTE ====================

// Cria ou atualiza cliente dependendo se está em modo edição
async function salvarCliente() {
  erroOnde("erroCliente", "");

  const nome = $("cliNome").value.trim();
  const email = $("cliEmail").value.trim();
  const telefone = $("cliTelefone").value.trim();

  if (!nome) 
    return erroOnde("erroCliente", "Nome é obrigatório.");

  try {
    if (state.editId) {
      await api(`/clientes/${state.editId}`, { 
        method:"PUT", 
        body:{ nome, email: email||null, telefone: telefone||null } 
      });
      toastOk("Cliente atualizado!");
    } else {
      await api("/clientes", { 
        method:"POST", 
        body:{ nome, email: email||null, telefone: telefone||null } 
      });
      toastOk("Cliente criado!");
    }

    limparFormulario();
    await listar();

  } catch (e) {
    erroOnde("erroCliente", e.message);
  }
}


// ==================== DELETAR ====================

// Remove cliente pelo ID
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


// ==================== LISTAR CLIENTES ====================

// Busca todos os clientes e renderiza na tabela
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

    // Evento botão editar
    tbody.querySelectorAll("[data-editar]").forEach(btn => {
      btn.addEventListener("click", async () => {
        const id = btn.getAttribute("data-editar");
        const cliente = await api(`/clientes/${id}`);
        entrarModoEdicao(cliente);
      });
    });

    // Evento botão excluir
    tbody.querySelectorAll("[data-excluir]").forEach(btn => {
      btn.addEventListener("click", () => 
        deletarCliente(btn.getAttribute("data-excluir"))
      );
    });

  } catch (e) {
    alert(e.message);
    sair();
  }
}


// ==================== SEGURANÇA ====================

// Protege contra injeção de HTML na tabela
function escapeHtml(str){
  return String(str)
    .replaceAll("&","&amp;")
    .replaceAll("<","&lt;")
    .replaceAll(">","&gt;")
    .replaceAll('"',"&quot;")
    .replaceAll("'","&#039;");
}


// ==================== EVENTOS ====================

$("btnLogin").addEventListener("click", login);
$("btnRegistrar").addEventListener("click", registrar);
$("btnSair").addEventListener("click", sair);
$("btnSalvar").addEventListener("click", salvarCliente);
$("btnLimpar").addEventListener("click", limparFormulario);
$("btnRecarregar").addEventListener("click", listar);


// Permite pressionar Enter para fazer login
["loginEmail","loginSenha"].forEach(id => {
  $(id).addEventListener("keydown", (e) => {
    if (e.key === "Enter") login();
  });
});


// ==================== INICIALIZAÇÃO ====================

// Ajusta interface ao carregar página
atualizarUIAutenticado();

// Se já houver token salvo, lista clientes automaticamente
if (state.token) listar();
