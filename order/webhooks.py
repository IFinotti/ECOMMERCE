import json
import hashlib
import hmac
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
def webhook(request):
    if request.method == "POST":
        # Debug: Imprime headers e corpo da requisição
        print("Headers:", request.headers)
        print("Body:", request.body)

        # Obtém a assinatura do cabeçalho
        x_signature = request.headers.get("x-signature")
        x_request_id = request.headers.get("x-request-id")
        print("x-signature:", x_signature)
        print("x-request-id:", x_request_id)

        # Se x_signature estiver vazio, o problema pode ser com o header
        if not x_signature:
            return HttpResponse(status=400)

        # Obtém os dados da notificação
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(status=400)

        # Assinatura secreta gerada no Mercado Pago
        secret = "E9TxX34klUd15W8KYzmOm7fXaOZ5ajwK"

        # Criação do template
        template = f"id:{data['data']['id']};request-id:{x_request_id};ts:{data['date_created']};"
        print("Template:", template)

        # Gera o HMAC para validação
        hmac_obj = hmac.new(
            secret.encode(), msg=template.encode(), digestmod=hashlib.sha256)
        sha = hmac_obj.hexdigest()
        print("Generated SHA:", sha)

        # Verifica a assinatura
        try:
            received_sha = x_signature.split(",")[1].split("=")[1]
            print("Received SHA:", received_sha)
            if sha == received_sha:
                # Processar a notificação
                return HttpResponse(status=200)
        except IndexError:
            return HttpResponse(status=400)

        return HttpResponse(status=400)

    return HttpResponse(status=405)
