def create_client(clients, request,jsonify):
    new_client = request.get_json()
    clients.append(new_client)
    return jsonify(message='Client added successfully!', client=new_client), 201