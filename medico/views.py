from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from .models import Medico 


def home(request):
    return render(request, 'medico/tela_principal_medico.html')

def nova_consulta_medico(request):
    return render(request, 'medico/nova_consulta_medico.html')

def consulta_pendente_medico(request):
    return render(request, 'medico/consulta_pendente_medico.html',)

def atestado_medico(request):
    return render(request, 'medico/atestado_medico.html')

def prescricao_medico(request):
    return render(request, 'medico/prescricao_medico.html')


def emitir_prescricao_medico(request):
    if request.method == 'POST':
        paciente_id = request.POST.get('paciente_id')
        data_consulta = request.POST.get('data')
        hora_consulta = request.POST.get('hora')
        observacoes = request.POST.get('observacoes')

        paciente = get_object_or_404(Paciente, id=paciente_id)

        # Cria um arquivo PDF em memória
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Cabeçalho
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, height - 50, "Prescrição Médica")

        # Dados do paciente e da consulta
        p.setFont("Helvetica", 12)
        y = height - 100
        p.drawString(50, y, f"Paciente: {paciente.nome}")
        y -= 20
        p.drawString(50, y, f"Data da Consulta: {data_consulta}")
        y -= 20
        p.drawString(50, y, f"Hora da Consulta: {hora_consulta}")
        y -= 40

        # Observações (Prescrição)
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Prescrição:")
        y -= 20
        p.setFont("Helvetica", 12)
        textobject = p.beginText(50, y)
        for line in observacoes.splitlines():
            textobject.textLine(line)
        p.drawText(textobject)

        # Rodapé (opcional)
        p.setFont("Helvetica-Oblique", 10)
        p.drawString(50, 50, "Prescrição gerada automaticamente pelo sistema Saúde Fácil")

        # Finaliza e salva
        p.showPage()
        p.save()

        buffer.seek(0)

        # Prepara resposta para download
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="prescricao_{paciente.nome}.pdf"'
        return response

    else:
        # Se GET, renderiza a tela do formulário
        pacientes = Paciente.objects.all()
        return render(request, 'prescricao_medico', {'pacientes': pacientes})
