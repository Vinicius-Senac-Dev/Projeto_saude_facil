// Funções para gerenciar o histórico de consultas do médico

document.addEventListener('DOMContentLoaded', function() {
  // Configuração das abas no modal de detalhes
  const tabButtons = document.querySelectorAll('.tab-button');
  const tabContents = document.querySelectorAll('.tab-content');
  
  tabButtons.forEach(button => {
    button.addEventListener('click', function() {
      const tabId = this.getAttribute('data-tab');
      
      // Desativar todas as abas
      tabButtons.forEach(btn => btn.classList.remove('active'));
      tabContents.forEach(content => content.classList.remove('active'));
      
      // Ativar a aba selecionada
      this.classList.add('active');
      document.getElementById(tabId).classList.add('active');
    });
  });
  
  // Configuração do modal
  const modal = document.getElementById('modalConsultaDetails');
  const closeBtn = document.querySelector('.close');
  const fecharBtn = document.getElementById('btn-fechar-detalhes');
  const detailBtns = document.querySelectorAll('.btn-details');
  
  detailBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      const consultaId = this.getAttribute('data-id');
      carregarDetalhesConsulta(consultaId);
      modal.style.display = 'block';
    });
  });
  
  closeBtn.addEventListener('click', function() {
    modal.style.display = 'none';
  });
  
  fecharBtn.addEventListener('click', function() {
    modal.style.display = 'none';
  });
  
  window.addEventListener('click', function(event) {
    if (event.target == modal) {
      modal.style.display = 'none';
    }
  });
  
  // Configuração dos filtros
  const periodoSelect = document.getElementById('filter-periodo');
  const customPeriod = document.getElementById('custom-period');
  
  periodoSelect.addEventListener('change', function() {
    if (this.value === 'custom') {
      customPeriod.classList.remove('hidden');
    } else {
      customPeriod.classList.add('hidden');
    }
  });
  
  // Botão para filtrar
  const btnFiltrar = document.getElementById('btn-filtrar');
  btnFiltrar.addEventListener('click', function() {
    aplicarFiltros();
  });
  
  // Botão para limpar filtros
  const btnLimparFiltros = document.getElementById('btn-limpar-filtros');
  btnLimparFiltros.addEventListener('click', function() {
    limparFiltros();
  });
  
  // Botão para editar prontuário
  const btnEditarProntuario = document.getElementById('btn-editar-prontuario');
  if (btnEditarProntuario) {
    btnEditarProntuario.addEventListener('click', function() {
      const consultaId = document.querySelector('.btn-details.active')?.getAttribute('data-id');
      if (consultaId) {
        // Redirecionar para a página de edição do prontuário
        window.location.href = `/prontuario/editar/${consultaId}/`;
      }
    });
  }
  
  // Botão para nova prescrição
  const btnNovaPrescrição = document.getElementById('btn-nova-prescricao');
  if (btnNovaPrescrição) {
    btnNovaPrescrição.addEventListener('click', function() {
      const consultaId = document.querySelector('.btn-details.active')?.getAttribute('data-id');
      if (consultaId) {
        // Redirecionar para a página de nova prescrição
        window.location.href = `/prescricoes/nova/${consultaId}/`;
      }
    });
  }
  
  // Botão para continuar atendimento
  const btnContinueAtendimento = document.querySelectorAll('.btn-continue');
  btnContinueAtendimento.forEach(btn => {
    btn.addEventListener('click', function() {
      const consultaId = this.getAttribute('data-id');
      // Redirecionar para a página de atendimento
      window.location.href = `/consulta/atendimento/${consultaId}/`;
    });
  });
  
  // Configuração de botões de prescrição
  const prescriptionBtns = document.querySelectorAll('.btn-prescription');
  prescriptionBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      const consultaId = this.getAttribute('data-id');
      // Redirecionar para a página de prescrições
      window.location.href = `/prescricoes/consulta/${consultaId}/`;
    });
  });
});

/**
 * Carrega os detalhes da consulta no modal
 * @param {string} consultaId - ID da consulta a ser carregada
 */
function carregarDetalhesConsulta(consultaId) {
  // Em uma implementação real, você faria uma requisição AJAX para carregar os detalhes
  // Por enquanto, simulamos os dados
  
  // Elementos para preencher
  const dateElement = document.getElementById('detail-date');
  const timeElement = document.getElementById('detail-time');
  const specialtyElement = document.getElementById('detail-specialty');
  const patientElement = document.getElementById('detail-patient');
  const ageElement = document.getElementById('detail-age');
  const diagnosisElement = document.getElementById('detail-diagnosis');
  const symptomsElement = document.getElementById('detail-symptoms');
  const examsElement = document.getElementById('detail-exams');
  const observationsElement = document.getElementById('detail-observations');
  
  // Marcar o botão como ativo para referência
  document.querySelectorAll('.btn-details').forEach(btn => {
    if (btn.getAttribute('data-id') === consultaId) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });
  
  // Resetar para a primeira aba
  document.querySelectorAll('.tab-button').forEach(btn => {
    if (btn.getAttribute('data-tab') === 'consulta-atual') {
      btn.click();
    }
  });
}

/**
 * Aplica os filtros selecionados na interface
 */
function aplicarFiltros() {
  // Em uma implementação real, você faria uma requisição AJAX para buscar os dados filtrados
  // Por enquanto, apenas simulamos o comportamento
  
  const periodoSelect = document.getElementById('filter-periodo').value;
  const especialidadeSelect = document.getElementById('filter-especialidade').value;
  const statusSelect = document.getElementById('filter-status').value;
  const pacienteInput = document.getElementById('filter-paciente').value;
  
  // Valores do período personalizado, se aplicável
  let dataInicio = null;
  let dataFim = null;
  
  if (periodoSelect === 'custom') {
    dataInicio = document.getElementById('data-inicio').value;
    dataFim = document.getElementById('data-fim').value;
  }
  
  console.log('Filtros aplicados:', {
    periodo: periodoSelect,
    especialidade: especialidadeSelect,
    status: statusSelect,
    paciente: pacienteInput,
    dataInicio,
    dataFim
  });
  
  // Aqui você faria uma requisição para buscar os dados filtrados
  // fetch('/api/consultas/medico?' + new URLSearchParams({...filtros}))
}

/**
 * Limpa todos os filtros aplicados
 */
function limparFiltros() {
  document.getElementById('filter-periodo').value = '30';
  document.getElementById('filter-especialidade').value = '';
  document.getElementById('filter-status').value = '';
  document.getElementById('filter-paciente').value = '';
  document.getElementById('data-inicio').value = '';
  document.getElementById('data-fim').value = '';
  
  // Esconder período personalizado
  document.getElementById('custom-period').classList.add('hidden');
  
  // Recarregar os dados
  // Em uma implementação real você faria uma requisição para recarregar os dados
}
