from flask import Flask, render_template, request, redirect
import mercadopago

app = Flask(__name__)

# Coloque seu token do Mercado Pago aqui
sdk = mercadopago.SDK("APP_USR-6333712476891288-102317-6f72496bae2a37b303c36f5c40490937-1223631932")

@app.route('/')
def planos():
    # Renderiza a página planos.html (certifique-se que existe na pasta templates)
    return render_template('planos.html')

@app.route('/pagamento', methods=['POST'])
def pagamento():
    # Recebe dados do formulário e passa para pagamento.html
    plano = request.form['plano']
    valor = float(request.form['valor'])
    return render_template('pagamento.html', plano=plano, valor=valor)

@app.route('/pagar', methods=['POST'])
def pagar():
    # Realiza o pagamento usando a SDK do Mercado Pago
    valor = float(request.form['valor'])

    payment_data = {
        "transaction_amount": valor,
        "token": request.form['token'],
        "description": "Pagamento no app de filmes",
        "installments": 1,
        "payment_method_id": request.form['payment_method_id'],
        "payer": {
            "email": request.form['email']
        }
    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]

    status = payment.get("status")

    # Redireciona conforme status do pagamento
    if status == "approved":
        return redirect('/aprovado')
    elif status == "pending":
        return redirect('/pendente')
    else:
        return redirect('/recusado')

@app.route('/aprovado')
def aprovado():
    return render_template('aprovado.html')

@app.route('/pendente')
def pendente():
    return render_template('pendente.html')

@app.route('/recusado')
def recusado():
    return render_template('recusado.html')

if __name__ == '__main__':
    # Executa o Flask aceitando conexões externas (0.0.0.0) na porta 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
