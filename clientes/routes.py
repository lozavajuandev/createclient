from flask import jsonify, redirect, render_template, request, url_for, Blueprint
from models import Client, db

clients_bp= Blueprint('clients',__name__)

@clients_bp.route("/api/formulario", methods=["GET", "POST"])
def form():
    if request.method == "GET":
        return render_template("clientForm.html")
    elif request.method == "POST":
        return create_client()


@clients_bp.route("/api/clients", methods=["POST", "GET"])
def create_client():
    if request.method == "GET":
        clients = Client.query.all()
        return render_template("clients.html", clients=clients)
    elif request.method == "POST":
        new_client_db = Client(
            document=request.form.get("document"),
            document_type=request.form.get("document_type"),
            first_name=request.form.get("client_name"),
            last_name=request.form.get("client_lastname"),
            email=request.form.get("email"),
            phone=request.form.get("phone"),
            address=request.form.get("address"),
        )
    # Check if the document already exists
    existing_client = Client.query.filter_by(document=new_client_db.document).first()
    if existing_client:
        return jsonify(error="Client with this document already exists"), 400
    db.session.add(new_client_db)
    db.session.commit()
    print(new_client_db)
    return redirect(url_for("clients.confirmation", new_client=new_client_db.document))


@clients_bp.route("/api/confirmation", methods=["GET"])
def confirmation():
    client = Client.query.filter_by(document=request.args.get("new_client")).first()
    return render_template(
        "confirmation.html", new_client=request.args.get("new_client"), client=client
    )


@clients_bp.route("/api/clients/edit/<int:document>", methods=["GET", "POST"])
def edit_client(document):
    client = Client.query.filter_by(document=document).first()
    if not client:
        return jsonify(error="Client not found"), 404

    if request.method == "GET":
        return render_template("clientEditForm.html", client=client)

    elif request.method == "POST":
        # Update client details
        client.document_type = request.form.get("document_type", client.document_type)
        client.first_name = request.form.get("client_name", client.first_name)
        client.last_name = request.form.get("client_lastname", client.last_name)
        client.email = request.form.get("email", client.email)
        client.phone = request.form.get("phone", client.phone)
        client.address = request.form.get("address", client.address)

        db.session.commit()
        return redirect(url_for("clients.create_client"))


@clients_bp.route("/api/clients/delete/<int:document>", methods=["POST"])
def delete_client(document):
    client = Client.query.filter_by(document=document).first()
    if client:
        db.session.delete(client)
        db.session.commit()
        return redirect(url_for("clients.create_client"))
