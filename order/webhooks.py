import json
import hashlib
import hmac
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
def webhook(request):
    if request.method == "POST":
        # Obtém a assinatura do cabeçalho
        x_signature = request.headers.get("x-signature")
        x_request_id = request.headers.get("x-request-id")

        # Obtém os dados da notificação
        data = json.loads(request.body)

        # Assinatura secreta gerada no Mercado Pago
        secret = "sua_assinatura_secreta_aqui"

        # Criação do template
        template = f"id:{data['data']['id']};request-id:{x_request_id};ts:{data['date_created']};"

        # Gera o HMAC para validação
        hmac_obj = hmac.new(
            secret.encode(), msg=template.encode(), digestmod=hashlib.sha256)
        sha = hmac_obj.hexdigest()

        # Verifica a assinatura
        if sha == x_signature.split(",")[1].split("=")[1]:
            # Processar a notificação
            # Aqui você pode atualizar seu banco de dados ou realizar outras ações com base no evento recebido
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

    return HttpResponse(status=405)
